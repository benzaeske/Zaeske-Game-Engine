import copy
from typing import Tuple

from perlin_numpy import generate_perlin_noise_2d
from pygame import Surface, Rect

from model.player.camera import Camera

TILE_SIZE: int = 64
GRID_WIDTH: int = 128
GRID_HEIGHT: int = 128
NOISE_RESOLUTION: Tuple[int, int] = (8, 8)

class Background:
    def __init__(self, display_w: int, display_h: int) -> None:  # (width, height) of the tile grid
        self._grid_width: int = GRID_WIDTH
        self._grid_height: int = GRID_HEIGHT
        self._tile_size: int = TILE_SIZE
        self._noise_resolution: Tuple[int, int] = NOISE_RESOLUTION

        self._background_width: int = self._grid_width * self._tile_size # The total width of all the background tiles
        self._background_height: int = self._grid_height * self._tile_size # The total height of all the background tiles
        self._display_w: int = display_w  # The maximum width of the current display
        self._display_h: int = display_h  # The maximum height of the current display

        # Number of padding cells needed to surround the surface
        self._pad_cells_x: int = int(self._display_w / 2) // self._tile_size
        self._pad_cells_y: int = int(self._display_h / 2) // self._tile_size
        self._pad_width: int = self._pad_cells_x * self._tile_size
        self._pad_height: int = self._pad_cells_y * self._tile_size
        self._height_with_padding: int = self._background_height + (2 * self._pad_height)

        self._background_surface: Surface = self.prepare_background_surface()

    def prepare_background_surface(self) -> Surface:
        """
        The background surface is padded in positive and negative x/y directions with extra cells that get their
        values by wrapping around the tile grid. This ensures the correct tiles are shown when a camera position
        is requested that has an edge that extends over the surface.
        """
        tiles: list[list[Surface]] = self._get_perlin_noise_colored_tiles()

        # Initialize the surface with dimensions that include the padding cells
        bg_w: int = ((self._pad_cells_x * 2) + self._grid_width) * self._tile_size
        bg_h: int = ((self._pad_cells_y * 2) + self._grid_height) * self._tile_size
        bg: Surface = Surface((bg_w, bg_h)).convert_alpha()

        for row in range(-self._pad_cells_y, self._grid_height + self._pad_cells_y):
            for col in range(-self._pad_cells_x, self._grid_width + self._pad_cells_x):
                # Get the row/col wrapped onto the tile grid
                wrap_row: int = (row + self._grid_height) % self._grid_height
                wrap_col: int = (col + self._grid_width) % self._grid_width
                # Convert top left of row, col to coordinates on the background surface
                x = (col + self._pad_cells_x) * self._tile_size
                y = (row + self._pad_cells_y) * self._tile_size
                # Blit the tile onto the background surface
                bg.blit(tiles[wrap_row][wrap_col], (x, y))

        return bg

    def _get_perlin_noise_colored_tiles(self) -> list[list[Surface]]:
        """
        Create a 2d array with grid_width * grid_height square tiles of size tile_size colored using perlin noise
        """
        tiles: list[list[Surface]] = self._initialize_tiles()
        noise_array = generate_perlin_noise_2d((self._grid_width, self._grid_height), self._noise_resolution, (True, True))
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                tiles[row][col].fill(self._get_color_from_noise(noise_array[row][col]))
        return tiles

    @staticmethod
    def _get_color_from_noise(noise: float) -> Tuple[int, int, int]:
        scaled_noise: int = int(noise * 64)
        return 0, 64 + int(scaled_noise/4), 191 + scaled_noise

    def _initialize_tiles(self) -> list[list[Surface]]:
        return [
            [
                Surface((self._tile_size, self._tile_size)).convert_alpha() for _ in range(self._grid_width)
            ] for _ in range(self._grid_height)
        ]

    def draw(self, screen: Surface, camera: Camera) -> None:
        # Wrap the camera's position onto the background surface
        camera_window: Rect = copy.deepcopy(camera.get_window())
        camera_window.center = (
            ((camera_window.centerx % self._background_width) + self._background_width) % self._background_width,
            ((camera_window.centery % self._background_height) + self._background_height) % self._background_height
        )
        # Add padding offset
        camera_window.center = (
            camera_window.centerx + self._pad_width,
            self._height_with_padding - (camera_window.centery + self._pad_height) # Pygame uses an inverted y-axis
        )
        # Draw onto the screen
        screen.blit(self._background_surface, (0, 0), camera_window)