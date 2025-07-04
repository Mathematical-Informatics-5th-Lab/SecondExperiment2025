# scenes/playScene.py
import pygame
import random
import time
from .baseScene import BaseScene
import SoundGenerator
from config import Config
from visualizer import HandVisualizer

# 定数
WIDTH = Config.WIDTH
HEIGHT = Config.HEIGHT
FRAME_RATE = Config.FRAME_RATE
CHECK_INTERVAL = Config.CHECK_INTERVAL
WAIT_TIME = Config.WAIT_TIME
REPEAT_COUNT = Config.REPEAT_COUNT
THRESHOLD = Config.THRESHOLD
BAR_HEIGHT = Config.BAR_HEIGHT
MAIN_HEIGHT = Config.MAIN_HEIGHT

class PlayScene(BaseScene):
    def __init__(self, switch_scene_callback, attr_using):
        self.switch_scene = switch_scene_callback
        self.font = pygame.font.SysFont(None, 36)
        self.attr_using = attr_using

        self.player = SoundGenerator.RandomSoundPlayer()
        self.reset_game()
        self.visualizer = HandVisualizer()

    def reset_game(self):
        # TODO: 理想的なパラメータがあれば, その範囲になるように調整する必要あり
        self.target_pos = random.uniform(0, 1)

        self.check_times = 0
        self.last_check = time.time()
        self.hand_position = 0
        self.state = "listening"  # 最初は正解音提示フェーズ
        self.listen_start_time = time.time()
        self.result = None
        self.wait_start_time = None

        self.remaining_time = CHECK_INTERVAL

        self.player.start(self.target_pos)
    
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

        if self.state == "listening":
            # 最初の正解音を3秒流すだけ
            if now - self.listen_start_time >= 3.0:
                self.state = "playing"
                self.last_check = now
                self.player.update_param(self.target_pos)  # 最初は0.0で始める（updateで更新される）

        elif self.state == "playing":
            self.hand_position = min(max(hand_position, 0), 1)
            self.player.update_param(self.hand_position)

            if now - self.last_check >= CHECK_INTERVAL:
                self.state = "waiting"
                self.wait_start_time = now
                self.frozen_hand_pos = self.hand_position
                self.check_times += 1
                self.player.update_param(self.frozen_hand_pos)  # 自分の音を固定

            self.remaining_time = max(0.0, CHECK_INTERVAL - (now - self.last_check))


        elif self.state == "waiting":
            elapsed = now - self.wait_start_time
            if elapsed >= WAIT_TIME:
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
                    self.state = "playing"

        elif self.state == "done":
            if now - self.done_time >= 1.0:
                self.player.stop()
                self.switch_scene("start")

    def draw_circle(self, screen, similarity):
        min_radius = min(WIDTH, MAIN_HEIGHT)  * 0.01
        radius_similarity = min(WIDTH, MAIN_HEIGHT) * 0.3
        radius_t = max(WIDTH, MAIN_HEIGHT)*0.3
        steps = 80  # より滑らかに

        for i in range(steps):
            t = i / steps
            radius = int(min_radius + radius_similarity * (1- similarity) + radius_t * (1 - t))  # 中央が濃くなるように調整

            # alpha を外側が強くなるように調整（指数カーブ）
            alpha = int(255 * t**2)  # 外が濃くなる
            color = (255, 255, 255, alpha)

            surf = pygame.Surface((WIDTH, MAIN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (WIDTH // 2, MAIN_HEIGHT // 2), radius)
            screen.blit(surf, (0, 0))

    def draw_percentage(self, screen, similarity):
        # 中央にパーセンテージ表示
        font = pygame.font.SysFont(None, 100)
        text = font.render(f"{int(similarity * 100)}%", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, MAIN_HEIGHT // 2))
        screen.blit(text, text_rect)

    def draw_current_status(self, screen):
        screen.blit(self.font.render(f"Target: {self.target_pos:.2f}", True, (0, 0, 0), (255, 255,255)), (20, 20))
        screen.blit(self.font.render(f"Your pos: {self.hand_position:.2f}", True, (0, 0, 0), (255, 255,255)), (20, 60))
        screen.blit(self.font.render(f"Attempt: {self.check_times}/{REPEAT_COUNT}", True, (0, 0, 0), (255, 255,255)), (20, 100))

    def draw_below_text(self, screen, text):
        # 白いバーを画面下に描画
        bar_rect = pygame.Rect(0, HEIGHT - BAR_HEIGHT, WIDTH, BAR_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), bar_rect)

        # テキストの描画
        text_surf = self.font.render(text, True, (0, 0, 0))  # 黒文字
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT - BAR_HEIGHT // 2))
        screen.blit(text_surf, text_rect)

    def draw(self, screen):
        screen.fill((0, 0, 255, 30))

        hand_pos = self.frozen_hand_pos if self.state in ["waiting", "done"] else self.hand_position
        similarity = self._calculate_similarity(hand_pos, self.target_pos)

        self.draw_circle(screen, similarity)
        self.draw_current_status(screen)

        self.visualizer.draw_hand(screen)

        if self.state == "waiting":
            label = "Target Sound"
            self.draw_percentage(screen, similarity)
            self.draw_below_text(screen, label)

        if self.state == "playing":
            countdown_text = f"Next check in: {self.remaining_time:.1f}s"
            self.draw_below_text(screen, countdown_text)
        if self.state == "listening":
            self.draw_below_text(screen, "Listening to Target Sound...")
        if self.result == "success":
            self.draw_below_text(screen, "Success! Returning to Start Scene...")
        elif self.result == "fail":
            self.draw_below_text(screen, "Failed. Returning to Start Scene...")
