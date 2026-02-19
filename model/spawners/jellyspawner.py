import random

from pygame import Vector2

from model.entities.jellyfish.jellyfish import Jellyfish
from model.entitygroups.jellyfishswarm.jellyfishswarm import JellyfishSwarm
from model.player.cameraspecs import CameraSpecs
from model.spawners.spawner import Spawner
from model.world.worldspecs import WorldSpecs


class JellySpawner(Spawner[JellyfishSwarm]):
    def __init__(self, jelly_swarm: JellyfishSwarm, cooldown: float, world_specs: WorldSpecs, camera_specs: CameraSpecs, amount: int):
        super().__init__(jelly_swarm, amount, cooldown, world_specs, camera_specs)

    def spawn_single(
            self,
            world_specs: WorldSpecs,
            camera_specs: CameraSpecs,
            camera_position: Vector2
    ) -> Jellyfish:
        new_jelly: Jellyfish = self.entity_group.create_entity()
        new_jelly.position = self._get_initial_position(world_specs, camera_specs, camera_position)
        return new_jelly

    @staticmethod
    def _get_initial_position(world_specs: WorldSpecs, camera_specs: CameraSpecs, camera_position: Vector2) -> Vector2:
        """
        Get a random x and y position evenly distributed between the edges of the camera and the boundary of the world
        """
        x_ranges = [
            [0, camera_position.x - camera_specs.camera_width_adj],
            [camera_position.x + camera_specs.camera_width_adj, world_specs.world_width],
        ]
        x_weights = [interval[1] - interval[0] for interval in x_ranges]
        x_range = random.choices(x_ranges, weights=x_weights, k=1)[0]
        x_pos = random.uniform(x_range[0], x_range[1])

        y_ranges = [
            [0, camera_position.y - camera_specs.camera_height_adj],
            [camera_position.y + camera_specs.camera_height_adj, world_specs.world_height],
        ]
        y_weights = [interval[1] - interval[0] for interval in y_ranges]
        y_range = random.choices(y_ranges, weights=y_weights, k=1)[0]
        y_pos = random.uniform(y_range[0], y_range[1])

        return Vector2(x_pos, y_pos)
