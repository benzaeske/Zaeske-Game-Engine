import sys
import time
from typing import Tuple

import pygame
from pygame import Vector2, Surface
from pygame.key import ScancodeWrapper
from pygame.time import Clock

from model.entities.jellyfish.jellyfishspawner import JellyfishSpawner
from model.entities.school.school import School
from model.player.player import Turtle
from model.world.world import SpatialPartitioningModel
from view.view import View


class ControllerOptions:
    """
    :param world_width: The size of the world model. This must be divisible by the grid cell size
    :param world_height: The size of the world model. This must be divisible by the grid cell size
    :param grid_cell_size: The map will be divided into grids of this size. In order for schooling to work properly, this must be at least as large as the smallest coherence radius of the fish being
    """

    def __init__(
        self,
        world_width: float,
        world_height: float,
        grid_cell_size: float,
    ) -> None:
        self.world_width: float = world_width
        self.world_height: float = world_height
        self.grid_cell_size: float = grid_cell_size


class GameController:
    """
    Orchestration class for running the current state of the game. Contains a model which is the simulated world, a view that is responsible for drawing on the screen,
    and a 'player' that is essentially a camera that can be moved around the world using WASD and has dimensions equal to the screen size used.\n
    The model tracks coordinates using a standard 2-dimensional x, y plane with (0,0) being the bottom left of the map.
    The view is currently implemented using pygame which draws to the screen on an inverted y-axis, so coordinates must be converted when coming from the model\n
    The world model can be any arbitrary size as long as it is bigger than the screen size. The entire world model is updated each frame, but only the grid cells within the player's 'camera' range are drawn each frame
    """

    def __init__(
        self,
        options: ControllerOptions,
    ) -> None:
        pygame.init()
        self.view: View = View()
        self.model: SpatialPartitioningModel = SpatialPartitioningModel(
            options.world_width,
            options.world_height,
            options.grid_cell_size,
            Turtle(
                self.view.screen_width,
                self.view.screen_height,
                (options.world_width, options.world_height),
            ),
        )
        self.clock: Clock = pygame.time.Clock()
        self.fps: int = 60
        self.game_start: float = -1
        self.dt: float = 0.0
        # Used to trigger logging when dt exceeds the max value required for 60fps
        self.max_dt: float = 0.017
        # Tracking player inputs
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.key_presses: ScancodeWrapper = ScancodeWrapper(())

    def start_game(self):
        self.game_start = time.time()
        self.model.hatch_schools()
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        self.key_presses = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.check_for_terminate()
        model_update_time = time.time()
        self.update_model()
        model_update_time = time.time() - model_update_time
        view_update_time = time.time()
        self.draw_background()
        #self.draw_fps_menu()
        self.draw_game_entities()
        self.view.update_screen()
        view_update_time = time.time() - view_update_time
        self.fps_logging(model_update_time, view_update_time)
        self.dt = self.clock.tick(self.fps) / 1000

    def check_for_terminate(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if self.key_presses[pygame.K_ESCAPE]:
            sys.exit()

    def update_model(self) -> None:
        self.model.update_model(self.dt, self.key_presses)

    def draw_background(self) -> None:
        for grid_cell in self.model.get_grid_cells_in_camera_range():
            self.view.draw_surface(
                grid_cell.background_surface,
                self.convert_model_pos_to_view_pos(
                    grid_cell.center_pos, grid_cell.background_surface
                ),
            )

    def draw_fps_menu(self) -> None:
        self.view.print_info_to_screen(
            self.clock.get_fps(),
            int(self.model.player.position.x),
            int(self.model.player.position.y),
        )

    def draw_game_entities(self) -> None:
        for fish in self.model.fish.values():
            fish_surface = fish.get_surface()
            self.view.draw_surface(fish_surface, self.convert_model_pos_to_view_pos(fish.position, fish_surface))
        for jelly in self.model.jellyfish.values():
            jelly_surface = jelly.get_surface()
            self.view.draw_surface(jelly_surface, self.convert_model_pos_to_view_pos(jelly.position, jelly_surface))
        self.view.draw_surface(
            self.model.player.get_surface(),
            self.model.player.get_camera_adjusted_position(),
        )

    def convert_model_pos_to_view_pos(
        self, model_pos: Vector2, blit_surface: Surface
    ) -> Tuple[float, float]:
        camera_pos = self.model.player.position
        camera_w = self.model.player.camera_width
        camera_h = self.model.player.camera_height
        # Find the center of my object in pygame view space (inverted y-axis). 0,0 is top left corner
        view_center_x = model_pos.x - (camera_pos.x - camera_w / 2)
        view_center_y = (camera_pos.y + camera_h / 2) - model_pos.y
        # Adjust to the top left corner of the object
        view_x = view_center_x - blit_surface.get_width() / 2
        view_y = view_center_y - blit_surface.get_height() / 2
        return view_x, view_y

    def add_school(self, school: School) -> None:
        self.model.add_school(school)

    def set_jellyfish_spawner(self, spawner: JellyfishSpawner) -> None:
        self.model.set_jellyfish_spawner(spawner)

    def fps_logging(self, model_t: float, view_t: float) -> None:
        if self.dt > self.max_dt:
            print(
                "Frame dt was too slow to meet",
                self.fps,
                "fps. dt:",
                self.dt,
                "\nModel update time ms:",
                model_t,
                "\nView update time ms:",
                view_t,
                "\n",
            )
