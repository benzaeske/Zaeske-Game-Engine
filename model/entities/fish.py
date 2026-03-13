from uuid import UUID

from pygame import Surface, Rect

from model.entities.boid import Boid
from model.entities.fishconfig import FishConfig
from model.world.modelcontext import ModelContext


class Fish(Boid):
    def __init__(self, sprite: Surface, manager_id: UUID, fish_config: FishConfig, shoal: Rect | None = None) -> None:
        super().__init__(sprite, manager_id, fish_config.max_speed, fish_config.max_acceleration, fish_config.boid_config)
        self._shoal: Rect | None = shoal
        self._shoal_radius: float = fish_config.shoal_radius
        self._shoal_k: float = fish_config.shoal_k

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        super().frame_actions(context, dt)
        if self._shoal is not None:
            self.shoal()

    def shoal(self) -> None:
        """
        Fish in a group can optionally move to a shoaling location in addition to schooling together.
        """
        d: float = self.get_position().distance_to(self._shoal.center)
        diff = self._shoal.center - self.get_position()
        if d > self._shoal_radius:
            self.target(diff, self._shoal_k)
        else:
            self.target(diff, -self._shoal_k)