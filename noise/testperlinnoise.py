import random
import sys

import noise
import pygame

from perlin_numpy import generate_perlin_noise_2d
from pygame import Surface
from pygame.time import Clock

def attempt_1():
    pygame.init()

    grid_square_dimension: float = 8.0
    grid_width: int = 128
    grid_height: int = 128

    screen = pygame.display.set_mode((grid_width * grid_square_dimension, grid_height * grid_square_dimension))
    screen.fill((0, 0, 0))
    pygame.display.update()
    pygame.display.set_caption("Perlin Noise")

    noise_array = generate_perlin_noise_2d((grid_width, grid_height), (2, 2))
    background_tiles = [[Surface((grid_square_dimension, grid_square_dimension)) for x in range(grid_width)] for y in
                        range(grid_height)]
    for row in range(grid_height):
        for col in range(grid_width):
            noise = int(noise_array[row][col] * 50)
            background_tiles[row][col].fill((0, 50 + noise, 140 + (noise * 2)))

    clock: Clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for row in range(grid_height):
            for col in range(grid_width):
                screen.blit(background_tiles[row][col], (grid_square_dimension * col, grid_square_dimension * row))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

def attempt_2():
    octaves = 2  # Number of layers of detail
    persistence = 0.5  # How much each octave contributes to the overall shape (amplitude)
    lacunarity = 2.0  # How much detail is added at each octave (frequency)

    pygame.init()

    grid_square_dimension: float = 8.0
    grid_width: int = 128
    grid_height: int = 128

    screen = pygame.display.set_mode((grid_width * grid_square_dimension, grid_height * grid_square_dimension))
    screen.fill((0, 0, 0))
    pygame.display.update()
    pygame.display.set_caption("Perlin Noise")

    background_tiles = [[Surface((grid_square_dimension, grid_square_dimension)) for x in range(grid_width)] for y in
                        range(grid_height)]
    for y in range(grid_height):
        for x in range(grid_width):
            n = noise.pnoise2((x / grid_width) - 0.5, (y / grid_height) - 0.5, base=base, repeatx=grid_width)
            n = (n / 2) + 0.5
            n = n * 255
            background_tiles[y][x].fill((0, 0, n))

    clock: Clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for y in range(grid_height):
            for x in range(grid_width):
                screen.blit(background_tiles[y][x], (grid_square_dimension * x, grid_square_dimension * y))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

attempt_2()