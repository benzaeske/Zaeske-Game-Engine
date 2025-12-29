import random

import pygame
from pygame import Surface, Vector2

from model.entities.entitygroup import EntityGroup
from model.entities.fish.fish import Fish
from model.entities.fish.fishsettings import FishType
from model.entities.jellyfish.jellyfish import Jellyfish
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings, JellyfishType
from model.entities.school.school import School
from model.player.cameraspecs import CameraSpecs
from model.world.grid_cell import GridCell
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
        world_specs: WorldSpecs,
        grid_space: list[list[GridCell]],
        player_position: Vector2 | None = None,
    ) -> None:
        neighbor_range: int = 1
        scared_range: int = 2
        for jellyfish in self.entities.values():
            neighbor_jellies: list[Jellyfish] = []
            r: int = int(jellyfish.position.y / world_specs.cell_size)
            c: int = int(jellyfish.position.x / world_specs.cell_size)
            for dr in range(-neighbor_range, neighbor_range + 1):
                for dc in range(-neighbor_range, neighbor_range + 1):
                    grid_r: int = r + dr
                    grid_r = (
                        grid_r + world_specs.grid_height
                    ) % world_specs.grid_height
                    grid_c: int = c + dc
                    grid_c = (grid_c + world_specs.grid_width) % world_specs.grid_width
                    group: EntityGroup[Jellyfish] = grid_space[grid_r][
                        grid_c
                    ].entity_groups.get(self.group_id)
                    if group is not None:
                        neighbor_jellies.extend(group.entities.values())

            afraid_of_fish: list[Fish] = []
            r: int = int(jellyfish.position.y / world_specs.cell_size)
            c: int = int(jellyfish.position.x / world_specs.cell_size)
            for dr in range(-scared_range, scared_range + 1):
                for dc in range(-scared_range, scared_range + 1):
                    grid_r: int = r + dr
                    grid_r = (
                        grid_r + world_specs.grid_height
                    ) % world_specs.grid_height
                    grid_c: int = c + dc
                    grid_c = (grid_c + world_specs.grid_width) % world_specs.grid_width
                    for entity_group in grid_space[grid_r][
                        grid_c
                    ].entity_groups.values():
                        if (
                            isinstance(entity_group, School)
                            and entity_group.fish_settings.fish_type is FishType.RED
                        ):
                            afraid_of_fish.extend(entity_group.entities.values())

            jellyfish.update_acceleration(
                player_position,
                neighbor_jellies,
                afraid_of_fish,
                world_specs.world_width,
            )

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
