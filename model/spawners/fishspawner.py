import random

from pygame import Vector2

from model.entities.fish.fishv1 import FishV1
from model.entities.fish.fishsettingsv1 import FishSettingsV1
from model.entitygroups.school.schoolv1 import SchoolV1
from model.player.cameraspecs import CameraSpecs
from model.spawners.spawner import Spawner
from model.utils.vectorutils import limit_magnitude
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class FishSpawner(Spawner[SchoolV1]):
    def __init__(self, school: SchoolV1, world_specs: WorldSpecs, camera_specs: CameraSpecs):
        super().__init__(school, school.school_params.egg_count, 0.0, world_specs, camera_specs)

    def spawn(
            self,
            grid_space: GridSpace,
            world_specs: WorldSpecs,
            camera_specs: CameraSpecs,
            camera_position: Vector2
    ) -> None:
        super().spawn(grid_space, world_specs, camera_specs, camera_position)
        # Fish only spawn once in the beginning
        self.set_destroy()

    def spawn_single(
            self,
            world_specs: WorldSpecs,
            camera_specs: CameraSpecs,
            camera_position: Vector2
    ) -> FishV1:
        new_fish: FishV1 = self.entity_group.create_entity()
        new_fish.position = self._get_initial_position()
        new_fish.velocity = self._get_initial_velocity()
        return new_fish

    def _get_initial_position(self) -> Vector2:
        hatch_region = self.entity_group.school_params.hatch_region
        return Vector2(
            random.uniform(hatch_region.x, hatch_region.x + hatch_region.width),
            random.uniform(hatch_region.y, hatch_region.y + hatch_region.height),
        )

    def _get_initial_velocity(self) -> Vector2:
        fish_settings: FishSettingsV1 = self.entity_group.fish_settings
        initial_velocity = Vector2(
            random.uniform(-fish_settings.max_speed, fish_settings.max_speed),
            random.uniform(-fish_settings.max_speed, fish_settings.max_speed),
        )
        limit_magnitude(initial_velocity, fish_settings.max_speed)
        return initial_velocity