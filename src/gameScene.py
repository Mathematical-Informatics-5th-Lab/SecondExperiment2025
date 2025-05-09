# gameScene.py
import pygame

class GameScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Leap Motion Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self, hand_position):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (0, 255, 0), hand_position, 30)
        pygame.display.flip()
        self.clock.tick(60)

    def should_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        return not self.running

    def cleanup(self):
        pygame.quit()
