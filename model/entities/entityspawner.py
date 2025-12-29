from abc import ABC, abstractmethod

from pygame import Vector2

from model.entities.entitygroup import EntityGroup
from model.entities.gameentity import GameEntity


class EntitySpawner(ABC, EntityGroup):
    def __init__(self, amount: int, spawn_delay: float):
        super().__init__()
        self.amount: int = amount
        self.spawn_delay: float = spawn_delay
        self.spawn_timer: float = spawn_delay

    @abstractmethod
    def check_for_spawn(self) -> bool:
        """
        Checks each frame if this spawner is ready to spawn new entities. When true, the spawn method will be called.
        """
        pass

    @abstractmethod
    def spawn(self, player_position: Vector2) -> list[GameEntity]:
        """
        Spawns new entities.
        This method is responsible for adding new entities to the base class EntityGroup's list of entities before returning
        """
        pass

