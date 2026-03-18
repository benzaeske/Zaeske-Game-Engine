from pygame import Surface

from model.entity.fish.fish import Fish
from model.player.camera import Camera
from view.entity.entityview import EntityView
from view.sprite.spritecatalog import SpriteCatalog


class FishView(EntityView[Fish]):
    def __init__(self, fish: Fish, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(fish, sprite_catalog)

    def draw_entity(self, screen: Surface, camera: Camera) -> None:
        # TODO
        pass