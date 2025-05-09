# main.py
from leapInput import LeapInput
from gameScene import GameScene
import time

def main():
    leap_input = LeapInput()
    game_scene = GameScene()

    while not game_scene.should_quit():
        hand_pos = leap_input.get_hand_position()
        game_scene.update(hand_pos)
        time.sleep(0.01)

    game_scene.cleanup()

if __name__ == "__main__":
    main()
