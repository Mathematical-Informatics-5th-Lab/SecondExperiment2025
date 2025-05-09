# scenes/playScene.py
import pygame
import random
import time
from .baseScene import BaseScene
import SoundGenerator
from config import Config

# 定数
WIDTH = Config.WIDTH
HEIGHT = Config.HEIGHT
FRAME_RATE = Config.FRAME_RATE
CHECK_INTERVAL = Config.CHECK_INTERVAL
WAIT_TIME = Config.WAIT_TIME
REPEAT_COUNT = Config.REPEAT_COUNT
THRESHOLD = Config.THRESHOLD

class PlayScene(BaseScene):
    def __init__(self, switch_scene_callback):
        self.switch_scene = switch_scene_callback
        self.font = pygame.font.SysFont(None, 36)
        self.sound_gen = SoundGenerator.RandomSoundGen()
        self.sound_gen.set_duration(1.0 / FRAME_RATE)
        pygame.mixer.pre_init(frequency=self.sound_gen.get_sample_rate(), size=-16, channels=2)
        self.reset_game()

    def reset_game(self):
        self.target_pos = random.uniform(0, 1)
        self.check_times = 0
        self.last_check = time.time()
        self.hand_position = 0
        self.state = "playing"  # "playing" / "waiting" / "done"
        self.wait_start_time = None
        self.result = None

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.event.post(event)

    def update(self, hand_position):
        now = time.time()

        if self.state == "playing":
            self.hand_position = min(max(hand_position, 0), 1)
            sound = self.sound_gen.generate(param=hand_position)
            sound.play()

            if now - self.last_check >= CHECK_INTERVAL:
                self.state = "waiting"
                self.wait_start_time = now
                self.frozen_hand_pos = self.hand_position
                self.check_times += 1

        elif self.state == "waiting":
            if now - self.wait_start_time >= WAIT_TIME:
                diff = abs(self.frozen_hand_pos - self.target_pos)
                self.last_check = now  # 次のチェックの基準を更新

                if diff < THRESHOLD:
                    self.result = "success"
                    self.state = "done"
                    self.done_time = now
                elif self.check_times >= REPEAT_COUNT:
                    self.result = "fail"
                    self.state = "done"
                    self.done_time = now
                else:
                    # 失敗だが回数は残っている → 再挑戦
                    self.state = "playing"

        elif self.state == "done":
            if now - self.done_time >= 1.0:
                self.switch_scene("start")

    def draw(self, screen):
        screen.fill((255, 255, 255))

        # ブラー効果（プレイ時のみ手に追従）
        blur_strength = self.frozen_hand_pos if self.state in ("waiting", "done") else self.hand_position
        max_radius = max(WIDTH, HEIGHT)
        steps = 50
        for i in range(steps):
            alpha = int(255 * blur_strength * (1 - i / steps))
            radius = int(max_radius * (i + 1) / steps)
            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (WIDTH // 2, HEIGHT // 2), radius)
            screen.blit(surf, (0, 0))

        # UI表示
        screen.blit(self.font.render(f"Target: {self.target_pos:.2f}", True, (0, 0, 0), (255, 255,255)), (20, 20))
        screen.blit(self.font.render(f"Your pos: {self.hand_position:.2f}", True, (0, 0, 0), (255, 255,255)), (20, 60))
        screen.blit(self.font.render(f"Attempt: {self.check_times}/{REPEAT_COUNT}", True, (0, 0, 0), (255, 255,255)), (20, 100))

        if self.state == "waiting":
            diff = abs(self.frozen_hand_pos - self.target_pos)
            similarity = max(0.0, 1.0 - diff / 1.0) * 100
            percent_text = f"Match: {similarity:.1f}%"
            screen.blit(self.font.render("Checking...", True, (100, 100, 100), (255, 255, 255)), (250, 300))
            screen.blit(self.font.render(percent_text, True, (0, 0, 0), (255, 255, 255)), (250, 340))

        if self.result == "success":
            screen.blit(self.font.render("🎉 Success! Returning...", True, (0, 150, 0)), (200, 400))
        elif self.result == "fail":
            screen.blit(self.font.render("❌ Failed. Returning...", True, (200, 0, 0)), (200, 400))
