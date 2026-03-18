from abc import ABC
from uuid import UUID

from model.entity.entity import Entity
from model.world.modelcontext import ModelContext


class Item(Entity, ABC):
    def __init__(self, manager_id: UUID):
        super().__init__(manager_id)

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        pass

    def move(self, context: ModelContext, dt: float) -> None:
        pass