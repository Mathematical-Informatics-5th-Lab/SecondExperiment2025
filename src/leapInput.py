import threading
import time
import leap
from leapdata import LeapData

class LeapInput:
    def __init__(self):
        self._start_listener()
        self._latest_data = LeapData.empty()  # ← 前回のデータ保持用
        self.leap_data = LeapData.empty()
        self.is_changed = False

    def _start_listener(self):
        def leap_thread():
            class MyListener(leap.Listener):
                def on_tracking_event(_, event):
                    if event.hands:
                        hand = event.hands[0]
                        fingers = hand.digits
                        data = LeapData(hand, fingers)
                        self.leap_data = data
                        self._latest_data = data  # ← 最新値を保持
                        self.is_changed = True

            listener = MyListener()
            connection = leap.Connection()
            connection.add_listener(listener)
            with connection.open():
                connection.set_tracking_mode(leap.TrackingMode.Desktop)
                while True:
                    time.sleep(0.1)

        thread = threading.Thread(target=leap_thread, daemon=True)
        thread.start()

    def get_hand_position(self):
        return self._latest_data, self.is_changed

def main():
    leap_input = LeapInput()
    t = 0
    try:
        while True:
            data = leap_input.get_hand_position()
            time.sleep(0.5)
            print(t)
            t += 1
    except KeyboardInterrupt:
        print("終了します")

if __name__ == "__main__":
    main()
