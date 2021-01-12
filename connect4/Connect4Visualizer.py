import pygame
pygame.init()

BLACK = 0,0,0
RED = 255,0,0
BLUE = 0,0,255
WHITE = 255, 255, 255

pygame.font.init()

class Connect4Visualizer:
    def __init__(self, rows=6, columns=7, width=640, height=480):
        self.rows = rows
        self.cols = columns
        self.screen = pygame.display.set_mode((width, height))

        self.width = width
        self.height = height
        self.radius = height / 20
        self.box_size = height / (rows + 2)
        self.left_disp_offset = self.box_size * 2
        self.top_disp_offset = self.box_size

        self.game_closed = False


    def draw_board(self, canonical_board, red_label=1, blue_label=-1):
        if not self.game_closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_closed = True
                    pygame.quit()

            # Reset screen
            self.screen.fill(BLACK)

            # Drawing the grid
            my_font = pygame.font.SysFont("monospace", 20)
            for row_num in range(self.rows + 1):
                row_start = (self.left_disp_offset, self.top_disp_offset + (self.box_size * row_num))
                row_end = (self.left_disp_offset + (self.box_size * self.cols), self.top_disp_offset + (self.box_size * row_num))
                pygame.draw.line(self.screen, WHITE, row_start, row_end)
            for col_num in range(self.cols + 1):
                col_start = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset)
                col_end = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset + (self.box_size * self.rows))
                if col_num > 0:
                    col_label = my_font.render(str(col_num), 1, WHITE)
                    self.screen.blit(col_label, (self.left_disp_offset + (self.box_size * col_num) - self.box_size / 2, self.height - 40))
                pygame.draw.line(self.screen, WHITE, col_start, col_end)

            # Drawing pieces
            for row_num, row in enumerate(canonical_board):
                for col_num, element in enumerate(row):
                    pos = (int(self.box_size * (col_num + 0.5)) + self.left_disp_offset,
                           int(self.box_size * (row_num + 0.5)) + self.top_disp_offset)
                    if element == red_label:
                        pygame.draw.circle(self.screen, RED, pos, self.radius)
                    elif element == blue_label:
                        pygame.draw.circle(self.screen, BLUE, pos, self.radius)
            pygame.display.flip()
            pygame.time.wait(1000)
