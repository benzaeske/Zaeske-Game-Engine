from uuid import UUID

from model.entities.fishconfig import FishType
from model.entitymanagers.enemymanager import EnemyManager
from model.entitymanagers.entitymanager import EntityManager
from model.entitymanagers.jellyfishswarm import JellyfishSwarm
from model.entitymanagers.school import School
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.entityrepository.entityrepositoryinterface import EntityRepositoryInterface
from model.world.modelcontext import ModelContext


class EntityRepository(EntityRepositoryInterface):
    def __init__(self) -> None:
        super().__init__()
        self._entity_managers: dict[UUID, EntityManager] = {}
        self._entity_manager_indexes: dict[EntityManagerIndex, set[UUID]] = {index: set() for index in EntityManagerIndex}

    def add_entity_manager(self, entity_manager: EntityManager) -> None:
        if entity_manager.get_manager_id() not in self._entity_managers:
            self._entity_managers[entity_manager.get_manager_id()] = entity_manager
            self.index_entity_manager(entity_manager)

    def index_entity_manager(self, entity_manager: EntityManager) -> None:
        if isinstance(entity_manager, EnemyManager):
            self._entity_manager_indexes[EntityManagerIndex.ENEMY].add(entity_manager.get_manager_id())
        elif isinstance(entity_manager, School):
            self._entity_manager_indexes[EntityManagerIndex.FISH].add(entity_manager.get_manager_id())
            match entity_manager.get_fish_type():
                case FishType.RED:
                    self._entity_manager_indexes[EntityManagerIndex.RED_FISH].add(entity_manager.get_manager_id())
                case FishType.YELLOW:
                    self._entity_manager_indexes[EntityManagerIndex.YELLOW_FISH].add(entity_manager.get_manager_id())
                case FishType.GREEN:
                    self._entity_manager_indexes[EntityManagerIndex.GREEN_FISH].add(entity_manager.get_manager_id())

    def remove_entity_manager(self, manager_id: UUID) -> None:
        self._entity_managers.pop(manager_id, None)
        # Remove the manager id from any indexes it was associated with
        for index, ids in self._entity_manager_indexes.items():
            if manager_id in ids:
                ids.remove(manager_id)

    def get_manager_ids(self, index: EntityManagerIndex) -> set[UUID]:
        return self._entity_manager_indexes.get(index, set())

    def perform_frame_actions(self, context: ModelContext, dt: float) -> None:
        for entity_manager in self._entity_managers.values():
            entity_manager.frame_actions(context, dt)

    def move_entities(self, context: ModelContext, dt: float) -> None:
        for entity_manager in self._entity_managers.values():
            entity_manager.movement(context, dt)