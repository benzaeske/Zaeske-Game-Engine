from pygame import Vector2

from model.entities.fish.fish import Fish
from model.entitygroups.school.school import School
from model.player.cameraspecs import CameraSpecs
from model.spawners.spawner import Spawner
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class FishSpawner(Spawner):
    def __init__(self, school: School, world_specs: WorldSpecs, camera_specs: CameraSpecs):
        super().__init__(school, 0.0, world_specs, camera_specs, school.school_params.egg_count)

    def spawn(self, grid_space: GridSpace, camera_position: Vector2):
        # TODO Barebones spawn impl
        #  add logic for positioning new fish here instead of having School do it
        for _ in range(self.amount):
            new_fish: Fish = self.entity_group.create_entity(self.world_specs, self.camera_specs, camera_position)
            self.entity_group.add_entity(new_fish)
            grid_space.add_entity(new_fish)
        # Fish only spawn once in the beginning
        self.set_destroy()