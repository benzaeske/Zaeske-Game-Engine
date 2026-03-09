import copy
import random

from pygame import Vector2, Surface, Rect, image, transform

from model.entities.boid import Boid
from model.entities.fishconfig import FishConfig, FishType
from model.entitymanagers.entitymanager import EntityManager, ModelContext
from model.utils.vectorutils import limit_magnitude


class School(EntityManager):
    def __init__(self, fish_config: FishConfig, amount: int, hatch_region: Rect) -> None:
        super().__init__()
        self._fish_config: FishConfig = fish_config
        self._sprite: Surface = self._get_sprite()
        self._fish: set[Boid] = set()
        self._amount: int = amount
        self._hatch_region: Rect = hatch_region
        self._did_spawn: bool = False

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        if not self._did_spawn:
            # Only hatch fish once at the beginning
            self.hatch(context)
            self._did_spawn = True
        for fish in self._fish:
            fish.frame_actions(context, dt)

    def movement(self, context: ModelContext, dt: float) -> None:
        for fish in self._fish:
            old_pos: Vector2 = copy.deepcopy(fish.get_position())
            fish.move(context, dt)
            context.grid_space.process_moved_entity(old_pos, fish)

    def hatch(self, context: ModelContext) -> None:
        """
        Hatch all the fish according to this school's amount property, fish config and hatch region
        """
        for _ in range(self._amount):
            new_fish: Boid = Boid(
                self._sprite,
                self.get_manager_id(),
                self._fish_config.max_speed,
                self._fish_config.max_acceleration,
                self._fish_config.boid_config
            )
            new_fish.set_position(self._get_initial_position())
            new_fish.set_velocity(self._get_initial_velocity())
            self._fish.add(new_fish)
            context.grid_space.add_entity(new_fish)

    def _get_sprite(self) -> Surface:
        match self._fish_config.fish_type:
            case FishType.RED:
                return self.load_sprite("images/red_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)
            case FishType.YELLOW:
                return self.load_sprite("images/yellow_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)
            case FishType.GREEN:
                return self.load_sprite("images/green_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)

    @staticmethod
    def load_sprite(image_location: str, w, h) -> Surface:
        surface: Surface = image.load(image_location).convert_alpha()
        return transform.scale(surface, (w, h))

    def _get_initial_position(self) -> Vector2:
        """
        Get an initial random position within the rectangular hatch region specified for this school
        """
        return Vector2(
            random.uniform(self._hatch_region.x, self._hatch_region.x + self._hatch_region.width),
            random.uniform(self._hatch_region.y, self._hatch_region.y + self._hatch_region.height),
        )

    def _get_initial_velocity(self) -> Vector2:
        """
        Create an initial velocity vector in a random direction with a magnitude capped at the max speed specified on
        this school's fish config.
        """
        max_speed: float = self._fish_config.max_speed
        initial_velocity = Vector2(
            random.uniform(-max_speed, max_speed),
            random.uniform(-max_speed, max_speed),
        )
        limit_magnitude(initial_velocity, max_speed)
        return initial_velocity

    def get_fish_type(self) -> FishType:
        return self._fish_config.fish_type