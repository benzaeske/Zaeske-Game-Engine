from pygame import Surface, image, transform

from model.entities.entitytype import EntityType
from view.sprite.playeranimation import PlayerAnimation
from view.sprite.spriteconfig import SpriteConfig
from view.sprite.spritedata import SpriteData
from view.sprite.spritesheet import SpriteSheet


class SpriteCatalog:
    """
    Repository containing all sprite sheets needed to draw the player and game entity animations.
    """
    def __init__(self, sprite_configs: list[SpriteConfig]):
        self._entity_sprites: dict[EntityType, SpriteData] = {} # Basic sprites that don't support animation frames for now
        self._player_animations: dict[PlayerAnimation, SpriteSheet] = {}
        self._load(sprite_configs)

    def get_entity_sprite_data(self, entity_type: EntityType) -> SpriteData:
        return self._entity_sprites.get(entity_type, None)

    def get_player_animation(self, animation: PlayerAnimation) -> SpriteSheet:
        return self._player_animations[animation]

    def _load(self, sprite_configs: list[SpriteConfig]) -> None:
        """
        Loads all sprite sheets. Should only be called once in the constructor.
        """
        self._load_entity_sprites(sprite_configs)
        self._load_player_animations()

    def _load_entity_sprites(self, sprite_configs: list[SpriteConfig]) -> None:
        for config in sprite_configs:
            self._entity_sprites[config.entity_type] = SpriteData(
                self.load_image(config.image_location, config.sprite_width, config.sprite_height)
            )

    def _load_player_animations(self) -> None:
        player_width: float = 128.0
        player_height: float = 128.0
        self._player_animations[PlayerAnimation.SWIMMING_LEFT] = SpriteSheet(
            [(1.0, self.load_image("assets/images/baby_turtle_left.png", player_width, player_height))],
            player_width,
            player_height
        )
        self._player_animations[PlayerAnimation.SWIMMING_RIGHT] = SpriteSheet(
            [(1.0, self.load_image("assets/images/baby_turtle_right.png", player_width, player_height))],
            player_width,
            player_height
        )
        self._player_animations[PlayerAnimation.IDLE_LEFT] = SpriteSheet(
            [(1.0, self.load_image("assets/images/baby_turtle_left.png", player_width, player_height))],
            player_width,
            player_height
        )
        self._player_animations[PlayerAnimation.IDLE_RIGHT] = SpriteSheet(
            [(1.0, self.load_image("assets/images/baby_turtle_right.png", player_width, player_height))],
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