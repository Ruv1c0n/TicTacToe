import pygame
from pygame import Surface, SurfaceType

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
"""
Размеры 
    cell: клеточки
    spacer: разделителя
     window_size: окна
"""
cell = 150
spacer = 3
width = cell * 3 + spacer * 4
window_size = (width, width)


class Field:
    """
    цвет для отрисовки
    __color: клетки
    __bg_color: заднего фона(разделителя)
    __cross_color: крестика
    __circle_color: кружочка
    screen: экран
    playable_field: игровое поле
    """
    __color: tuple[int, int, int]
    __bg_color: tuple[int, int, int]
    __cross_color: tuple[int, int, int]
    __circle_color: tuple[int, int, int]
    screen: Surface | SurfaceType
    playable_field: list[list[int]]

    def __init__(self, _screen: pygame.surface) -> None:
        self.__color = WHITE
        self.__bg_color = BLACK
        self.__cross_color = BLUE
        self.__circle_color = RED
        self.screen = _screen
        self.playable_field = [[0] * 3 for _ in range(3)]

    # Отрисовывает начальное окно
    def draw(self) -> None:
        self.screen.fill(self.__bg_color)
        for row in range(3):
            for column in range(3):
                x = column * cell + (column + 1) * spacer
                y = row * cell + (row + 1) * spacer
                pygame.draw.rect(
                    self.screen, 
                    self.__color, 
                    (x, y, cell, cell)
                )
        pygame.display.update()

    # Отрисовывает обновленное окно
    def update(self) -> None:
        self.screen.fill(self.__bg_color)
        for row in range(3):
            for column in range(3):
                x = column * cell + (column + 1) * spacer
                y = row * cell + (row + 1) * spacer
                pygame.draw.rect(self.screen, self.__color, (x, y, cell, cell))
                if self.playable_field[row][column] == 'x':
                    pygame.draw.line(
                        self.screen, 
                        self.__cross_color,
                        (x, y), 
                        (x + cell, y + cell), 
                        3
                    )
                    pygame.draw.line(
                        self.screen, 
                        self.__cross_color, 
                        (x + cell, y), (x, y + cell), 
                        3
                    )
                elif self.playable_field[row][column] == 'o':
                    pygame.draw.circle(
                        self.screen, 
                        self.__circle_color, 
                        (x + cell // 2, y + cell // 2), 
                        cell // 2 - 3, 
                        3
                    )
        pygame.display.update()


class Control:
    field: Field
    player: int

    def __init__(self, _field: Field) -> None:
        self.field = _field
        self.player = 0

    def run(self, event, flag) -> None:
        if not flag and \
                event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            column = x_mouse // (cell + spacer)
            row = y_mouse // (cell + spacer)
            if self.field.playable_field[row][column] == 0:
                if not self.player:
                    self.field.playable_field[row][column] = 'x'
                else:
                    self.field.playable_field[row][column] = 'o'
                self.player = not self.player
                self.field.update()
        elif event.type == pygame.KEYDOWN and\
                event.key == pygame.K_r:
            self.field.playable_field = [[0] * 3 for _ in range(3)]
            self.player = 0
            self.field.draw()
            pygame.display.flip()


class Game:
    """"
     __screen: экран
    __running: флаг доступа к игре
    __field: игровое поле
    __control: управление
    """
    __screen: Surface | SurfaceType
    __running: bool
    __field: Field
    __control: Control

    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.__screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Tic Tac Toe")
        self.__running = True
        self.__field = Field(self.__screen)
        self.__control = Control(self.__field)

    # Основной метод игры
    def run(self) -> None:
        self.__field.draw()
        game_over = False
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                self.__control.run(event, game_over)
                if self.__control.player:
                    game_over = self.is_end_game('x')
                else:
                    game_over = self.is_end_game('o')
                if game_over:
                    self.__screen.fill(BLACK)
                    font = pygame.font.SysFont('TimesNewRoman', 80)
                    text1 = font.render("winner", True, WHITE)
                    text2 = font.render(game_over, True, WHITE)
                    text1_rect = text1.get_rect()
                    text1_coord = self.__screen.get_width() / 2 - text1_rect.width / 2
                    text2_rect = text2.get_rect()
                    text2_coord = self.__screen.get_width() / 2 - text2_rect.width / 2
                    if game_over != "Draw":
                        self.__screen.blit(text1, [text1_coord, text1_coord])
                    self.__screen.blit(text2, [text2_coord, text2_coord])
                    pygame.display.flip()

    # Проверяем на конец игры и возвращаем знак попедителя или False
    def is_end_game(self, sign) -> bool | str:
        empty = 0
        for row in self.__field.playable_field:
            empty += row.count(0)
            if row.count(sign) == 3:
                return sign
        for column in range(3):
            if self.__field.playable_field[0][column] == \
               self.__field.playable_field[1][column] == \
               self.__field.playable_field[2][column] == sign:
                return sign
            if self.__field.playable_field[0][0] == \
               self.__field.playable_field[2][2] == \
               self.__field.playable_field[1][1] == sign:
                return sign
            if self.__field.playable_field[0][2] == \
               self.__field.playable_field[2][0] == \
               self.__field.playable_field[1][1] == sign:
                return sign
        if not empty:
            return "Draw"
        return False


Game().run()
