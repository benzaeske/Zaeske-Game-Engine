from abc import ABC

from model.entities.entity import Entity
from model.world.modelcontext import ModelContext


class Item(Entity, ABC):
    def __init__(self):
        super().__init__()

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        pass

    def move(self, context: ModelContext, dt: float) -> None:
        pass