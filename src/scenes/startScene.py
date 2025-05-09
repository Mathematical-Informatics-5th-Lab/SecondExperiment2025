# scenes/startScene.py
import pygame
from .baseScene import BaseScene

class StartScene(BaseScene):
    def __init__(self, switch_scene_callback):
        self.font = pygame.font.SysFont(None, 48)
        self.button_rect = pygame.Rect(300, 250, 200, 80)
        self.switch_scene = switch_scene_callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.switch_scene("play")

    def update(self, hand_position):
        pass  # 特に処理なし

    def draw(self, screen):
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (70, 130, 180), self.button_rect)
        text = self.font.render("Start", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=self.button_rect.center))
