import pygame
import sys
from random import randint
from time import sleep
from pygame.locals import *


pygame.init()

x_screen_width = int(600)
y_screen_height = int(600)
block_size = int(9)

speed = 0.07

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((x_screen_width, y_screen_height), 0, 24)

alive_color = pygame.Color(WHITE)
pending_color = pygame.Color(BLACK)

random_lower_constraint = 1 * block_size
random_upper_constraint = 6 * block_size


def evolve_cell(alive: bool, friends: int):
    return friends == 3 or (alive and friends == 2)


def count_friends(grid: list, position):
    x, y = position
    friend_cells = [(x-1, y-1), (x-1, y), (x-1, y+1),
                    (x, y-1), (x, y+1),
                    (x+1, y-1), (x+1, y), (x+1, y+1)]

    count = 0
    for x, y in friend_cells:
        if x >= 0 and y >= 0:
            try:
                count += grid[x][y]
            except:
                pass
    return count


def make_grid(x: int, y: int, randomize: bool):
    grid = []
    for row_x in range(x):
        row = []
        for col_y in range(y):
            fits_constraints = row_x > random_lower_constraint and row_x < random_upper_constraint and col_y > random_lower_constraint and col_y < random_upper_constraint
            row.append(randint(0, 1) if randomize and fits_constraints else 0)
        grid.append(row)
    return grid


def evolve(world: list):
    x_len = len(world)
    y_len = len(world[0])
    new_grid = make_grid(x_len, y_len, False)
    for row_x in range(x_len):
        for col_y in range(y_len):
            cell = world[row_x][col_y]
            friends = count_friends(world, (row_x, col_y))
            new_grid[row_x][col_y] = 1 if evolve_cell(cell, friends) else 0
    return new_grid


def draw_block(x: int, y: int, color: Color):
    x *= block_size
    y *= block_size
    center = ((x + (block_size//2)), (y + (block_size//2)))
    pygame.draw.circle(screen, color, center, block_size // 2, 0)


def main():
    h = 0
    alive_color.hsva = [h, 100, 100]
    world = make_grid(x_screen_width // block_size,
                      y_screen_height // block_size, True)
    while True:
        for event in pygame.event.get():
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 1):
                    world = make_grid(x_screen_width // block_size,
                                      y_screen_height // block_size, True)
            if(event.type == pygame.KEYDOWN or event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
        for x in range(x_screen_width // block_size):
            for y in range(y_screen_height // block_size):
                cell_color = alive_color if world[x][y] else pending_color
                draw_block(x, y, cell_color)
        pygame.display.flip()
        h = (h + 2) % 360
        alive_color.hsva = (h, 100, 100)
        world = evolve(world)
        sleep(speed)


if __name__ == '__main__':
    main()
