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
        hand = self.leap_input.get_hand_data()
        if not hand:
            return

        # 手のひらの位置を描画
        palm_pos = self.leap_input.get_joint_position(hand.palm)
        if self.is_valid_position(palm_pos):
            pygame.draw.circle(self.screen, self.hands_colour, palm_pos, 5)

        # 各指の骨を描画
        for digit in hand.digits:
            for bone in digit.bones:
                start_pos = self.leap_input.get_joint_position(bone.prev_joint)
                end_pos = self.leap_input.get_joint_position(bone.next_joint)

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
