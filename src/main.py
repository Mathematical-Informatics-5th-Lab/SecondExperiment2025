# main.py
from leapInput import LeapInput
from gameScene import GameScene
import time
import random

def main():
    leap_input = LeapInput()
    game_scene = GameScene()

    while not game_scene.should_quit():
        leap_data, is_changed = leap_input.get_hand_position()
        if is_changed:
            game_scene.switch_scene("start")
            break

    while not game_scene.should_quit():
        leap_data, is_changed = leap_input.get_hand_position()
        if not is_changed:
            continue
        
        game_scene.update(leap_data)

    game_scene.cleanup()

if __name__ == "__main__":
    main()
