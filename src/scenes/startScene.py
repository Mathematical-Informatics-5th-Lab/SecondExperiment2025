# scenes/startScene.py
import pygame
from .baseScene import BaseScene

class StartScene(BaseScene):
    def __init__(self, switch_scene_callback):
        self.font = pygame.font.SysFont(None, 48)
        self.start_button_rect = pygame.Rect(300, 200, 200, 80)
        self.practice_button_rect = pygame.Rect(300, 320, 200, 80)
        self.switch_scene = switch_scene_callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                self.switch_scene("play")
            elif self.practice_button_rect.collidepoint(event.pos):
                self.switch_scene("practice")

    def update(self, hand_position):
        pass  # 特に処理なし

    def draw(self, screen):
        screen.fill((30, 30, 30))

        # Startボタン
        pygame.draw.rect(screen, (70, 130, 180), self.start_button_rect)
        start_text = self.font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, start_text.get_rect(center=self.start_button_rect.center))

        # Practiceボタン
        pygame.draw.rect(screen, (100, 180, 100), self.practice_button_rect)
        practice_text = self.font.render("Practice", True, (255, 255, 255))
        screen.blit(practice_text, practice_text.get_rect(center=self.practice_button_rect.center))
