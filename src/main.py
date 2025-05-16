# main.py
from leapInput import LeapInput
from gameScene import GameScene
import time
import random

def main():
    leap_input = LeapInput()
    game_scene = GameScene()

    while not game_scene.should_quit():
        leap_data = leap_input.get_hand_position()
        if leap_data is None:
            continue
        param = leap_data.finger_directions_to_parameter()
        if param is None:
            continue
        # hand_pos = random.random()  # テスト用
        game_scene.update(param)

    game_scene.cleanup()

if __name__ == "__main__":
    main()
