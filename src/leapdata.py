# leapInput.py
import threading
import time
import leap
import math
import numpy as np

class LeapData:
    def __init__(self, hand, fingers):
        # 指の方向ベクトル（distal bone の方向）を指ごとに取得
        self.finger_direction_x = []
        self.finger_direction_y = []
        self.finger_direction_z = []

        for digit in fingers:
            distal_bone = digit.bones[3]  # 3: Distal bone
            if distal_bone:
                vec = [0, 0, 0]
                vec[0] = distal_bone.next_joint.x - distal_bone.prev_joint.x
                vec[1] = distal_bone.next_joint.y - distal_bone.prev_joint.y
                vec[2] = distal_bone.next_joint.z - distal_bone.prev_joint.z
                norm = np.linalg.norm([vec[0], vec[1], vec[2]])
                if norm != 0:
                    self.finger_direction_x.append(vec[0] / norm)
                    self.finger_direction_y.append(vec[1] / norm)
                    self.finger_direction_z.append(vec[2] / norm)
                else:
                    self.finger_direction_x.append(0.0)
                    self.finger_direction_y.append(0.0)
                    self.finger_direction_z.append(0.0)
            else:
                self.finger_direction_x.append(0.0)
                self.finger_direction_y.append(0.0)
                self.finger_direction_z.append(0.0)

        
        """
        # 指の幅（distal bone の直径）
        self.finger_widths = [finger.distal.Width for finger in fingers]
        """
        # 手のひらの法線ベクトル
        self.palm_normal_x = hand.palm.normal.x
        self.palm_normal_y = hand.palm.normal.y
        self.palm_normal_z = hand.palm.normal.z

        # 開き具合
        self.grab_strength = hand.grab_strength
        self.pinch_strength = hand.pinch_strength

        # 左右判定
        self.is_left = hand.type == leap.HandType.Left
        self.is_right = hand.type == leap.HandType.Right

        # 手の位置
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
        if len(self.finger_direction_x) <= 1:
            raise ValueError("self.finger_directions に十分なデータがありません")

        # 基準ベクトルを定義
        reference_vector = [1 / math.sqrt(3), 1 / math.sqrt(3), -1 / math.sqrt(3)]

        # 指定された指の方向ベクトルを取得
        direction = [self.finger_direction_x[1], self.finger_direction_y[1], self.finger_direction_z[1]]

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
    
    

