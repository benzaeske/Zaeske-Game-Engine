from pygame import Vector2

from model.entities.jellyfish.jellyfish import Jellyfish
from model.entitygroups.entitygroup import EntityGroup
from model.player.cameraspecs import CameraSpecs
from model.spawners.spawner import Spawner
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class JellySpawner(Spawner):
    def __init__(self, entity_group: EntityGroup[Jellyfish], cooldown: float, world_specs: WorldSpecs, camera_specs: CameraSpecs, amount: int):
        super().__init__(entity_group, cooldown, world_specs, camera_specs, amount)

    def spawn(self, grid_space: GridSpace, camera_position: Vector2):
        for _ in range(self.amount):
            # TODO Barebones spawn impl
            #  add logic for positioning new jellies here instead of having the JellyFishSwarm do it
            new_entity: Jellyfish = self.entity_group.create_entity(self.world_specs, self.camera_specs, camera_position)
            self.entity_group.add_entity(new_entity)
            grid_space.add_entity(new_entity)
