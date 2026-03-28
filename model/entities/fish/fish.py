from uuid import UUID

from pygame import Rect

from model.entities.fish.boid import Boid
from model.entities.fish.fishconfigv1 import FishConfigV1, FishType
from model.world.modelcontext import ModelContext


class Fish(Boid):
    def __init__(self, manager_id: UUID, fish_config: FishConfigV1, shoal: Rect | None = None) -> None:
        super().__init__(manager_id, fish_config.max_speed, fish_config.max_acceleration, fish_config.boid_config)
        self._fish_type: FishType = fish_config.fish_type
        self._shoal: Rect | None = shoal
        self._shoal_radius: float = fish_config.shoal_radius
        self._shoal_k: float = fish_config.shoal_k

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        super().frame_actions(context, dt)
        if self._shoal is not None:
            self._move_to_shoal()

    def _move_to_shoal(self) -> None:
        """
        Fish in a group can optionally move to a shoaling location in addition to schooling together.
        """
        d: float = self.get_position().distance_to(self._shoal.center)
        diff = self._shoal.center - self.get_position()
        if d > self._shoal_radius:
            self.target(diff, self._shoal_k)
        else:
            self.target(diff, -self._shoal_k)

    def get_fish_type(self) -> FishType:
        return self._fish_type