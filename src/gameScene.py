# gameScene.py
import pygame
from scenes.startScene import StartScene
from scenes.playScene import PlayScene

class GameScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Blur Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.scenes = {
            "start": StartScene(self.switch_scene),
            "play": PlayScene()
        }
        self.current_scene = self.scenes["start"]

    def switch_scene(self, scene_name):
        self.current_scene = self.scenes[scene_name]

    def should_quit(self):
        return not self.running

    def update(self, hand_position):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.current_scene.handle_event(event)

        self.current_scene.update(hand_position)
        self.current_scene.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def cleanup(self):
        pygame.quit()
