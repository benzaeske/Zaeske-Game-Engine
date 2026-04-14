from abc import ABC, abstractmethod
from uuid import UUID

from model.entities.enemies.enemy import Enemy
from model.entities.entity import Entity
from model.entities.items.projectileconfig import ProjectileConfig
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.modelcontext import ModelContext


class Projectile(Entity, ABC):
    def __init__(self, config: ProjectileConfig, manager_id: UUID):
        super().__init__(config, manager_id)
        self._damage: float = config.damage
        self._knockback_force: float = config.knockback_force
        self._cooldown: float = config.cooldown
        self._hit_cooldowns: dict[UUID, float] = {}
        self._cell_range: int = config.cell_range

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        self._process_entity_hit_cooldowns(dt)
        self._process_enemy_collisions(context, dt)

    def _process_entity_hit_cooldowns(self, dt) -> None:
        """
        Decrements all hit cooldowns and removes any that are finished
        """
        for entity_id in list(self._hit_cooldowns.keys()):
            self._hit_cooldowns[entity_id] -= dt
            if self._hit_cooldowns[entity_id] <= 0:
                self._hit_cooldowns.pop(entity_id)

    def _process_enemy_collisions(self, context: ModelContext, dt: float) -> None:
        """
        Checks for enemies that collide with this projectile. If any are found, decreases their hp and applies knockback
        according to the stats of this projectile. Will only attempt to detect collisions for enemy entities that are
        not being tracked in the hit cooldown list.
        """
        for enemy in context.grid_space.get_neighbors(self.get_position(), self._cell_range,
                                                      context.entity_repository.get_manager_ids(EntityManagerIndex.ENEMY)):
            if enemy.get_id() not in self._hit_cooldowns and self.collides_with(enemy, dt):
                enemy.update_hp(-self._damage)
                enemy.apply_knockback(self._knockback_force)
                self._hit_cooldowns[enemy.get_id()] = self._cooldown

    @abstractmethod
    def collides_with(self, enemy: Enemy, dt: float) -> bool:
        """
        Determines if this projectile collides with the given enemy in the current frame or at any point during the
        duration of the frame.
        :param enemy: The enemy to check for collisions
        :param dt: Time elapsed of the current frame
        :return: True when this projectile collides with the enemy, False otherwise
        """
        pass