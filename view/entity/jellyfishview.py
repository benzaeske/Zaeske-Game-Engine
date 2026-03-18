from pygame import Surface

from model.entity.enemies.jellyfish import Jellyfish
from model.player.camera import Camera
from view.entity.entityview import EntityView
from view.sprite.spritecatalog import SpriteCatalog


class JellyfishView(EntityView[Jellyfish]):
    def __init__(self, jellyfish: Jellyfish, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(jellyfish, sprite_catalog)

    def draw_entity(self, screen: Surface, camera: Camera) -> None:
        # TODO
        pass