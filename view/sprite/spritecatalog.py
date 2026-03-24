from pygame import Surface, image, transform

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
        self._entity_animations[EntityAnimation.RED_JELLYFISH] = SpriteSheet(
            [(1.0, self.load_image("images/red_jelly.png", 96.0, 96.0))],
            96.0,
            96.0
        )
        self._entity_animations[EntityAnimation.RED_FISH] = SpriteSheet(
            [(1.0, self.load_image("images/red_fish.png", 32.0, 32.0))],
            32.0,
            32.0
        )
        self._entity_animations[EntityAnimation.YELLOW_FISH] = SpriteSheet(
            [(1.0, self.load_image("images/yellow_fish.png", 26.0, 26.0))],
            26.0,
            26.0
        )
        self._entity_animations[EntityAnimation.GREEN_FISH] = SpriteSheet(
            [(1.0, self.load_image("images/green_fish.png", 36.0, 36.0))],
            36.0,
            36.0
        )

    def _load_player_animations(self) -> None:
        player_width: float = 128.0
        player_height: float = 128.0
        self._player_animations[PlayerAnimation.SWIMMING_LEFT] = SpriteSheet(
            [(1.0, self.load_image("images/baby_turtle_left.png", player_width, player_height))],
            player_width,
            player_height
        )
        self._player_animations[PlayerAnimation.SWIMMING_RIGHT] = SpriteSheet(
            [(1.0, self.load_image("images/baby_turtle_right.png", player_width, player_height))],
            player_width,
            player_height
        )
        self._player_animations[PlayerAnimation.IDLE_LEFT] = SpriteSheet(
            [(1.0, self.load_image("images/baby_turtle_left.png", player_width, player_height))],
            player_width,
            player_height
        )
        self._player_animations[PlayerAnimation.IDLE_RIGHT] = SpriteSheet(
            [(1.0, self.load_image("images/baby_turtle_right.png", player_width, player_height))],
            player_width,
            player_height
        )

    @staticmethod
    def load_image(image_location: str, width: float, height: float) -> Surface:
        """
        Loads a surface from the provided image location and scales it to the provided width and height. Uses convert_alpha
        on the surface before returning it.
        """
        surface: Surface = image.load(image_location).convert_alpha()
        return transform.scale(
            surface, (width, height)
        ).convert_alpha()