from uuid import UUID

from model.entities.entitymanagers.entitymanager import EntityManager
from model.entities.items.Item import Item
from model.world.modelcontext import ModelContext


class ItemManager(EntityManager):
    def __init__(self):
        super().__init__()
        self._items: dict[UUID, Item] = {}

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        for item in self._items.values():
            item.frame_actions(context, dt)

    def movement(self, context: ModelContext, dt: float) -> None:
        for item in self._items.values():
            item.move(context, dt)

    def add_item(self, item: Item) -> None:
        self._items[item.get_id()] = item

    def remove_item(self, item_id: UUID) -> None:
        self._items.pop(item_id, None)
