import copy

from pygame import Rect, Vector2

from model.entities.shield import Shield
from model.entitymanagers.entitymanager import EntityManager, ModelContext
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex


class ShieldConfig:
    def __init__(self, shield_radius: float, shield_cell_detection_range: int) -> None:
        self.shield_radius = shield_radius
        self.shield_cell_detection_range = shield_cell_detection_range

class ShieldManager(EntityManager):
    def __init__(self, config: ShieldConfig):
        super().__init__()
        self._shield = Shield(self.get_manager_id(), config.shield_radius)
        self._shield_cell_detection_range = config.shield_cell_detection_range

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        if context.player.get_cohere_yellow():
            self._shield.charge_shield(dt)
        # Detect collisions with enemies
        if self._shield.get_shield_charge() > 0:
            for enemy in context.grid_space.get_entity_neighbors(self._shield, self._shield_cell_detection_range,
                                                                 context.get_manager_ids_by_type(EntityManagerIndex.ENEMY)):
                d, other_pos = calculate_shortest_distance_and_virtual_position(
                    self._shield.get_position(), enemy.get_position(), context.get_world_width()
                )
                enemy_hitbox: Rect = copy.deepcopy(enemy.get_hitbox())
                enemy_hitbox.center = other_pos
                # find the closest point on the enemy's hitbox to the circular shield
                closest_point: Vector2 = Vector2(
                    max(
                        enemy_hitbox.left,
                        min(int(context.get_player_position().x), enemy_hitbox.right),
                    ),
                    max(
                        enemy_hitbox.top,
                        min(int(context.get_player_position().y), enemy_hitbox.bottom),
                    ),
                )
                if closest_point.distance_squared_to(context.get_player_position()) < self._shield.get_shield_radius_squared():
                    self._shield.decrement_shield()
                    enemy.take_damage(self._shield.get_shield_damage())
        # Update the sprite at the very end after all increment/decrement operations have been performed
        self._shield.update_sprite()

    def movement(self, context: ModelContext, dt: float) -> None:
        self._shield.set_position(context.get_player_position())