from abc import ABC, abstractmethod

from pygame import Vector2

from model.entitygroups.entitygroup import EntityGroup
from model.player.cameraspecs import CameraSpecs
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class Spawner(ABC):
    """
    Basic abstract class for all spawners.
    Provides a built-in method for tracking spawn cooldown and a basic spawn method for a single entity.
    Amount determines how many entities are spawned per spawn cooldown.
    """
    def __init__(self, entity_group: EntityGroup, cooldown: float, world_specs: WorldSpecs, camera_specs: CameraSpecs, amount: int = 1):
        self.entity_group: EntityGroup = entity_group
        self.cooldown: float = cooldown
        self.spawn_timer: float = 0.0
        self.world_specs: WorldSpecs = world_specs
        self.camera_specs: CameraSpecs = camera_specs
        self.amount: int = amount

    def tick_spawn_timer(self, dt: float) -> bool:
        """
        Updates the spawner's timer according to the provided delta time since the last frame. Should only be called once in the game loop.
        If the spawning cooldown is reached, returns True and reset the timer, otherwise False.
        """
        self.spawn_timer += dt
        if self.spawn_timer > self.cooldown:
            self.spawn_timer = 0.0
            return True
        return False


    @abstractmethod
    def spawn(self, grid_space: GridSpace, camera_position: Vector2) -> EntityGroup:
        """
        Most basic spawning method possible. Creates a new entity.
        Adds it to the entity group the spawner is built from and adds it to the provided grid space.
        Camera position is provided as an input in case future spawning functions want to determine spawn location based on things being in/out of frame.
        """
        pass



