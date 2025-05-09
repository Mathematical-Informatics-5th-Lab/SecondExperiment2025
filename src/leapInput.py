# leapInput.py
import threading
import time
import leap

class LeapInput:
    def __init__(self):
        self.hand_position = (320, 240)
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
