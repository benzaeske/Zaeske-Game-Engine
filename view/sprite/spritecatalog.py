from pygame import Surface, image, transform

from model.entities.entitytype import EntityType
from model.player.playerconfig import PlayerConfig
from view.sprite.playeranimation import PlayerAnimation
from view.sprite.spriteconfig import SpriteConfig
from view.sprite.spritedata import SpriteData


class SpriteCatalog:
    """
    Source of truth for all sprite sheets needed to draw the player and game entity animations.
    """
    def __init__(self, sprite_configs: list[SpriteConfig], player_config: PlayerConfig) -> None:
        self._entity_sprites: dict[EntityType, SpriteData] = {} # Basic sprites that don't support animation frames for now
        self._player_animations: dict[PlayerAnimation, SpriteData] = {}
        self._load(sprite_configs, player_config)

    def get_entity_sprite_data(self, entity_type: EntityType) -> SpriteData:
        return self._entity_sprites.get(entity_type, None)

    def get_player_animation(self, animation: PlayerAnimation) -> SpriteData:
        return self._player_animations[animation]

    def _load(self, sprite_configs: list[SpriteConfig], player_config: PlayerConfig) -> None:
        """
        Loads all sprite sheets. Should only be called once in the constructor.
        """
        self._load_entity_sprites(sprite_configs)
        self._load_player_animations(player_config)

    def _load_entity_sprites(self, sprite_configs: list[SpriteConfig]) -> None:
        for config in sprite_configs:
            self._entity_sprites[config.entity_type] = SpriteData(
                self.load_image(config.image_location, config.sprite_width, config.sprite_height)
            )

    def _load_player_animations(self, player_config: PlayerConfig) -> None:
        self._player_animations[PlayerAnimation.SWIMMING_LEFT] = SpriteData(
            self.load_image_from_config(player_config.left_sprite))
        self._player_animations[PlayerAnimation.SWIMMING_RIGHT] = SpriteData(
            self.load_image_from_config(player_config.right_sprite))
        self._player_animations[PlayerAnimation.IDLE_LEFT] = SpriteData(
            self.load_image_from_config(player_config.left_sprite))
        self._player_animations[PlayerAnimation.IDLE_RIGHT] = SpriteData(
            self.load_image_from_config(player_config.right_sprite))

    def load_image_from_config(self, sprite_config: SpriteConfig) -> Surface:
        return self.load_image(sprite_config.image_location, sprite_config.sprite_width, sprite_config.sprite_height)

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