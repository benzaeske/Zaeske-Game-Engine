import copy
from typing import Tuple

from perlin_numpy import generate_perlin_noise_2d
from pygame import Surface, Rect

from model.player.camera import Camera


class BackgroundOptions:
    def __init__(self, grid_dimensions: Tuple[int, int], tile_size: int):
        self.grid_dimensions: Tuple[int, int] = grid_dimensions
        self.tile_size: int = tile_size


class Background:
    def __init__(self, options: BackgroundOptions) -> None:
        self._grid_dimensions: Tuple[int, int] = options.grid_dimensions
        self._tile_size: int = options.tile_size
        self._background_dimensions: Tuple[int, int] = (self._grid_dimensions[0] * self._tile_size,
                                                                self._grid_dimensions[1] * self._tile_size)
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
                self._tiles[row][col].fill((0, 75 + (noise/2), 190 + noise))

    def get_background_tile(self, row: int, col: int) -> Surface:
        if row < 0 or row >= self._grid_dimensions[1] or col < 0 or col >= self._grid_dimensions[0]:
            raise ValueError(f"Invalid background tile coordinates: ({row}, {col})")
        return self._tiles[row][col]

    def get_tile_size(self) -> int:
        return self._tile_size

    def get_grid_dimensions(self) -> Tuple[int, int]:
        return self._grid_dimensions

    def get_background_dimensions(self) -> Tuple[int, int]:
        return self._background_dimensions

    def draw(self, screen: Surface, camera: Camera) -> None:
        # Adjust camera window center so that it is at its relative position inside the background
        camera_window: Rect = copy.deepcopy(camera.get_window())
        camera_window.center = (
            ((camera_window.centerx % self._background_dimensions[0]) + self._background_dimensions[0]) % self._background_dimensions[0],
            ((camera_window.centery % self._background_dimensions[1]) + self._background_dimensions[1]) % self._background_dimensions[1]
        )
        # Define the left/right/bottom/top ranges of tiles to draw
        left: int = int(camera_window.left // self._tile_size)
        right: int = int(camera_window.right // self._tile_size)
        bottom: int = int(camera_window.top // self._tile_size)  # Pygame Rects use inverted y
        top: int = int(camera_window.bottom // self._tile_size)  # Pygame Rects use inverted y
        # Loop through and draw the tiles
        for row in range(bottom, top + 1):
            for col in range(left, right + 1):
                grid_r = (row + self._grid_dimensions[1]) % self._grid_dimensions[1]
                grid_c = (col + self._grid_dimensions[0]) % self._grid_dimensions[0]
                # Convert top left of row, col to coordinates on the background surface
                x = col * self._tile_size
                y = (row + 1) * self._tile_size
                # Adjust to screen relative coordinates
                x = x - camera_window.left
                y = camera_window.bottom - y  # Pygame Rects use inverted y
                screen.blit(self.get_background_tile(grid_r, grid_c), (x, y))


