import random
from uuid import UUID

import pygame
from pygame import Surface, Vector2

from model.entities.gameentity import GameEntity
from model.entitygroups.entitygroup import EntityGroup
from model.entities.fish.fishsettings import FishType
from model.entities.jellyfish.jellyfish import Jellyfish
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings, JellyfishType
from model.entitygroups.school.school import School
from model.player.cameraspecs import CameraSpecs
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class JellyfishSwarm(EntityGroup[Jellyfish]):
    def __init__(self, jellyfish_settings: JellyfishSettings, amount: int):
        super().__init__()
        self.jellyfish_settings: JellyfishSettings = jellyfish_settings
        self.sprite = self.get_jelly_sprite(
            jellyfish_settings.jelly_type,
            jellyfish_settings.width,
            jellyfish_settings.height,
        )
        self.amount: int = amount

    def update_entities(
        self,
        grid_space: GridSpace,
        entity_groups: dict[UUID, EntityGroup],
        world_specs: WorldSpecs,
        player_position: Vector2 | None = None,
    ) -> None:
        # TODO make these properties on jellyfish settings
        neighbor_range: int = 1
        scared_range: int = 2
        scared_of_groups: set[UUID] = self.get_scared_group_ids(entity_groups)
        for jellyfish in self._entities:
            neighbor_jellies: list[GameEntity] = grid_space.get_neighbors(jellyfish, neighbor_range)
            afraid_of_fish: list[GameEntity] = grid_space.get_neighbors(jellyfish, scared_range, scared_of_groups)
            jellyfish.update_acceleration(
                player_position,
                neighbor_jellies,
                afraid_of_fish,
                world_specs.world_width,
            )

    @staticmethod
    def get_scared_group_ids(entity_groups: dict[UUID, EntityGroup]) -> set[UUID]:
        """
        Returns a set of group ids of entities that jellyfish are afraid of
        :param entity_groups: The current entity groups present in the game world
        :return: A set of group ids
        """
        scared_of_groups: set[UUID] = set()
        for group in entity_groups.values():
            if isinstance(group, School) and group.fish_settings.fish_type is FishType.RED:
                scared_of_groups.add(group.group_id)
        return scared_of_groups

    def create_entity(
        self,
        world_specs: WorldSpecs,
        camera_specs: CameraSpecs | None = None,
        camera_position: Vector2 | None = None,
    ) -> Jellyfish:
        return self.spawn_jellyfish(
            camera_position,
            camera_specs.camera_width_adj,
            camera_specs.camera_height_adj,
            world_specs.world_width,
            world_specs.world_height,
        )

    @staticmethod
    def get_jelly_sprite(
        jelly_type: JellyfishType, width: float, height: float
    ) -> Surface:
        match jelly_type:
            case JellyfishType.RED:
                surface: Surface = pygame.image.load(
                    "images/red_jelly.png"
                ).convert_alpha()
                return pygame.transform.scale(surface, (width, height))

    def spawn_jellyfish(
        self,
        camera_pos: Vector2,
        camera_w_adj: float,
        camera_h_adj: float,
        world_w: float,
        world_h: float,
    ) -> Jellyfish:
        """Create a new jellyfish at a random position outside camera range but within the world boundary"""
        # TODO this logic should move to the spawner.
        #  Create entity on EntityGroup should just return a blank entity that has no meaningful initial position
        # Pick between 2 different ranges: one between 0 and the camera edge, the other between the camera edge and the far world boundary
        x_ranges = [
            [0, camera_pos.x - camera_w_adj],
            [camera_pos.x + camera_w_adj, world_w],
        ]
        x_weights = [interval[1] - interval[0] for interval in x_ranges]
        x_range = random.choices(x_ranges, weights=x_weights, k=1)[0]
        x_pos = random.uniform(x_range[0], x_range[1])

        y_ranges = [
            [0, camera_pos.y - camera_h_adj],
            [camera_pos.y + camera_h_adj, world_h],
        ]
        y_weights = [interval[1] - interval[0] for interval in y_ranges]
        y_range = random.choices(y_ranges, weights=y_weights, k=1)[0]
        y_pos = random.uniform(y_range[0], y_range[1])

        return Jellyfish(
            self.group_id,
            self.sprite,
            JellyfishSettings(
                self.jellyfish_settings.jelly_type,
                self.jellyfish_settings.width,
                self.jellyfish_settings.height,
                Vector2(x_pos, y_pos),
                Vector2(0.0, 0.0),
                self.jellyfish_settings.max_speed,
                self.jellyfish_settings.max_acceleration,
                self.jellyfish_settings.health,
                self.jellyfish_settings.damage,
            ),
        )
