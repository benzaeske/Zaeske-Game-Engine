import copy
from typing import Callable
from uuid import UUID

from pygame import Vector2, Surface, Rect
from pygame.constants import SRCALPHA
from pygame.draw import circle

from model.entities.gameentity import GameEntity
from model.entities.playerentity import PlayerEntity
from model.player.player import Player
from model.world.entitygroupindex import EntityGroupIndex
from model.world.gridspace import GridSpace


class Shield(PlayerEntity):
    def __init__(self, player_pos: Vector2):
        super().__init__(player_pos)
        self.max_shield: int = 10
        self.shield: int = 0
        self.shield_radius: float = self.hitbox.width
        self.shield_radius_squared: float = self.shield_radius * self.shield_radius
        self.shield_charge_delay: float = 1.0
        self.current_shield_charge_cooldown: float = self.shield_charge_delay
        self.shield_alpha_scaling: int = 10
        self.shield_surface: Surface = self.get_shield_surface()
        self.shield_surface_w_adj: float = self.shield_surface.get_width() / 2
        self.shield_surface_h_adj: float = self.shield_surface.get_height() / 2
        self.shield_damage: float = 100.0

    def update(self, grid_space: GridSpace, get_group_ids_by_type: Callable[[EntityGroupIndex], set[UUID]], player: Player, dt: float) -> None:
        if player.cohere_yellow > 0:
            player.charge_shield(dt)
        if self.shield > 0:
            # Only process shield collisions for jellies that are within a cell range that can actually reach the player shield
            shield_cell_range: int = 2
            jelly_groups: set[UUID] = get_group_ids_by_type(EntityGroupIndex.JELLY)
            for jelly in grid_space.get_neighbors(player.position.x, player.position.y, shield_cell_range, jelly_groups):
                jelly_hitbox: Rect = jelly.hitbox
                # TODO implement infinite map and get rid of the ugly wrapping code
                if virtual_grid_c < 0 or virtual_grid_c >= self.world_specs.grid_width:
                    jelly_hitbox = self.get_virtual_wrapped_hitbox(jelly, virtual_grid_c)
                # find the closest point on the jelly's hitbox to the player's circular shield
                closest_point: Vector2 = Vector2(
                    max(
                        jelly_hitbox.left,
                        min(int(player.position.x), jelly_hitbox.right),
                    ),
                    max(
                        jelly_hitbox.top,
                        min(int(player.position.y), jelly_hitbox.bottom),
                    ),
                )
                if closest_point.distance_squared_to(player.position) < self.shield_radius_squared:
                    self.decrement_shield()
                    jelly.health -= self.shield_damage

    def charge_shield(self, dt) -> None:
        if self.shield < self.max_shield:
            self.current_shield_charge_cooldown -= dt
            if self.current_shield_charge_cooldown <= 0:
                self.current_shield_charge_cooldown = self.shield_charge_delay
                self.increment_shield()

    def increment_shield(self) -> None:
        self.shield += 1
        if self.shield > self.max_shield:
            self.shield = self.max_shield

    def decrement_shield(self) -> None:
        self.shield -= 1
        if self.shield < 0:
            self.shield = 0

    def get_shield_surface(self) -> Surface:
        shield_surface = Surface((self.shield_radius * 2, self.shield_radius * 2), SRCALPHA)
        circle(
            shield_surface,
            (
                255,
                255,
                0,
                self.shield_alpha_scaling + (self.shield * self.shield_alpha_scaling),
            ),
            shield_surface.get_rect().center,
            self.shield_radius,
        )
        return shield_surface

    #--------- Helper functions -----------

    def get_virtual_wrapped_hitbox(
        self, game_entity: GameEntity, virtual_grid_r: int
    ) -> Rect:
        virtual_hitbox: Rect = copy.deepcopy(game_entity.hitbox)
        if virtual_grid_r < 0:
            virtual_hitbox.center = (
                int(game_entity.position.x - self.world_specs.world_width),
                int(game_entity.position.y),
            )
        elif virtual_grid_r >= self.world_specs.grid_width:
            virtual_hitbox.center = (
                int(game_entity.position.x + self.world_specs.world_width),
                int(game_entity.position.y),
            )
        return virtual_hitbox

