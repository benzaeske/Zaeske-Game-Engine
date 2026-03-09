import sys
import time
from typing import Tuple

import pygame
from pygame import Vector2
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.time import Clock

from model.entitymanagers.jellyfishswarm import JellyfishSwarm
from model.entitymanagers.school import School
from model.world.gridspace.grid_cell import GridCell
from model.world.model import Model
from model.world.worldspecs import WorldSpecs
from view.view import View, WindowOptions


class ControllerOptions:
    def __init__(
        self,
        world_specs: WorldSpecs,
        window_options: WindowOptions,
    ) -> None:
        self.world_specs: WorldSpecs = world_specs
        self.window_options: WindowOptions = window_options


class GameController:
    def __init__(
        self,
        options: ControllerOptions,
    ) -> None:
        pygame.init()
        self.options: ControllerOptions = options
        self.view: View = View(self.options.window_options)
        self.camera_specs: CameraSpecs = CameraSpecs(self.view.screen_width, self.view.screen_height)
        self.model: Model = Model(
            options.world_specs,
            Turtle(
                self.camera_specs,
                options.world_specs
            )
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
        # All input 'events' such as keypresses etc.
        # Pygame allows us to get the list of events once and then clears the event queue so we need to store them each frame
        self.current_frame_input_events: list[Event] = []
        self.paused: bool = False
        self.score: int = 0

    def start_game(self):
        self.game_start = time.time()
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        # TODO State machine for different display loops
        #  Pause menu. Display high score and current score. Options to resume or quit
        #  Display a score, save high score locally
        #  You died screen. Shows score, high score. Options to quit, play again
        self.key_presses = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.current_frame_input_events = pygame.event.get()
        self.check_for_terminate()
        self.check_for_pause()
        if not self.paused:
            model_update_time = time.time()
            self.update_model()
            model_update_time = time.time() - model_update_time
            view_update_time = time.time()
            self.draw_background()
            self.draw_game_entities()
            self.draw_player()
            # self.draw_fps_menu()
            self.draw_score()
            self.view.update_screen()
            view_update_time = time.time() - view_update_time
            self.fps_logging(model_update_time, view_update_time)
        self.dt = self.clock.tick(self.fps) / 1000

    def check_for_terminate(self):
        for event in self.current_frame_input_events:
            if event.type == pygame.QUIT:
                sys.exit()
        if self.key_presses[pygame.K_ESCAPE]:
            sys.exit()
        if self.model.get_player().health <= 0:
            sys.exit()

    def check_for_pause(self):
        for event in self.current_frame_input_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def update_model(self) -> None:
        self.model.update(self.key_presses, self.dt)

    def draw_background(self) -> None:
        # TODO Grid cell background matrix using perlin noise instead of storing background tiles in grid cell class
        # Loop over grid cells within camera range.
        cell_size: float = self.options.world_specs.cell_size
        left: int = int(
            self.model.get_player().camera.left // cell_size
        )
        right: int = int(
            self.model.get_player().camera.right // cell_size
        )
        bottom: int = int(
            self.model.get_player().camera.top // cell_size
        )
        top: int = int(
            self.model.get_player().camera.bottom // cell_size
        )
        for row in range(bottom, top + 1):
            for col in range(left, right + 1):
                # If the column overflows, wrap around to other side of the map
                grid_r = row
                grid_c = (
                    col + self.options.world_specs.grid_width
                ) % self.options.world_specs.grid_width
                # Convert top left of row, col to coords on the world map
                x = col * self.options.world_specs.cell_size
                y = (row + 1) * self.options.world_specs.cell_size
                # Adjust world map coords to screen relative coords
                x = x - self.model.get_player().camera.left
                y = self.model.get_player().camera.bottom - y
                self.view.draw_surface(
                    self.model._grid_space.get_grid_cell((grid_r, grid_c)).background_surface, (x, y)
                )

    def draw_fps_menu(self) -> None:
        self.view.print_info_to_screen(
            self.clock.get_fps(),
            int(self.model_v1.player.position.x),
            int(self.model_v1.player.position.y),
        )

    def draw_score(self) -> None:
        self.view.print_score_to_screen(self.score)

    def draw_game_entities(self) -> None:
        # Loop over grid cells within camera range.
        cell_size: float = self.options.world_specs.cell_size
        left: int = int(
            self.model.get_player().camera.left // cell_size
        )
        right: int = int(
            self.model.get_player().camera.right // cell_size
        )
        bottom: int = int(
            self.model.get_player().camera.top // cell_size
        )
        top: int = int(
            self.model.get_player().camera.bottom // cell_size
        )
        for row in range(bottom, top + 1):
            for col in range(left, right + 1):
                # Wrap the grid col around the map if it extends over the edge
                wrapped_col = (
                    col + self.options.world_specs.grid_width
                ) % self.options.world_specs.grid_width
                # Adjust the entities position if it is wrapping
                entity_adj: Vector2 = Vector2(0, 0)
                if col < 0:
                    entity_adj = Vector2(-self.options.world_specs.world_width, 0)
                if col >= self.options.world_specs.grid_width:
                    entity_adj = Vector2(self.options.world_specs.world_width, 0)
                # Get the grid cell that holds the entities we need to draw
                grid_cell: GridCell = self.model._grid_space.get_grid_cell((row, wrapped_col))
                for group_id, entities in grid_cell.contained_entities_by_manager_id.items():
                    for entity in entities:
                        entity.draw(self.view.screen, self.model.get_player().camera)

    @staticmethod
    def adj_game_entity_pos_to_camera(
        entity_pos: Vector2,
        sprite_w_adj: float,
        sprite_h_adj: float,
        camera_left: float,
        camera_top: float,
    ) -> Tuple[float, float]:
        return (
            entity_pos.x - camera_left - sprite_w_adj,
            camera_top - entity_pos.y - sprite_h_adj,
        )

    def draw_player(self) -> None:
        self.model.get_player().draw(self.view.screen)

    def add_school(self, school: School) -> None:
        self.model.add_entity_manager(school)
        #self.model_v1.add_entity_group(school)
        #self.model_v1.add_spawner(FishSpawner(school, self.options.world_specs, self.camera_specs))

    def add_jellyfish_swarm(self, jellyfish_swarm: JellyfishSwarm) -> None:
        self.model.add_entity_manager(jellyfish_swarm)

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

    def increment_score(self, n: int | None) -> None:
        self.score += n
