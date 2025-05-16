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
    
    def _calculate_similarity(self, hand_pos, target_pos):
        """
        手の位置とターゲット位置の類似度を計算するメソッド
        Parameters
        ----------
        hand_pos : float
            手の位置
        target_pos : float
            ターゲット位置
        Returns
        -------
        float
            類似度 (0.0~1.0)
        """
        diff = abs(hand_pos - target_pos)
        if diff < THRESHOLD:
            return 1.0

        diff = min(abs(hand_pos - target_pos - THRESHOLD), abs(hand_pos - target_pos + THRESHOLD))
        if target_pos > 0.5:
            denominator = target_pos - THRESHOLD
        else:
            denominator = 1 - (target_pos + THRESHOLD)
        return 1 - diff / denominator

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
        screen.fill((0, 0, 255, 30))

        hand_pos = self.frozen_hand_pos if self.state in ["waiting", "done"] else self.hand_position
        similarity = self._calculate_similarity(hand_pos, self.target_pos)
        min_radius = min(WIDTH, HEIGHT)  * 0.01
        radius_similarity = min(WIDTH, HEIGHT) * 0.3
        radius_t = max(WIDTH, HEIGHT)*0.3
        steps = 80  # より滑らかに

        for i in range(steps):
            t = i / steps
            radius = int(min_radius + radius_similarity * (1- similarity) + radius_t * (1 - t))  # 中央が濃くなるように調整

            # alpha を外側が強くなるように調整（指数カーブ）
            alpha = int(255 * t**2)  # 外が濃くなる
            color = (255, 255, 255, alpha)

            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (WIDTH // 2, HEIGHT // 2), radius)
            screen.blit(surf, (0, 0))

        # 中央にパーセンテージ表示
        font = pygame.font.SysFont(None, 100)
        text = font.render(f"{int(similarity * 100)}%", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        # UI表示
        screen.blit(self.font.render(f"Target: {self.target_pos:.2f}", True, (0, 0, 0), (255, 255,255)), (20, 20))
        screen.blit(self.font.render(f"Your pos: {self.hand_position:.2f}", True, (0, 0, 0), (255, 255,255)), (20, 60))
        screen.blit(self.font.render(f"Attempt: {self.check_times}/{REPEAT_COUNT}", True, (0, 0, 0), (255, 255,255)), (20, 100))

        if self.state == "waiting":
            percent_text = f"Match: {similarity*100:.1f}%"
            screen.blit(self.font.render("Checking...", True, (100, 100, 100), (255, 255, 255)), (250, 300))
            screen.blit(self.font.render(percent_text, True, (0, 0, 0), (255, 255, 255)), (250, 340))

        if self.result == "success":
            screen.blit(self.font.render("🎉 Success! Returning...", True, (0, 150, 0)), (200, 400))
        elif self.result == "fail":
            screen.blit(self.font.render("❌ Failed. Returning...", True, (200, 0, 0)), (200, 400))
