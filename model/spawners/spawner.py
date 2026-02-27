import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from pygame import Vector2

from model.entities.gameentity import GameEntity
from model.entitygroups.gameentitygroup import GameEntityGroup
from model.player.cameraspecs import CameraSpecs
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class Spawner[T: GameEntityGroup](ABC):
    """
    Basic abstract class for spawners.
    Amount determines how many entities are spawned each time the spawn cooldown (seconds) is reached
    """
    def __init__(self, entity_group: T, amount: int, cooldown: float, world_specs: WorldSpecs, camera_specs: CameraSpecs):
        self.spawner_id: UUID = uuid.uuid4()
        self.entity_group: T = entity_group
        self.cooldown: float = cooldown
        self.spawn_timer: float = 0.0
        self.world_specs: WorldSpecs = world_specs
        self.camera_specs: CameraSpecs = camera_specs
        self.amount: int = amount
        # Tracks if this spawner should be removed from the world
        self._destroy_spawner: bool = False

    def tick_spawn_timer(self, dt: float) -> bool:
        """
        Updates the spawner's timer according to the provided delta time since the last frame. Should only be called
        once in the game loop.
        If the spawning cooldown is reached, returns True and reset the timer, otherwise False.
        """
        self.spawn_timer += dt
        if self.spawn_timer >= self.cooldown:
            self.spawn_timer = 0.0
            return True
        return False

    def spawn(
            self,
            grid_space: GridSpace,
            world_specs: WorldSpecs,
            camera_specs: CameraSpecs,
            camera_position: Vector2
    ) -> None:
        """
        Most basic spawning method possible. Creates new entities based on the amount specified for this spawner.
        Created entities are automatically added into the provided grid space.
        World specs, camera specs, and camera position are provided in case the spawning function wants to place the new
        entities in an initial position relative to any of those parameters.
        """
        for _ in range(self.amount):
            new_entity: GameEntity = self.spawn_single(world_specs, camera_specs, camera_position)
            grid_space.add_entity(new_entity)

    @abstractmethod
    def spawn_single(
            self,
            world_specs: WorldSpecs,
            camera_specs: CameraSpecs,
            camera_position: Vector2
    ) -> GameEntity:
        """
        Creates a single new entity based on the entity group of this spawner.
        World specs, camera specs, and camera position are provided in case the spawning function wants to place the
        entity in an initial position relative to any of those parameters.
        """
        pass

    def set_destroy(self) -> None:
        self._destroy_spawner = True

    def should_destroy(self) -> bool:
        return self._destroy_spawner



