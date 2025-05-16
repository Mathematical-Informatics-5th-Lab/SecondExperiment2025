import pygame
import sys
from leapInput import LeapInput


class HandVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Leap Motion Hand Visualizer")
        self.clock = pygame.time.Clock()
        self.leap_input = LeapInput()
        self.hands_colour = (255, 255, 255)
        self.background_colour = (0, 0, 0)
        # 画面の中心座標を計算
        self.screen_center_x = self.screen.get_width() // 2
        self.screen_center_y = self.screen.get_height() // 2

    def transform_coordinates(self, x, z):
        """Leap Motionの座標をPygameの座標系に変換"""
        # x座標はそのまま、z座標はy座標として使用
        if x is None or z is None:
            return None
        # スケーリング係数（必要に応じて調整）
        scale = 1.0
        screen_x = self.screen_center_x + x * scale
        screen_y = self.screen_center_y + z * scale
        return (screen_x, screen_y)

    def is_valid_position(self, pos):
        if pos is None:
            return False
        try:
            x, y = pos
            return (
                isinstance(x, (int, float))
                and isinstance(y, (int, float))
                and 0 <= x < self.screen.get_width()
                and 0 <= y < self.screen.get_height()
            )
        except (TypeError, ValueError):
            return False

    def draw_hand(self):
        leap_data = self.leap_input.get_hand_position()
        if not leap_data or leap_data.palm_x is None or leap_data.palm_z is None:
            return

        # 手のひらの位置を描画
        palm_pos = self.transform_coordinates(leap_data.palm_x, leap_data.palm_z)
        if self.is_valid_position(palm_pos):
            pygame.draw.circle(self.screen, self.hands_colour, palm_pos, 5)

        def get_joint_position(joint):
            if joint is None or joint.x is None or joint.z is None:
                return None
            return self.transform_coordinates(joint.x, joint.z)

        # 各指の骨を描画
        for digit in leap_data.fingers:
            if digit is None:
                continue
            for bone in digit.bones:
                if bone is None or bone.prev_joint is None or bone.next_joint is None:
                    continue
                start_pos = get_joint_position(bone.prev_joint)
                end_pos = get_joint_position(bone.next_joint)

                if start_pos is None or end_pos is None:
                    continue

                if self.is_valid_position(start_pos) and self.is_valid_position(
                    end_pos
                ):
                    try:
                        pygame.draw.line(
                            self.screen, self.hands_colour, start_pos, end_pos, 2
                        )
                        pygame.draw.circle(self.screen, self.hands_colour, start_pos, 3)
                        pygame.draw.circle(self.screen, self.hands_colour, end_pos, 3)
                    except (TypeError, ValueError):
                        continue

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # 画面をクリア
            self.screen.fill(self.background_colour)

            # 手の描画
            self.draw_hand()

            # 画面を更新
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    visualizer = HandVisualizer()
    visualizer.run()
