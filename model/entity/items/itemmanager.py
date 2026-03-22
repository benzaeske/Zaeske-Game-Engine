import copy
from uuid import UUID

from pygame import Vector2

from controller.camerainterface import CameraInterface
from model.entity.entity import Entity
from model.entity.entitymanager import EntityManager
from model.world.modelcontext import ModelContext


class ItemManager(EntityManager):
    """
    Manages active player item entities.
    """
    def __init__(self):
        super().__init__()
        self._items: dict[UUID, Entity] = {}

    def frame_actions(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        for item in self._items.values():
            item.frame_actions(context, dt)

    def movement(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        for item in self._items.values():
            old_pos: Vector2 = copy.deepcopy(item.get_position())
            item.move(context, dt)
            context.grid_space.process_moved_entity(old_pos, item)

    def track_item(self, item: Entity) -> None:
        self._items[item.get_id()] = item

    def remove_item(self, item_id: UUID) -> None:
        self._items.pop(item_id, None)
