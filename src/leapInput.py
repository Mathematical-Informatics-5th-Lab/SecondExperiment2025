import threading
import time
import leap
from leapdata import LeapData

class LeapInput:
    def __init__(self):
        self._start_listener()
        self.leap_data = None

    def _start_listener(self):
        def leap_thread():
            class MyListener(leap.Listener):
                def on_tracking_event(_, event):
                    if event.hands:
                        hand = event.hands[0]
                        fingers = hand.digits
                        #print(dir(event.hands[0]))
                        self.leap_data = LeapData(hand, fingers)

                        
                        # デバッグ出力
                        print("Palm position (x, y, z):", 
                              self.leap_data.palm_x, 
                              self.leap_data.palm_y, "\n",
                              self.leap_data.palm_z)
                        print("Palm normal (x, y, z):", 
                              self.leap_data.palm_normal_x, 
                              self.leap_data.palm_normal_y, 
                              self.leap_data.palm_normal_z)
                        print("is_left:", self.leap_data.is_left)
                        print("Grab strength:", self.leap_data.grab_strength)
                        print("-" * 40)
                        

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
        return self.leap_data

def main():
    leap_input = LeapInput()

    try:
        while True:
            data = leap_input.get_hand_position()
            if data:
                print("== get_hand_position() の結果 ==")
                print("Palm:", data.palm_x, data.palm_y, data.palm_z)
                print("Grab strength:", data.grab_strength)
                print("-" * 50)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("終了します")

if __name__ == "__main__":
    main()
