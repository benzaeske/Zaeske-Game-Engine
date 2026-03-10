from typing import Tuple

from perlin_numpy import generate_perlin_noise_2d
from pygame import Surface


class Background:
    def __init__(self, grid_dimensions: Tuple[int, int], tile_size: int) -> None:
        self._grid_dimensions: Tuple[int, int] = grid_dimensions
        self._tile_size: int = tile_size
        self._background_dimensions: Tuple[int, int] = (grid_dimensions[0] * self._tile_size,
                                                                grid_dimensions[1] * self._tile_size)
        self._tiles: list[list[Surface]] = self._initialize_tiles()
        self._color_tiles_with_perlin_noise()

    def _initialize_tiles(self) -> list[list[Surface]]:
        return [
            [
                Surface((self._tile_size, self._tile_size)).convert_alpha() for _ in range(self._grid_dimensions[0])
            ] for _ in range(self._grid_dimensions[1])
        ]

    def _color_tiles_with_perlin_noise(self) -> None:
        resolution: Tuple[int, int] = (2, 2)
        noise_array = generate_perlin_noise_2d(self._grid_dimensions, resolution, (True, True))
        for row in range(self._grid_dimensions[1]):
            for col in range(self._grid_dimensions[0]):
                noise = int(noise_array[row][col] * 50)
                self._tiles[row][col].fill((0, 50 + noise, 140 + (noise * 2)))

    def get_background_tile(self, row: int, col: int) -> Surface:
        if row < 0 or row >= self._grid_dimensions[1] or col < 0 or col >= self._grid_dimensions[0]:
            raise ValueError(f"Invalid background tile coordinates: ({row}, {col})")
        return self._tiles[row][col]

    def get_tile_size(self) -> int:
        return self._tile_size

    def get_background_dimensions(self) -> Tuple[int, int]:
        return self._background_dimensions


