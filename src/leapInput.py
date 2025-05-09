# leapInput.py
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
                        fingers = hand.fingers
                        self.leap_data = LeapData(hand, fingers)

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
        return self.leap_data
