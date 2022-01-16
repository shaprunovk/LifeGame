import sys
import pygame
import random

# Default settings
SIZE = 10
C_LIVE = 1
C_DEAD = 0
WIDTH = 1280
HEIGHT = 720
# Default colors
DEAD = (0, 0, 0)
LIVE = (50, 170, 55)


class Game:
    class Field:

        def __init__(self, columns_cnt, rows_cnt):
            self.columns_cnt = columns_cnt
            self.rows_cnt = rows_cnt
            self.current = []
            self.glider_seed = 0
            self.create()

        class Cell:

            def __init__(self, color=None, size=SIZE, row=0, column=0):
                self.size = size
                self.row = row
                self.column = column
                if color is None:
                    self.color = random.randint(C_DEAD, C_LIVE)
                else:
                    self.color = color

            def get_color(self):
                return self.color

            def set_color(self, color):
                self.color = color

            def recolor(self, field):
                neigh_cnt = 0
                for delta_x in range(-1, 2, 1):
                    for delta_y in range(-1, 2, 1):
                        if not (delta_y * delta_x == 0 and delta_y + delta_x == 0):
                            neigh_cnt += field.seed_field.current[(self.column + delta_x) % field.columns_cnt][
                                (self.row + delta_y) % field.rows_cnt].get_color()
                if self.get_color() == C_LIVE:
                    if neigh_cnt == 2 or neigh_cnt == 3:
                        return C_LIVE
                    else:
                        return C_DEAD
                elif self.get_color() == C_DEAD:
                    if neigh_cnt == 3:
                        return C_LIVE
                return self.get_color()

        def create(self, color=None):
            field_temp = [[self.Cell()] * self.rows_cnt for _ in range(self.columns_cnt)]
            for column in range(self.columns_cnt):
                for row in range(self.rows_cnt):
                    field_temp[column][row] = self.Cell(color=color, column=column, row=row)
            self.current = field_temp

        def add_glider(self, current_field):
            glider = [[C_DEAD, C_DEAD, C_LIVE], [C_LIVE, C_DEAD, C_LIVE], [C_DEAD, C_LIVE, C_LIVE]]
            for x in range(3):
                for y in range(3):
                    current_field[(self.glider_seed + x) % self.columns_cnt][y % self.rows_cnt]\
                        .set_color(glider[x][y])
            self.glider_seed += 5
            return current_field

        def create_gosper_glider_gun_field(self):
            self.create(C_DEAD)
            column_gun_seed = 0
            # column_gun_seed = self.columns_cnt // 2 - 20
            row_gun_seed = 0
            # row_gun_seed = self.rows_cnt // 2 - 20
            gun = [[0] * 38 for _ in range(11)]
            gun[5][1] = gun[5][2] = C_LIVE
            gun[6][1] = gun[6][2] = C_LIVE
            gun[3][13] = gun[3][14] = C_LIVE
            gun[4][12] = gun[4][16] = C_LIVE
            gun[5][11] = gun[5][17] = C_LIVE
            gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = C_LIVE
            gun[7][11] = gun[7][17] = C_LIVE
            gun[8][12] = gun[8][16] = C_LIVE
            gun[9][13] = gun[9][14] = C_LIVE
            gun[1][25] = C_LIVE
            gun[2][23] = gun[2][25] = C_LIVE
            gun[3][21] = gun[3][22] = C_LIVE
            gun[4][21] = gun[4][22] = C_LIVE
            gun[5][21] = gun[5][22] = C_LIVE
            gun[6][23] = gun[6][25] = C_LIVE
            gun[7][25] = C_LIVE
            gun[3][35] = gun[3][36] = C_LIVE
            gun[4][35] = gun[4][36] = C_LIVE
            for x in range(11):
                for y in range(38):
                    self.current[(column_gun_seed + x) % self.columns_cnt][(row_gun_seed + y) % self.rows_cnt]\
                        .set_color(gun[x][y])

    def __init__(self, screen_width=WIDTH, screen_height=HEIGHT):
        pygame.init()
        self.pause = False
        self.quit = False
        self.screen_height = screen_height
        self.screen_width = screen_width

        self.cell_size = self.Field.Cell().size
        self.columns_cnt = self.screen_width // self.cell_size
        self.rows_cnt = self.screen_height // self.cell_size
        self.seed_field = self.Field(self.columns_cnt, self.rows_cnt)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.flip()

    def print(self):
        for column in range(self.columns_cnt):
            for row in range(self.rows_cnt):
                if self.seed_field.current[column][row].get_color() == C_LIVE:
                    color = LIVE
                else:
                    color = DEAD
                pygame.draw.polygon(self.screen, color, [(column * self.cell_size, row * self.cell_size),
                                                         ((column + 1) * self.cell_size, row * self.cell_size),
                                                         ((column + 1) * self.cell_size, (row + 1) * self.cell_size),
                                                         (column * self.cell_size, (row + 1) * self.cell_size)])
        pygame.display.flip()

    def next_field(self):
        temp = self.Field(self.columns_cnt, self.rows_cnt)
        for column in range(self.columns_cnt):
            for row in range(self.rows_cnt):
                next_color = self.seed_field.current[column][row].recolor(self)
                temp.current[column][row] = self.Field.Cell(color=next_color, column=column, row=row)
        self.seed_field = temp

    def press_buttons(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    # Spawns glider at the (5 * button presses, 0) cell (Every press adds 5 to x coordinate)
                    self.seed_field.current = self.seed_field.add_glider(self.seed_field.current)
                elif event.key == pygame.K_p:  # Pause the game
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True
                elif event.key == pygame.K_c:  # Clear the field
                    self.seed_field.create(C_DEAD)
                elif event.key == pygame.K_f:  # Creates a field with GosperGliderGun in top left bottom
                    self.seed_field.create_gosper_glider_gun_field()
                elif event.key == pygame.K_r:  # Randomize the field
                    self.seed_field.create()
                elif event.key == pygame.K_q:  # Quit the game
                    self.quit = True
            elif event.type == pygame.QUIT:
                sys.exit()

    def start(self):
        while True:
            if self.quit:
                return
            self.press_buttons()
            self.print()
            if self.pause:
                continue
            self.next_field()
            self.print()


if __name__ == '__main__':
    game = Game()
    game.start()
