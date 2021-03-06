import pygame
import sys
import numpy as np
import time

pygame.init()

# Numeric constants
WIDTH = 600
HEIGHT = 600
BOARD_ROWS = 3
BOARD_COLS = 3
FACTOR_X = WIDTH//BOARD_COLS
FACTOR_Y = HEIGHT//BOARD_ROWS
LINE_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 50
VICTORY_LINE_WIDTH = 10

# Color constants
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC TAC TOE')

def draw_lines():
    # horizontal
    pygame.draw.line(screen, LINE_COLOR, (200, 10), (200, 590), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 10), (400, 590), LINE_WIDTH)
    # vertical
    pygame.draw.line(screen, LINE_COLOR, (10, 200), (590, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (10, 400), (590, 400), LINE_WIDTH)


def mark_square(row, col, player_num):
    board[row][col] = player_num


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row,col):
                return False
    return True


def translate_coordinate_x(x):
    col_width = WIDTH//BOARD_COLS
    index = x//col_width
    if index > 2:
        return 2
    return index


def translate_coordinate_y(y):
    row_height = HEIGHT//BOARD_ROWS
    index = y//row_height
    if index > 2:
        return 2
    return index


def draw_figure(row,col,player_num):
    if player_num == 1:
        x = int(col * FACTOR_Y + FACTOR_Y//2)
        y = int(row * FACTOR_X + FACTOR_X//2)
        pygame.draw.circle(screen, CIRCLE_COLOR, (x,y), CIRCLE_RADIUS, CIRCLE_WIDTH)
    else:
        x1 = col * FACTOR_X + SPACE
        x2 = col * FACTOR_X + FACTOR_X - SPACE
        y1 = row * FACTOR_Y + SPACE
        y2 = row * FACTOR_Y + FACTOR_Y - SPACE
        pygame.draw.line(screen, CROSS_COLOR, (x1,y1), (x2,y2), CROSS_WIDTH)
        x1 = col * FACTOR_X + FACTOR_X - SPACE
        x2 = col * FACTOR_X + SPACE
        y1 = row * FACTOR_Y + SPACE
        y2 = row * FACTOR_Y + FACTOR_Y - SPACE
        pygame.draw.line(screen, CROSS_COLOR, (x1, y1), (x2, y2), CROSS_WIDTH)


def draw_victory_line(col1, row1, col2, row2):
    x1 = int(col1 * FACTOR_X + FACTOR_X//2)
    x2 = int(col2 * FACTOR_X + FACTOR_X//2)
    y1 = int(row1 * FACTOR_Y + FACTOR_Y//2)
    y2 = int(row2 * FACTOR_Y + FACTOR_Y//2)
    pygame.draw.line(screen, RED, (x1,y1),(x2,y2), VICTORY_LINE_WIDTH)



def is_player_won(player_num):
    # vertical
    for col in range(BOARD_COLS):
        if board[0][col] == player_num and board[1][col] == player_num and board[2][col] == player_num:
            draw_victory_line(col, 0, col, 2)
            return True

    # horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == player_num and board[row][1] == player_num and board[row][2] == player_num:
            draw_victory_line(0, row, 2, row)
            return True

    # left-to-right diagonal
    if board[0][0] == player_num and board[1][1] == player_num and board[2][2] == player_num:
        draw_victory_line(0, 0, 2, 2)
        return True

    # right-to-left diagonal
    if board[2][0] == player_num and board[1][1] == player_num and board[0][2] == player_num:
        draw_victory_line(2, 0, 0, 2)
        return True

    return False


def init():
    screen.fill(BG_COLOR)

    draw_lines()

    # board
    return np.zeros((BOARD_ROWS, BOARD_COLS))


def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    player_number = 1
    game_over = False
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


board = init()


player_number = 1
game_over = False

# mainloop
while True:
    # Handle events
    for event in pygame.event.get():
        # Exit event
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_col = translate_coordinate_x(mouseX)
            clicked_row = translate_coordinate_y(mouseY)

            # the square is available
            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row,clicked_col, player_number)
                draw_figure(clicked_row,clicked_col,player_number)

                if is_player_won(player_number):
                    game_over = True
                    board = restart()
                    continue

                # change player
                if player_number == 1:
                    player_number = 2
                else:
                    player_number = 1

                print(board)



    pygame.display.update()
