import random

from pygame import Vector2, Surface, Rect

from model.entities.boid import Boid
from model.entities.fishconfig import FishConfig, FishType
from model.entitymanagers.entitymanager import EntityManager, FrameActionContext, MovementContext
from model.utils.vectorutils import limit_magnitude


class School(EntityManager):
    def __init__(self, fish_config: FishConfig, amount: int, hatch_region: Rect, sprite: Surface) -> None:
        super().__init__()
        self._fish: set[Boid] = set()
        self._fish_config: FishConfig = fish_config
        self._amount: int = amount
        self._hatch_region: Rect = hatch_region
        self._sprite: Surface = sprite
        self._did_spawn: bool = False

    def frame_actions(self, context: FrameActionContext, dt: float) -> None:
        if not self._did_spawn:
            # Only hatch fish once at the beginning
            self.hatch(context)
            self._did_spawn = True
        for fish in self._fish:
            fish.frame_actions(
                self._fish_config.boid_config,
                context.grid_space.get_entity_neighbors(fish, self._fish_config.boid_config.interaction_cell_range),
                context.get_world_width(),
                context.get_world_height()
            )

    def movement(self, context: MovementContext, dt: float) -> None:
        for fish in self._fish:
            fish.move(context.get_world_width(), context.get_world_height(), dt)

    def hatch(self, context: FrameActionContext) -> None:
        """
        Hatch all the fish according to this school's amount property, fish config and hatch region
        """
        for _ in range(self._amount):
            new_fish: Boid = Boid(
                self._sprite,
                self.get_manager_id(),
                self._fish_config.max_speed,
                self._fish_config.max_acceleration
            )
            new_fish.set_position(self._get_initial_position())
            new_fish.set_velocity(self._get_initial_velocity())
            self._fish.add(new_fish)
            context.grid_space.add_entity(new_fish, None)

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
        return self._fish_config.type