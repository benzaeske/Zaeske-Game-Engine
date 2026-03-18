from view.sprite.entityanimation import EntityAnimation
from view.sprite.playeranimation import PlayerAnimation
from view.sprite.spritesheet import SpriteSheet


class SpriteCatalog:
    """
    Repository containing all sprite sheets needed to draw the player and game entity animations.
    """
    def __init__(self):
        self._entity_animations: dict[EntityAnimation, SpriteSheet] = {}
        self._player_animations: dict[PlayerAnimation, SpriteSheet] = {}
        self._load()

    def get_entity_animation(self, animation: EntityAnimation) -> SpriteSheet:
        return self._entity_animations[animation]

    def get_player_animation(self, animation: PlayerAnimation) -> SpriteSheet:
        return self._player_animations[animation]

    def _load(self) -> None:
        """
        Loads all sprite sheets. Should only be called once in the constructor.
        """
        self._load_entity_animations()
        self._load_player_animations()

    def _load_entity_animations(self) -> None:
        pass

    def _load_player_animations(self) -> None:
        pass

