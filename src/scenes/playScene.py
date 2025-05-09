# scenes/playScene.py
import pygame
import math
from .baseScene import BaseScene

WIDTH, HEIGHT = 800, 600

class PlayScene(BaseScene):
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.event.post(event)

    def update(self, hand_position):
        self.hand_position = hand_position

    def draw(self, screen):
        screen.fill((255, 255, 255))
        blur_strength = min(max(self.hand_position, 0), 1)

        max_radius = max(WIDTH, HEIGHT)
        steps = 50
        for i in range(steps):
            alpha = int(255 * blur_strength * (1 - i / steps))
            radius = int(max_radius * (i + 1) / steps)
            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (WIDTH // 2, HEIGHT // 2), radius)
            screen.blit(surf, (0, 0))
