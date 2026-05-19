import pygame
from enum import Enum

# Константы
WIDTH = 10
HEIGHT = 20
QUALITY = 30

BG_COLOR = pygame.Color(69, 69, 69)
PIECE_COLOR = pygame.Color(255, 255, 255)

NORMAL_DROP_DELAY = 800
NORMAL_MOVE_DELAY = 500
FAST_DROP_DELAY = 50

# Игровые переменные
running = True
cup = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
current_drop_delay = NORMAL_DROP_DELAY
move_time = 0
fall_time = 0

# Enums
class PieceForm(Enum):
    J: list[int] = [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]
    L: list[int] = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ]
    T: list[int] = [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ]
    O: list[int] = [
        [1, 1],
        [1, 1]
    ]

class Piece:
    def __init__(self, form: PieceForm) -> None:
        self.form: list[int] = form.value
        self.x = (WIDTH-len(self.form))//2
        self.y = 0
     
    def draw(self) -> None:
        for piece_y in range(len(self.form)):
            for piece_x in range(len(self.form[piece_y])):
                if self.form[piece_y][piece_x] != 0:
                    cup_y = piece_y + self.y
                    cup_x = piece_x + self.x
                    cup[cup_y][cup_x] = self.form[piece_y][piece_x]
    
    def erase(self) -> None:
        for piece_y in range(len(self.form)):
            for piece_x in range(len(self.form[piece_y])):
                if self.form[piece_y][piece_x] != 0:
                    cup_y = piece_y + self.y
                    cup_x = piece_x + self.x
                    if 0 <= cup_y < HEIGHT and 0 <= cup_x < WIDTH:
                        cup[cup_y][cup_x] = 0
    
    def move(self, right: int, bottom: int) -> None:
        self.erase()
        self.x += right
        self.y += bottom
        self.draw()
    
    def check_collision(self, next_x: int = None, next_y: int = None) -> bool:
        target_x = next_x if next_x else self.x
        target_y = next_y if next_y else self.y
        for piece_y in range(len(self.form)):
            for piece_x in range(len(self.form[piece_y])):
                if self.form[piece_y][piece_x] != 0:
                    cup_y = piece_y + target_y
                    cup_x = piece_x + target_x

                    if cup_x < 0 or cup_x >= WIDTH or cup_y >= HEIGHT:
                        return True
                    
                    if cup_y >= 0 and cup[cup_y][cup_x] != 0:
                        return True
        return False

pygame.init()
screen = pygame.display.set_mode((QUALITY*WIDTH, QUALITY*HEIGHT))
clock = pygame.time.Clock()

piece = Piece(form=PieceForm.L)
piece.draw()

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                current_drop_delay = FAST_DROP_DELAY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                current_drop_delay = NORMAL_DROP_DELAY

    screen.fill(BG_COLOR)

    keys = pygame.key.get_pressed()
    move_time += dt
    if move_time >= NORMAL_MOVE_DELAY:
        if keys[pygame.K_LEFT]:
            piece.move(-1, 0)
        elif keys[pygame.K_RIGHT]:
            piece.move(1, 0)

        move_time = 0

    fall_time += dt
    if fall_time >= current_drop_delay:
        piece.erase()

        if piece.check_collision(piece.x, piece.y+1):
            piece.draw()
            piece = Piece(PieceForm.T)
            if piece.check_collision():
                print("GAME OVER!!!")
                running = False
        else:
            piece.y += 1
        piece.draw()
        # piece.move(0, 1)
        fall_time = 0

    for y_offset, row in enumerate(cup):
        for x_offset, column in enumerate(row):
            if column != 0:
                rect = pygame.Rect(x_offset*QUALITY, y_offset*QUALITY, QUALITY, QUALITY)
                pygame.draw.rect(screen, PIECE_COLOR, rect=rect)

    pygame.display.flip()

pygame.quit()
    