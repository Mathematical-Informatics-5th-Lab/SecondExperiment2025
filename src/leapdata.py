# leapInput.py
import threading
import time
import leap

class LeapData:
    def __init__(self, hand, fingers):
        # 1. 各指の幅
        self.finger_widths = [finger.width for finger in fingers]

        # 2. 各指の先端方向ベクトル
        self.finger_directions = [finger.direction for finger in fingers]

        # 3. 手のひらの向き（通常は hand.palm.normal で取得）
        self.palm_normal = hand.palm.normal

        # 4. 各指の先端位置
        self.finger_tip_positions = [finger.tip_position for finger in fingers]

        # 5. 手の開き具合（grab_strength: 握り具合, pinch_strength: つまみ具合）
        self.grab_strength = hand.grab_strength
        self.pinch_strength = hand.pinch_strength

        # 6. 手が左か右か（hand.type: leap.HandType.Left / Right）
        self.is_left = hand.type == leap.HandType.Left
        self.is_right = hand.type == leap.HandType.Right

        # 7. 手の位置（手のひらの中心座標）
        self.palm_position = hand.palm.position

