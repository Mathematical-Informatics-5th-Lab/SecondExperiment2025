# gameScene.py
import random

import pygame

from config import Config
from scenes.playScene import PlayScene
from scenes.startScene import StartScene
from scenes.loadScene import LoadScene

# 定数
WIDTH = Config.WIDTH
HEIGHT = Config.HEIGHT
FRAME_RATE = Config.FRAME_RATE
class GameScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Blur Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.attr_using = random.choice(["finger", "palm", "grab"])

        self.current_scene = LoadScene(self.switch_scene)
        self.current_scene.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FRAME_RATE)


    def switch_scene(self, scene_name):
        if scene_name == "start":
            self.current_scene = StartScene(self.switch_scene)
        elif scene_name == "play":
            self.current_scene = PlayScene(self.switch_scene, self.attr_using)

    def should_quit(self):
        return not self.running

    def update(self, leap_data):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.current_scene.handle_event(event)

        # self.current_scene.update(hand_position)
        if self.attr_using == "finger":
            param = leap_data.finger_directions_to_parameter()
        elif self.attr_using == "palm":
            param = leap_data.palm_normal_to_parameter()
        elif self.attr_using == "grab":
            param = leap_data.palm_normal_to_parameter()

        self.current_scene.update(param)
        self.current_scene.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FRAME_RATE)

    def cleanup(self):
        pygame.quit()
