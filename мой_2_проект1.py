import sys
import pygame
import random
from itertools import product
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

start_time = None
the_best_time = 1000 ** 1000

# values
size = 500, 380
screen_width, screen_height = size
screen = pygame.display.set_mode(size)
board_w_number = 6
board_h_number = 5
fps = 30
box_reveal_speed = 8
box_size = 50
gap_size = 10
x_board = 70
y_board = 45

# shapes
shapes = ['square', 'triangle', 'circle']

# colors
red = pygame.Color(220, 0, 0)
green = pygame.Color(0, 210, 0)
yellow = pygame.Color('yellow')
cyan = pygame.Color(0, 150, 250)
magenta = pygame.Color('magenta')
bg_color = pygame.Color(10, 10, 40)
box_color = pygame.Color(150, 150, 255)
colors = [red, green, yellow, cyan, magenta]


def main():
    global start_time
    global screen, the_best_time

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('карточная игра на память')

    board = get_random_board()
    revealed = [[False] * board_w_number for i in range(board_h_number)]

    start_screen()

    mouse_x = 0
    mouse_y = 0
    mouse_clicked = False
    first_box = None

    running = True
    start_game_animation(board)
    start_time = pygame.time.get_ticks()

    while running:
        screen.fill(bg_color)
        draw_board(board, revealed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_clicked = True

        x, y = get_position(mouse_x, mouse_y)

        if x is not None and y is not None:
            if not revealed[x][y]:
                if mouse_clicked:
                    revealed[x][y] = True
                    draw_box(board, revealed, x, y)

                    if first_box is None:
                        first_box = (x, y)
                    else:
                        pygame.time.wait(1000)
                        if board[x][y] != board[first_box[0]][first_box[1]]:
                            revealed[x][y] = False
                            revealed[first_box[0]][first_box[1]] = False
                        first_box = None

                    if game_won(revealed):
                        time_since_start = pygame.time.get_ticks() - start_time
                        game_won_mig(board, revealed)
                        sec1 = time_since_start // 1000
                        min1 = sec1 // 60
                        sec1 -= min1 * 60
                        sec2 = the_best_time // 1000
                        min2 = sec2 // 60
                        sec2 -= min2 * 60
                        end_screen(True, (min1, sec1), (min2, sec2))
                        board = get_random_board()
                        revealed = [[False] * board_w_number for i in range(board_h_number)]
                        start_game_animation(board)

                else:
                    draw_selected_box(x, y)

        mouse_clicked = False
        pygame.display.update()
        pygame.time.Clock().tick(30)

    else:
        pygame.quit()
        quit()


# начало игры, показывам по пять рандомных карточек
def start_game_animation(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    coord = list(product(range(board_h_number), range(board_w_number)))
    random.shuffle(coord)

    revealed = [[False] * board_w_number for i in range(board_h_number)]

    screen.fill(bg_color)
    draw_board(board, revealed)
    pygame.display.update()
    pygame.time.wait(1000)

    for sz in range(0, board_h_number * board_w_number, 5):
        coord_list = coord[sz: sz + 5]
        for x in coord_list:
            revealed[x[0]][x[1]] = True
            draw_box(board, revealed, *x)
        pygame.time.wait(800)
        for x in coord_list:
            revealed[x[0]][x[1]] = False
            draw_box(board, revealed, *x)


# заставка при запуске
def start_screen():
    intro_text = ["  ПРАВИЛА", "",
                  "Нажимайте на карточки, которые,",
                  "по вашему, должны быть одинаковыми",
                  "(нажмите любую кнопку для начала)"]

    fon = pygame.image.load("fon.jpg").convert()
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(30)


# заставка при победе
def end_screen(value, now_record, best_record):
    now_min = str(now_record[0])
    now_sec = str(now_record[1])
    best_min = str(best_record[0])
    best_sec = str(best_record[1])

    lose_text = ["Вы открыли все карточки и одержали победу", '',
                 '    Время игры: ' + now_min + 'мин ' + now_sec + 'сек',
                 "    (нажмите любую кнопку для новой игры)"]

    fon = pygame.image.load("fon2.jpg").convert()
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in lose_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(30)


# проверка, все ли карточки открыты
def game_won(revealed):
    return all(all(x) for x in revealed)


# мигание доски при победе
def game_won_mig(board, revealed):
    color1 = box_color
    color2 = bg_color
    for i in range(10):
        color1, color2 = color2, color1
        screen.fill(color1)
        draw_board(board, revealed)
        pygame.display.update()
        pygame.time.wait(200)


# возвращает рандомно собранную доску
def get_random_board():
    icons = []
    for shape in shapes:
        for color in colors:
            icons.append((shape, color))
            icons.append((shape, color))
    random.shuffle(icons)

    board = [icons[i:i + screen_width]
             for i in range(0, board_h_number * board_w_number, board_w_number)]
    return board


def get_coord(x, y):
    top = x_board + y * (box_size + gap_size)
    left = y_board + x * (box_size + gap_size)
    return top, left


def get_position(cx, cy):
    if cx < x_board or cy < y_board:
        return None, None

    x = (cy - y_board) // (box_size + gap_size)
    y = (cx - x_board) // (box_size + gap_size)

    if x >= board_h_number or y >= board_w_number or (cx - x_board) % \
            (box_size + gap_size) > box_size or (cy - y_board) % \
            (box_size + gap_size) > box_size:
        return None, None
    else:
        return x, y


# отрисовка клетчатого поля
def draw_board(board, revealed):
    for x in range(board_w_number):
        for y in range(board_h_number):
            left = x * (box_size + gap_size) + x_board
            top = y * (box_size + gap_size) + y_board
            if not revealed[y][x]:
                pygame.draw.rect(screen, box_color, (left, top, box_size, box_size))
            else:
                draw_icon(board[y][x], y, x)


# отрисовка нужного квадратика
def draw_box(board, revealed, x, y):
    coord_x, coord_y = get_coord(x, y)[0], get_coord(x, y)[1]
    pygame.draw.rect(screen, bg_color, (coord_x, coord_y, box_size, box_size))
    if revealed[x][y]:
        draw_icon(board[x][y], x, y)
    else:
        pygame.draw.rect(screen, box_color, (coord_x, coord_y, box_size, box_size))
    pygame.display.update(coord_x, coord_y, box_size, box_size)


# рисует фигуру в назначенном месте
def draw_icon(icon, x, y):
    px, py = get_coord(x, y)

    if icon[0] == 'square':
        pygame.draw.rect(screen, icon[1],
                         (px + 5, py + 5, box_size - 10, box_size - 10))
    elif icon[0] == 'triangle':
        pygame.draw.polygon(screen, icon[1],
                            ((px + box_size // 2, py + 5), (px + 5, py + box_size - 5),
                             (px + box_size - 5, py + box_size - 5)))
    elif icon[0] == 'circle':
        pygame.draw.circle(screen, icon[1],
                           (px + box_size // 2, py + box_size // 2), box_size // 2 - 5)


# рисует серый ободочек вокруг выбранного квадрата
def draw_selected_box(x, y):
    x_x, y_y = get_coord(x, y)
    pygame.draw.rect(screen, Color('grey'), (x_x - 5, y_y - 5, box_size + 10, box_size + 10), 3)


if __name__ == '__main__':
    main()
