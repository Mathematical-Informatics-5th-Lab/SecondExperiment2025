# leapInput.py
import threading
import time
import leap
import math

class LeapInput:
    def __init__(self):
        self.hand_position = (320, 240)
        self.hand_data = None
        self._start_listener()

    def _start_listener(self):
        def leap_thread():
            class MyListener(leap.Listener):
                def on_tracking_event(_, event):
                    if event.hands:
                        hand = event.hands[0]
                        palm = hand.palm.position
                        x = int(palm.x) + 320
                        y = 480 - int(palm.y)
                        self.hand_position = (x, y)
                        self.hand_data = hand

            listener = MyListener()
            connection = leap.Connection()
            connection.add_listener(listener)
            with connection.open():
                connection.set_tracking_mode(leap.TrackingMode.Desktop)
                while True:
                    time.sleep(0.01)

        thread = threading.Thread(target=leap_thread, daemon=True)
        thread.start()

    def get_hand_position(self):
        return self.hand_position

    def get_hand_data(self):
        return self.hand_data

    def get_joint_position(self, bone):
        if bone:
            try:
                if hasattr(bone, 'position'):
                    # Palmオブジェクトの場合
                    x = bone.position.x
                    z = bone.position.z
                else:
                    # 通常の骨の場合
                    x = bone.x
                    z = bone.z

                # NaNチェック
                if math.isnan(x) or math.isnan(z):
                    return None

                return int(x + 320), int(z + 240)
            except (AttributeError, ValueError):
                return None
        return None

if __name__ == "__main__":
    leap_input = LeapInput()
    while True:
        print(leap_input.get_hand_position())
        time.sleep(0.3)
