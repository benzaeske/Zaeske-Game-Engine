import copy
import math
from typing import Tuple

import pygame
from pygame import Surface, Font, Rect

from model.player.camera import Camera
from view.background import Background


class WindowOptions:
    def __init__(self, screen_width: int = None, screen_height: int = None, full_screen: bool = False) -> None:
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.full_screen: bool = full_screen
        # If nothing is passed in, default to full screen
        if self.screen_width is None and self.screen_height is None:
            self.full_screen: bool = True

class View:
    """
    The View is responsible for drawing everything on the screen using pygame functions, but should know nothing about the size or shape of the model it is drawing.\n
    Pygame uses an inverted y-axis which is why coordinates are being converted when coming from the model.
    """

    def __init__(self, options: WindowOptions) -> None:
        self._options: WindowOptions = options
        # Screen sizing
        display_info = pygame.display.Info()
        # Width the display being used as detected by pygame's built in display Info class
        self._display_width: int = display_info.current_w
        self._display_height: int = display_info.current_h
        # The screen that will be used to blit each frame
        self._screen: Surface = self._initialize_screen()
        # Get dimensions from created screen
        self._screen_width: int = self._screen.get_width()
        self._screen_height: int = self._screen.get_height()
        # Font
        self._font: Font = pygame.font.SysFont("Arial", 48)
        print(
            "Initialized view with pygame screen Surface dimensions: ",
            self._screen_width,
            self._screen_height,
        )
        self._background: Background = Background((64, 64), 128)

    def _initialize_screen(self) -> Surface:
        """
        Get the screen that will be used for displaying the game
        """
        if self._options.full_screen:
            return pygame.display.set_mode((self._display_width, self._display_height), pygame.FULLSCREEN)
        else:
            # Don't let the width/height exceed the maximum dimensions of the current display
            width: int = self._options.screen_width if self._options.screen_width is not None and self._options.screen_width < self._display_width else self._display_width
            height: int = self._options.screen_height if self._options.screen_height is not None and self._options.screen_height < self._display_height else self._display_height
            return pygame.display.set_mode((width, height))

    def get_screen(self) -> Surface:
        return self._screen

    def get_screen_width(self) -> int:
        return self._screen_width

    def get_screen_height(self) -> int:
        return self._screen_height

    def draw_background(self, camera: Camera) -> None:
        # Pull out some constants for readability
        tile_size: int = self._background.get_tile_size()
        background_width: int = self._background.get_background_dimensions()[0]
        background_height: int = self._background.get_background_dimensions()[1]

        # Adjust camera window center so that it is at its relative position inside the background
        camera_window: Rect = copy.deepcopy(camera.get_window())
        camera_window.center = (
            ((camera_window.centerx % background_width) + background_width) % background_width,
            ((camera_window.centery % background_height) + background_height) % background_height
        )

        # Define the left/right/bottom/top ranges of tiles to draw
        left: int = int(camera_window.left // tile_size)
        right: int = int(camera_window.right // tile_size)
        bottom: int = int(camera_window.top // tile_size) # Pygame Rects use inverted y
        top: int = int(camera_window.bottom // tile_size) # Pygame Rects use inverted y
        # Loop through and draw the tiles
        for row in range(bottom, top + 1):
            for col in range(left, right + 1):
                grid_r = (row + background_height) % background_height
                grid_c = (col + background_width) % background_width
                # Convert top left of row, col to coordinates on the background surface
                x = col * tile_size
                y = (row + 1) * tile_size
                # Adjust to screen relative coordinates
                x = x - camera_window.left
                y = camera_window.bottom - y # Pygame Rects use inverted y
                self.draw_surface(self._background.get_background_tile(grid_r, grid_c), (x, y))

    def draw_surface(self, surface: Surface, dest: Tuple[float, float], area: Tuple[float, float, float, float] | None = None) -> None:
        self._screen.blit(surface, dest, area)

    def print_fps_to_screen(self, fps: float, player_x: int, player_y: int) -> None:
        fps_surface: Surface = self._font.render(
            str(math.floor(fps)), True, (255, 255, 255)
        )
        self._screen.blit(fps_surface, fps_surface.get_rect(x=0, y=0))

    def print_location_to_screen(self, player_x: int, player_y: int) -> None:
        x_surface: Surface = self._font.render(
            "x: " + str(player_x), True, (255, 255, 255)
        )
        self._screen.blit(x_surface, x_surface.get_rect(x=0, y=fps_surface.get_height()))
        y_surface: Surface = self._font.render(
            "y: " + str(player_y), True, (255, 255, 255)
        )
        self._screen.blit(
            y_surface,
            y_surface.get_rect(
                x=0, y=fps_surface.get_height() + x_surface.get_height()
            ),
        )

    def print_score_to_screen(self, score: int | None) -> None:
        if score is None:
            score = 0
        score_surface: Surface = self._font.render("Score: " + str(score), True, (255, 255, 255))
        self._screen.blit(score_surface, score_surface.get_rect(x=0, y=0))


    @staticmethod
    def update_screen() -> None:
        pygame.display.update()
