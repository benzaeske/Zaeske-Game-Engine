import uuid
from abc import ABC, abstractmethod

from pygame import Vector2

from model.entities.gameentity import GameEntity


class EntityGroup(ABC):
    def __init__(self):
        self.group_id: uuid.UUID = uuid.uuid4()
        self.entities: dict[uuid.UUID, GameEntity] = {}

    @abstractmethod
    def update_entities(self, world_width: float | None = None, world_height: float | None = None, player_position: Vector2 | None = None) -> None:
        """
        Updates all entities in their current position for a given frame. Does not move them.
        """
        pass

    def move_entities(self, world_w: float, world_h: float, dt: float) -> None:
        """
        Moves all entities in the group based on delta time (dt) since the last frame.
        World width and world height are used for x-axis wrapping rules and preventing entities from leaving y-axis edge boundaries respectively.
        """
        for entity in self.entities.values():
            entity.update_position(world_w, world_h, dt)

    @abstractmethod
    def create_entity(self, camera_position: Vector2 | None = None) -> GameEntity:
        """
        Factory method to create a new entity that belongs to this group.
        """
        pass

