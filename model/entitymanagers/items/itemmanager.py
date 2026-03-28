from uuid import UUID

from pygame import Vector2

from controller.camerainterface import CameraInterface
from model.entities.entity import Entity
from model.entitymanagers.entitymanager import EntityManager
from model.world.modelcontext import ModelContext


class ItemManager(EntityManager):
    """
    Manages item entities.
    """
    def __init__(self):
        super().__init__()
        self._items: dict[UUID, Entity] = {}

    def frame_actions(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        for item in self._items.values():
            item.frame_actions(context, dt)

    def movement(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        for item in self._items.values():
            old_pos: Vector2 = item.get_position()
            item.move(context, dt)
            context.grid_space.process_moved_entity(old_pos, item)

    def track_item(self, item: Entity, context: ModelContext) -> None:
        self._items[item.get_id()] = item
        self._notify_observers_entity_created(item)
        context.grid_space.add_entity(item)

    def remove_item(self, item_id: UUID) -> None:
        self._notify_observers_entity_deleted(self._items.pop(item_id, None))
