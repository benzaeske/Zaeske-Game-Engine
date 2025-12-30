import random
import time

import pygame
from perlin_noise import PerlinNoise
from perlin_numpy import generate_perlin_noise_2d
from pygame import Surface
from pygame.time import Clock

grid_square_dimension: float = 8.0
grid_width: int = 128
grid_height: int = 128


def initialize_noise_grid() -> list[list[Surface]]:
    return [
        [
            Surface((grid_square_dimension, grid_square_dimension))
            for _ in range(grid_width)
        ]
        for _ in range(grid_height)
    ]


def attempt_1() -> list[list[Surface]]:
    noise_array = generate_perlin_noise_2d((grid_width, grid_height), (2, 2))
    background_tiles = initialize_noise_grid()
    for row in range(grid_height):
        for col in range(grid_width):
            noise = int(noise_array[row][col] * 50)
            background_tiles[row][col].fill((0, 50 + noise, 140 + (noise * 2)))
    return background_tiles


def attempt_2() -> list[list[Surface]]:
    seed: int = random.randint(1, 10**5)
    # Inputs
    octaves: int = 1

    # Instantiate noise generator
    noise_generator: PerlinNoise = PerlinNoise(octaves, seed)
    print("generator created with seed:", noise_generator.seed)

    background_tiles: list[list[Surface]] = initialize_noise_grid()

    min_noise: float = 1
    max_noise: float = -1
    # Loop and create tiles
    for y in range(grid_height):
        for x in range(grid_width):
            nx = x / grid_height
            ny = y / grid_width
            noise = noise_generator.noise((nx, ny))
            min_noise = min(noise, min_noise)
            max_noise = max(noise, max_noise)
            """
            noise = (noise / 2) + 0.5
            noise = noise * noise
            noise = noise * 255
            noise = 255 if noise < 0 else 1
            """
            noise = noise * 127
            background_tiles[y][x].fill((0, 30, 127 + (noise * 1)))
    print("min:", min_noise)
    print("max:", max_noise)

    return background_tiles


def main():
    # Load
    generation_load_time: float = time.time()
    background_tiles: list[list[Surface]] = attempt_2()
    generation_load_time = time.time() - generation_load_time
    print("noise generation load time (seconds):", generation_load_time)
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode(
        (grid_width * grid_square_dimension, grid_height * grid_square_dimension)
    )
    pygame.display.set_caption("Perlin Noise")
    clock: Clock = pygame.time.Clock()
    running = True
    # Draw loop
    while running:
        # Check for terminate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        # Draw noise
        draw_time: float = time.time()
        for row in range(grid_height):
            for col in range(grid_width):
                screen.blit(
                    background_tiles[row][col],
                    (grid_square_dimension * col, grid_square_dimension * row),
                )
        pygame.display.flip()
        draw_time = time.time() - draw_time
        print("noise draw time (seconds):", draw_time)
        clock.tick(30)


main()
