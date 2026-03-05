import random
from abc import abstractmethod, ABC

from pygame import Vector2

from model.entities.enemy import Enemy
from model.entities.enemyconfig import EnemyConfig
from model.entities.entity import Entity
from model.entitymanagers.entitymanager import EntityManager, FrameActionContext, MovementContext
from model.world.entitymanagerindex import EntityManagerIndex


class EnemyManager[T: Enemy](EntityManager, ABC):
    """
    Base class for a group of enemies that continue to spawn on a given cooldown interval.
    """
    def __init__(self, initial_cooldown: float, initial_amount: int) -> None:
        super().__init__()
        self._enemies: set[T] = set()
        self._cooldown: float = initial_cooldown
        self._spawn_timer: float = 0.0
        self._amount: int = initial_amount

    def frame_actions(self, context: FrameActionContext, dt: float) -> None:
        # Destroy enemies that have no hp
        for enemy in self._enemies.copy():
            if enemy.get_hp() <= 0:
                self._enemies.remove(enemy)
                context.grid_space.remove_entity(enemy)
        # Spawn new enemies
        if self.tick_spawn_timer(dt):
            self.spawn(context)
        # Accelerate all enemies towards the player and avoid close neighbors
        for enemy in self._enemies:
            neighbors: list[Entity] = context.grid_space.get_entity_neighbors(
                enemy,
                self.get_enemy_config().neighbor_cell_range,
                context.get_manager_ids_by_type(EntityManagerIndex.ENEMY)
            )
            enemy.swarm_to_player(
                self.get_enemy_config(),
                context.get_player_position(),
                neighbors,
                context.get_world_width()
            )

    def movement(self, context: MovementContext, dt: float) -> None:
        for enemy in self._enemies:
            enemy.move(context.get_world_width(), context.get_world_height(), dt)

    def tick_spawn_timer(self, dt: float) -> bool:
        """
        Updates the spawner's timer according to the provided delta time since the last frame. Should only be called
        once in the game loop.
        If the spawning cooldown is reached, returns True and reset the timer, otherwise False.
        """
        self._spawn_timer += dt
        if self._spawn_timer >= self._cooldown:
            self._spawn_timer = 0.0
            return True
        return False

    def spawn(self, context: FrameActionContext) -> None:
        """
        Creates new enemies according to this spawner's amount property. Adds new enemies to this group's list as well
        as to the grid space.
        """
        for _ in range(self._amount):
            new_enemy: T = self.get_new_enemy()
            new_enemy.set_position(self._get_initial_position(context))
            self._enemies.add(new_enemy)
            context.grid_space.add_entity(new_enemy, None)

    @abstractmethod
    def get_new_enemy(self) -> T:
        """
        Factory method to create a new Enemy. Initial position/velocity/acceleration should not be set here
        """
        pass

    @abstractmethod
    def get_enemy_config(self) -> EnemyConfig:
        pass

    @staticmethod
    def _get_initial_position(context: FrameActionContext) -> Vector2:
        """
        Get a random x and y position evenly distributed between the edges of the camera and the boundary of the world
        """
        camera_specs = context.player.camera_specs
        camera_position = Vector2(context.player.camera.center)

        x_ranges = [
            [0, camera_position.x - camera_specs.camera_width_adj],
            [camera_position.x + camera_specs.camera_width_adj, context.get_world_width()],
        ]
        x_weights = [interval[1] - interval[0] for interval in x_ranges]
        x_range = random.choices(x_ranges, weights=x_weights, k=1)[0]
        x_pos = random.uniform(x_range[0], x_range[1])

        y_ranges = [
            [0, camera_position.y - camera_specs.camera_height_adj],
            [camera_position.y + camera_specs.camera_height_adj, context.get_world_height()],
        ]
        y_weights = [interval[1] - interval[0] for interval in y_ranges]
        y_range = random.choices(y_ranges, weights=y_weights, k=1)[0]
        y_pos = random.uniform(y_range[0], y_range[1])

        return Vector2(x_pos, y_pos)