# scenes/startScene.py
import pygame
from .baseScene import BaseScene

class LoadScene(BaseScene):
    def __init__(self, switch_scene_callback):
        self.font = pygame.font.SysFont(None, 48)
        self.button_rect = pygame.Rect(300, 250, 200, 80)
        self.switch_scene = switch_scene_callback

    def handle_event(self, event):
        pass

    def update(self, hand_position):
        pass  # 特に処理なし

    def draw(self, screen):
        screen.fill((255, 255, 255))
        text = self.font.render("Loading leapMotion...", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=self.button_rect.center))
