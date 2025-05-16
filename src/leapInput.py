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

                        
                        # デバッグ出力（簡略版）
                        """print("=" * 30)
                        
                        print(f"Palm (x, y, z): ({self.leap_data.palm_x:.1f}, "
                            f"{self.leap_data.palm_y:.1f}, {self.leap_data.palm_z:.1f})")
                        print(f"Normal: ({self.leap_data.palm_normal_x:.2f}, "
                            f"{self.leap_data.palm_normal_y:.2f}, {self.leap_data.palm_normal_z:.2f})")
                        print(f"Grab: {self.leap_data.grab_strength:.2f}, Pinch: {self.leap_data.pinch_strength:.2f}")
                    
                        print(f"IndexDir: ({self.leap_data.finger_direction_x[1]:.2f}, "
                            f"{self.leap_data.finger_direction_y[1]:.2f}, "
                            f"{self.leap_data.finger_direction_z[1]:.2f})")
                        
                        print(self.leap_data.finger_directions_to_parameter())
                        print("=" * 30)
                        """
                        


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
                print(data.palm_normal_to_parameter())
                print(data.grab_strength_to_parameter())
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("終了します")

if __name__ == "__main__":
    main()
