import leap  # Leap Motion SDK に応じて適切に import

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