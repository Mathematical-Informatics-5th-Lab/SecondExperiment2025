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
        
        game_scene.update(leap_data)

    game_scene.cleanup()

if __name__ == "__main__":
    main()
