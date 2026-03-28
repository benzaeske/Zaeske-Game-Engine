import sys
import time
from typing import Tuple
from uuid import UUID

import pygame
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.time import Clock

from model.entities.fish.boidconfigv1 import BoidConfigV1
from model.entities.enemies.enemyconfigv1 import EnemyConfigV1
from model.entities.fish.fishconfigv1 import FishConfigV1, FishType
from model.entities.enemies.jellyfishconfigv1 import JellyfishType, JellyfishConfigV1
from model.entities.enemies.jellyfishswarm import JellyfishSwarm
from model.entitymanagers.fish.school import School
from controller.camera import Camera
from model.entitymanagers.items.itemmanager import ItemManager
from model.entities.items.shield import Shield
from model.player.player import Player
from model.player.turtle import Turtle
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.gridspace.grid_cell import GridCell
from model.world.model import Model
from view.view import View, WindowOptions


class ControllerOptions:
    def __init__(
        self,
        window_options: WindowOptions,
        grid_cell_size: float
    ) -> None:
        self.window_options: WindowOptions = window_options
        self.grid_cell_size: float = grid_cell_size


class GameController:
    """
    Top level orchestration class for managing logic loops for the game and menus. Contains a model for simulating the
    game world and entities, and a view class for drawing onto the screen.
    """
    def __init__(
        self,
        options: ControllerOptions,
    ) -> None:
        pygame.init()
        ############################
        # Initialize View and Model:
        ############################
        # The View holds all logic related to drawing entities and rendering on screen
        self._view: View = View(options.window_options)
        # The Model holds the simulated world and is responsible for performing updates each frame
        self._model: Model = Model(options.grid_cell_size)
        self._model.register_entity_manager_observer(self._view)
        # Initialize the player and register on View and Model
        self._player: Player = Turtle()
        self._view.register_player(self._player)
        self._model.register_player(self._player)
        # Initialize the camera
        self._camera: Camera = Camera(self._view.get_screen_width(), self._view.get_screen_height())
        self._player.add_movement_listener(self._camera)
        ####################################
        # Variables for tracking game state:
        ####################################
        self._clock: Clock = pygame.time.Clock()
        self._fps: int = 60
        self._game_start_time: float = -1
        self._dt: float = 0.0
        self._mouse_pos: Tuple[int, int] = (0, 0)
        self._key_presses: ScancodeWrapper = ScancodeWrapper(())
        self._current_frame_input_events: list[Event] = []
        self._paused: bool = False

    def start_game(self):
        self._game_start_time = time.time()
        self._create_entity_managers()
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
            view_update_time = time.time() - view_update_time
            self.fps_logging(model_update_time, view_update_time)
        self._dt = self._clock.tick(self._fps) / 1000

    def check_for_terminate(self):
        for event in self._current_frame_input_events:
            if event.type == pygame.QUIT:
                sys.exit()
        if self._key_presses[pygame.K_ESCAPE]:
            sys.exit()
        if self._player.get_current_health() <= 0.0:
            sys.exit()

    def check_for_pause(self):
        for event in self._current_frame_input_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._paused = not self._paused

    def update_model(self) -> None:
        self._model.update(self._key_presses, self._camera, self._dt)

    def draw(self) -> None:
        self.draw_background()
        camera_grid_cells: list[GridCell] = (self._model.get_model_context().grid_space
                                             .get_grid_cells_in_camera_range(self._camera))
        # Draw in a specified order:
        #  Fish
        self.draw_entities(camera_grid_cells, EntityManagerIndex.FISH)
        #  Player
        self.draw_player()
        #  Enemies
        self.draw_entities(camera_grid_cells, EntityManagerIndex.ENEMY)
        #  Items
        self.draw_entities(camera_grid_cells, EntityManagerIndex.ITEM)
        self._view.update_screen()

    def draw_background(self) -> None:
        self._view.draw_background(self._camera)

    def draw_player(self) -> None:
        self._view.draw_player(self._camera, self._dt)

    def draw_entities(self, grid_cells: list[GridCell], entity_type: EntityManagerIndex) -> None:
        """
        Draws all entities of a given type found in the provided grid cells
        :param grid_cells: The grid cells containing entities to draw.
        :param entity_type: Only entities belonging to entity managers of this type will be drawn.
        """
        manager_ids: set[UUID] = self._model.get_model_context().entity_repository.get_manager_ids(entity_type)
        for grid_cell in grid_cells:
            for entity in grid_cell.get_entities_by_manager_ids(manager_ids):
                self._view.draw_entity(entity.get_id(), self._camera, self._dt)

    def _create_entity_managers(self) -> None:
        """
        Statically creates entity managers for all entities in the game world. This will eventually be replaced with a
        more dynamic method that adds/removes entity managers throughout the game based on various factors such as
        player position, game time, world state etc
        """

        # ORDER MATTERS!

        # Item manager first
        item_manager: ItemManager = ItemManager()
        self._model.add_entity_manager(item_manager)
        item_manager.track_item(
            Shield(item_manager.get_manager_id(), 128.0, 100.0),
            self._model.get_model_context(),
        )

        jelly_spawn_cd: float = 5.0
        jelly_spawn_amount: int = 4
        jelly_config: JellyfishConfigV1 = JellyfishConfigV1(
            JellyfishType.RED,
            96.0,
            96.0,
            EnemyConfigV1(
                192.0,
                256.0,
                96.0,
                96.0,
                100,
                10,
                1,
                96.0,
                2.0
            ),
            2,
            192.0,
            3.0
        )
        self._model.add_entity_manager(JellyfishSwarm(jelly_spawn_cd, jelly_spawn_amount, jelly_config))

        red_fish: FishConfigV1 = FishConfigV1(
            FishType.RED,
            160.0,
            48.0,
            BoidConfigV1(
                128.0,
                48.0,
                1,
                1.0,
                2.0,
                1.0
            ),
            True,
            128.0,
            1.2
        )
        num_red_schools: int = 2
        for _ in range(num_red_schools):
            school: School = School(red_fish, 16, self._model.get_model_context())
            self._model.add_entity_manager(school)
            school.hatch(self._model.get_model_context())

        yellow_fish: FishConfigV1 = FishConfigV1(
            FishType.YELLOW,
            224.0,
            100.0,
            BoidConfigV1(
                128.0,
                44.0,
                1,
                1,
                2.0,
                1.0
            ),
            True,
            384.0,
            1.2
        )
        num_yellow_schools: int = 2
        for _ in range(num_yellow_schools):
            school: School = School(yellow_fish, 16, self._model.get_model_context())
            self._model.add_entity_manager(school)
            school.hatch(self._model.get_model_context())

        green_fish: FishConfigV1 = FishConfigV1(
            FishType.GREEN,
            128.0,
            32.0,
            BoidConfigV1(
                128.0,
                52.0,
                1,
                1.0,
                2.0,
                1.0
            ),
            True,
            64.0,
            1.2
        )
        num_green_schools: int = 2
        for _ in range(num_green_schools):
            school: School = School(green_fish, 16, self._model.get_model_context())
            self._model.add_entity_manager(school)
            school.hatch(self._model.get_model_context())

    def fps_logging(self, model_t: float, view_t: float) -> None:
        if self._dt > 0.017:
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