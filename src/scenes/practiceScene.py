import pygame
from .baseScene import BaseScene
import SoundGenerator
from config import Config
from visualizer import HandVisualizer

WIDTH = Config.WIDTH
HEIGHT = Config.HEIGHT
MAIN_HEIGHT = Config.MAIN_HEIGHT
BAR_HEIGHT = Config.BAR_HEIGHT

class PracticeScene(BaseScene):
    def __init__(self, switch_scene_callback, attr_using):
        self.switch_scene = switch_scene_callback
        self.font = pygame.font.SysFont(None, 36)
        self.attr_using = attr_using

        self.hand_position = 0
        self.visualizer = HandVisualizer()
        self.player = SoundGenerator.RandomSoundPlayer()

        self.player.start(0.5)  # 初期音

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.event.post(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.player.stop()
                self.switch_scene("start")

    def update(self, hand_position):
        self.hand_position = min(max(hand_position, 0), 1)
        self.player.update_param(self.hand_position)

    def draw_circle_blur(self, screen, intensity):
        min_radius = min(WIDTH, MAIN_HEIGHT) * 0.01
        radius_range = min(WIDTH, MAIN_HEIGHT) * 0.3
        radius_t = max(WIDTH, MAIN_HEIGHT) * 0.3
        steps = 80

        for i in range(steps):
            t = i / steps
            radius = int(min_radius + radius_range * (1 - intensity) + radius_t * (1 - t))
            alpha = int(255 * t**2)
            color = (255, 255, 255, alpha)

            surf = pygame.Surface((WIDTH, MAIN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (WIDTH // 2, MAIN_HEIGHT // 2), radius)
            screen.blit(surf, (0, 0))

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # ブラー背景描画（手の位置に応じた強度）
        self.draw_circle_blur(screen, self.hand_position)

        # パラメータ表示
        text = self.font.render(f"Hand Pos: {self.hand_position:.2f}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

        # 手の視覚化（任意）
        self.visualizer.draw_hand(screen)

        # 下部バーに説明表示
        bar_rect = pygame.Rect(0, HEIGHT - BAR_HEIGHT, WIDTH, BAR_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), bar_rect)

        msg = "Move your hand to change the sound. Press ESC to return."
        footer_text = self.font.render(msg, True, (0, 0, 0))
        footer_rect = footer_text.get_rect(center=(WIDTH // 2, HEIGHT - BAR_HEIGHT // 2))
        screen.blit(footer_text, footer_rect)
