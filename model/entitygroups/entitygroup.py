import uuid
from abc import ABC
from uuid import UUID

from model.entities.entity import Entity, FrameActionContext, EntityMovementContext


class EntityGroup(ABC):
    """
    A group of entities that are controlled by the game.
    """
    def __init__(self):
        self._group_id: UUID = uuid.uuid4()
        self._entities: set[Entity] = set()

    def frame_actions(self, context: FrameActionContext, dt: float) -> None:
        """
        Performs frame actions for all entities in the group. Should be overridden by subclasses to perform frame
        actions of its own that are separate from the individual entities.
        """
        for entity in self._entities:
            entity.frame_actions(context, dt)

    def move_entities(self, context: EntityMovementContext, dt: float) -> None:
        """
        Moves all entities in the group.
        """
        for entity in self._entities:
            entity.move(context, dt)

    def add_entity(self, entity: Entity) -> None:
        self._entities.add(entity)

    def remove_entity(self, entity: Entity) -> None:
        self._entities.remove(entity)

    def get_group_id(self) -> UUID:
        return self._group_id
