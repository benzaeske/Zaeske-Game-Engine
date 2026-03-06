from uuid import UUID

from pygame.key import ScancodeWrapper

from model.entities.fishconfig import FishType
from model.entitymanagers.enemymanager import EnemyManager
from model.entitymanagers.entitymanager import EntityManager, ModelContext
from model.entitymanagers.jellyfishswarm import JellyfishSwarm
from model.entitymanagers.school import School

from model.player.player import Player
from model.world.entitymanagerindex import EntityManagerIndex
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class Model:
    def __init__(self, world_specs: WorldSpecs, player: Player):
        self._world_specs = world_specs
        self._grid_space: GridSpace = GridSpace(world_specs)
        self._entity_managers: dict[UUID, EntityManager] = {}
        self._entity_manager_indexes: dict[EntityManagerIndex, set[UUID]] = {index: set() for index in EntityManagerIndex}
        self._player: Player = player
        self._frame_action_context: ModelContext = ModelContext(
            self._grid_space,
            self._entity_manager_indexes,
            self._player,
            self._world_specs
        )

    def update(self, key_presses: ScancodeWrapper, dt: float) -> None:
        self._player.update(self._grid_space, self._entity_manager_indexes, dt)
        self.perform_entity_frame_actions(dt)
        self._player.move_player(key_presses, dt)
        self.move_entities(dt)

    def add_entity_manager(self, entity_manager: EntityManager) -> None:
        self._entity_managers[entity_manager.get_manager_id()] = entity_manager
        self.index_entity_manager(entity_manager)

    def index_entity_manager(self, entity_manager: EntityManager) -> None:
        if isinstance(entity_manager, JellyfishSwarm):
            self._entity_manager_indexes[EntityManagerIndex.JELLY].add(entity_manager.get_manager_id())
        elif isinstance(entity_manager, EnemyManager):
            self._entity_manager_indexes[EntityManagerIndex.ENEMY].add(entity_manager.get_manager_id())
        elif isinstance(entity_manager, School):
            match entity_manager.get_fish_type():
                case FishType.RED:
                    self._entity_manager_indexes[EntityManagerIndex.RED_FISH].add(entity_manager.get_manager_id())
                case FishType.YELLOW:
                    self._entity_manager_indexes[EntityManagerIndex.YELLOW_FISH].add(entity_manager.get_manager_id())
                case FishType.GREEN:
                    self._entity_manager_indexes[EntityManagerIndex.GREEN_FISH].add(entity_manager.get_manager_id())

    def remove_entity_manager(self, manager_id: UUID) -> None:
        self._entity_managers.pop(manager_id)
        # Remove the manager id from any indexes it was associated with
        for index, ids in self._entity_manager_indexes.items():
            if manager_id in ids:
                ids.remove(manager_id)

    def perform_entity_frame_actions(self, dt) -> None:
        # TODO process frame actions for projectiles before enemies
        for entity_manager in self._entity_managers.values():
            entity_manager.frame_actions(self._frame_action_context, dt)

    def move_entities(self, dt) -> None:
        for entity_manager in self._entity_managers.values():
            entity_manager.movement(self._frame_action_context, dt)

    def get_player(self) -> Player:
        return self._player



