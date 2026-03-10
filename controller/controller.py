import sys
import time
from typing import Tuple
from uuid import UUID

import pygame
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.time import Clock

from model.entitymanagers.entitymanager import EntityManager
from model.player.player import Player
from model.player.turtle import Turtle
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.gridspace.grid_cell import GridCell
from model.world.model import Model
from view.background import BackgroundOptions
from view.view import View, WindowOptions


class ControllerOptions:
    def __init__(
        self,
        window_options: WindowOptions,
        background_options: BackgroundOptions,
    ) -> None:
        self.window_options: WindowOptions = window_options
        self.background_options: BackgroundOptions = background_options


class GameController:
    def __init__(
        self,
        options: ControllerOptions,
    ) -> None:
        pygame.init()
        self._options: ControllerOptions = options
        self._view: View = View(self._options.window_options, self._options.background_options)
        self._player: Player = Turtle(self._view.get_screen_width(), self._view.get_screen_height())
        self._model: Model = Model(
            128.0,
            self._player
        )
        self._clock: Clock = pygame.time.Clock()
        self._fps: int = 60
        self._game_start_time: float = -1
        self._dt: float = 0.0
        # Used to trigger logging when dt exceeds the max value required for 60fps
        self._max_dt: float = 0.017
        # Tracking player inputs
        self._mouse_pos: Tuple[int, int] = (0, 0)
        self._key_presses: ScancodeWrapper = ScancodeWrapper(())
        # All input 'events' such as keypresses etc.
        # Pygame allows us to get the list of events once and then clears the event queue so we need to store them each frame
        self._current_frame_input_events: list[Event] = []
        self._paused: bool = False
        self._score: int = 0

    def start_game(self):
        self._game_start_time = time.time()
        # TODO State machine for different display loops
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        self._key_presses = pygame.key.get_pressed()
        self._mouse_pos = pygame.mouse.get_pos()
        self._current_frame_input_events = pygame.event.get()
        self.check_for_terminate()
        self.check_for_pause()
        if not self._paused:
            model_update_time = time.time()
            self.update_model()
            model_update_time = time.time() - model_update_time
            view_update_time = time.time()
            self.draw()

            self._view.update_screen()
            view_update_time = time.time() - view_update_time
            self.fps_logging(model_update_time, view_update_time)
        self._dt = self._clock.tick(self._fps) / 1000

    def check_for_terminate(self):
        for event in self._current_frame_input_events:
            if event.type == pygame.QUIT:
                sys.exit()
        if self._key_presses[pygame.K_ESCAPE]:
            sys.exit()
        if self._player.get_current_hp() <= 0.0:
            sys.exit()

    def check_for_pause(self):
        for event in self._current_frame_input_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._paused = not self._paused

    def update_model(self) -> None:
        self._model.update(self._key_presses, self._dt)

    def draw(self) -> None:
        self.draw_background()
        camera_grid_cells: list[GridCell] = (self._model.get_grid_space()
                                             .get_grid_cells_in_camera_range(self._player.get_camera()))
        # Draw in a specified order:
        #  1. fish
        self.draw_entities(camera_grid_cells, EntityManagerIndex.FISH)
        #  2. items
        self.draw_entities(camera_grid_cells, EntityManagerIndex.ITEM)
        #  3. player
        self._player.draw(self._view.get_screen())
        #  4. enemies
        self.draw_entities(camera_grid_cells, EntityManagerIndex.ENEMY)
        #  5. projectiles
        self.draw_entities(camera_grid_cells, EntityManagerIndex.PROJECTILE)

    def draw_background(self) -> None:
        self._view.draw_background(self._player.get_camera())

    def draw_entities(self, grid_cells: list[GridCell], entity_type: EntityManagerIndex) -> None:
        """
        Draws all entities of a given type found in the provided grid cells
        :param grid_cells: The grid cells containing entities to draw.
        :param entity_type: Only entities belonging to entity managers of this type will be drawn.
        """
        for grid_cell in grid_cells:
            for entity in grid_cell.get_entities_by_manager_ids(self._model.get_entity_repository().get_manager_ids(entity_type)):
                entity.draw(self._view.get_screen(), self._player.get_camera().get_window())

    def draw_fps_menu(self) -> None:
        self._view.print_info_to_screen(
            self._clock.get_fps(),
            int(self.model_v1.player.position.x),
            int(self.model_v1.player.position.y),
        )

    def draw_score(self) -> None:
        self._view.print_score_to_screen(self._score)

    def fps_logging(self, model_t: float, view_t: float) -> None:
        if self._dt > self._max_dt:
            print(
                "Frame dt was too slow to meet",
                self._fps,
                "fps. dt:",
                self._dt,
                "\nModel update time ms:",
                model_t,
                "\nView update time ms:",
                view_t,
                "\n",
            )

    def increment_score(self, n: int | None) -> None:
        self._score += n

    def add_entity_manager(self, entity_manager: EntityManager) -> None:
        self._model.add_entity_manager(entity_manager)

    def remove_entity_manager(self, manager_id: UUID) -> None:
        self._model.remove_entity_manager(manager_id)