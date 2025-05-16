# leapInput.py
import threading
import time
import leap
import math

class LeapData:
    def __init__(self, hand, fingers):
        """
        # 1. 各指の幅（tip.radius × 2）[15 ~ 25 mm 程度]
        self.finger_widths = [finger.tip.radius * 2 for finger in fingers]

        # 2. 各指の方向ベクトル（軸ごとに分解）
        self.finger_direction_x = [finger.direction.x for finger in fingers]
        self.finger_direction_y = [finger.direction.y for finger in fingers]
        self.finger_direction_z = [finger.direction.z for finger in fingers]
        """

        # 3. 手のひらの法線ベクトル（軸ごとに）
        self.palm_normal_x = hand.palm.normal.x
        self.palm_normal_y = hand.palm.normal.y
        self.palm_normal_z = hand.palm.normal.z

        """
        # 4. 各指の先端位置（軸ごとに）
        self.finger_tip_x = [finger.tip.position.x for finger in fingers]
        self.finger_tip_y = [finger.tip.position.y for finger in fingers]
        self.finger_tip_z = [finger.tip.position.z for finger in fingers]
        """

        # 5. 開き具合
        self.grab_strength = hand.grab_strength  # 0.0 ~ 1.0
        self.pinch_strength = hand.pinch_strength  # 0.0 ~ 1.0

        # 6. 左右判定
        self.is_left = hand.type == leap.HandType.Left
        self.is_right = hand.type == leap.HandType.Right

        # 7. 手の位置（軸ごとに）
        self.palm_x = hand.palm.position.x
        self.palm_y = hand.palm.position.y
        self.palm_z = hand.palm.position.z


    def variable_range(self, variable_name: str):
        # 変数名に応じた値域を返す
        ranges = {
            "finger_widths": [15, 25],  # mm
            "finger_direction_x": [-1.0, 1.0],
            "finger_direction_y": [-1.0, 1.0],
            "finger_direction_z": [-1.0, 1.0],
            "palm_normal_x": [-1.0, 1.0],
            "palm_normal_y": [-1.0, 1.0],
            "palm_normal_z": [-1.0, 1.0],
            "finger_tip_x": [-200, 200],
            "finger_tip_y": [0, 500],
            "finger_tip_z": [-200, 200],
            "grab_strength": [0.0, 1.0],
            "pinch_strength": [0.0, 1.0],
            "palm_x": [-200, 200],
            "palm_y": [0, 500],
            "palm_z": [-200, 200],
        }
        return ranges.get(variable_name, None)
        # 指定された変数名が存在しない場合は None を返す
        

    def normalize_values(self, value, value_range):
        """値を0以上1以下の範囲に正規化する関数"""
        min_value=value_range[0]
        max_value=value_range[1]

        normalized = (value - min_value) / (max_value - min_value)
        return normalized  # 0以上1以下に制限



    def finger_directions_to_parameter(self):
        """
        self.finger_directions[1] のベクトルと 1/sqrt(3) * [1, 1, -1] の内積を計算し、
        0以上1以下に正規化して返す関数
        """
        if len(self.finger_directions) <= 1:
            raise ValueError("self.finger_directions に十分なデータがありません")

        # 基準ベクトルを定義
        reference_vector = [1 / math.sqrt(3), 1 / math.sqrt(3), -1 / math.sqrt(3)]

        # 指定された指の方向ベクトルを取得
        direction = self.finger_directions[1]

        # 内積を計算
        dot_product = sum(d * r for d, r in zip(direction, reference_vector))

        # 内積を 0 以上 1 以下に正規化
        normalized_dot_product = (dot_product + 1) / 2

        return max(0, min(1, normalized_dot_product))  # 0以上1以下に制限
    
    def palm_normal_to_parameter(self):
        """
        self.palm_normal のベクトルと 1/3 * [2, 2, 1] の内積を計算し、
        0以上1以下に正規化して返す関数
        """
        if not self.palm_normal:
            raise ValueError("self.palm_normal にデータがありません")

        # 基準ベクトルを定義
        reference_vector = [2 / 3, 2 / 3, 1 / 3]

        # 手のひらの法線ベクトルを取得
        normal = self.palm_normal

        # 内積を計算
        dot_product = sum(n * r for n, r in zip(normal, reference_vector))

        # 内積を 0 以上 1 以下に正規化
        normalized_dot_product = (dot_product + 1) / 2

        return max(0, min(1, normalized_dot_product))  # 0以上1以下に制限
    

    def grab_strength_to_parameter(self):
        """
        grab_strength (0~1) を入力として y = -4x(x-1) の値を計算して返す関数
        """
        if not (0 <= self.grab_strength <= 1):
            raise ValueError("grab_strength は 0 以上 1 以下である必要があります")

        # y = -4x(x-1) の計算
        x = self.grab_strength
        if self.is_left:
            x*=1/2
        return x
    
    

