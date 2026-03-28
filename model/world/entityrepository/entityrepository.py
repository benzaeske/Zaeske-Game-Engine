from uuid import UUID

from controller.camera import Camera
from model.entities.fish.fishconfigv1 import FishType
from model.entitymanagers.enemies.enemymanager import EnemyManager
from model.entitymanagers.entitymanager import EntityManager
from model.entitymanagers.fish.school import School
from model.entitymanagers.items.itemmanager import ItemManager
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.entityrepository.entityrepositoryinterface import EntityRepositoryInterface
from model.entitymanagers.entitymanagerobserver import EntityManagerObserver
from model.world.modelcontext import ModelContext


class EntityRepository(EntityRepositoryInterface):
    def __init__(self) -> None:
        super().__init__()
        self._entity_managers: dict[UUID, EntityManager] = {}
        self._entity_manager_indexes: dict[EntityManagerIndex, set[UUID]] = {index: set() for index in EntityManagerIndex}
        self._manager_observers: list[EntityManagerObserver] = []

    def add_entity_manager(self, entity_manager: EntityManager) -> None:
        if entity_manager.get_manager_id() not in self._entity_managers:
            entity_manager.add_observers(self._manager_observers)
            self._entity_managers[entity_manager.get_manager_id()] = entity_manager
            self.index_entity_manager(entity_manager)
        else:
            raise RuntimeError(f"Entity manager {entity_manager.get_manager_id()} already registered")

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
        elif isinstance(entity_manager, ItemManager):
            self._entity_manager_indexes[EntityManagerIndex.ITEM].add(entity_manager.get_manager_id())

    def remove_entity_manager(self, manager_id: UUID) -> None:
        self._entity_managers.pop(manager_id, None)
        # Remove the manager id from any indexes it was associated with
        for index, ids in self._entity_manager_indexes.items():
            if manager_id in ids:
                ids.remove(manager_id)

    def get_manager_ids(self, index: EntityManagerIndex) -> set[UUID]:
        return self._entity_manager_indexes.get(index, set())

    def frame_actions(self, context: ModelContext, camera: Camera, dt: float) -> None:
        for entity_manager in self._entity_managers.values():
            entity_manager.frame_actions(context, camera, dt)

    def move_entities(self, context: ModelContext, camera: Camera, dt: float) -> None:
        for entity_manager in self._entity_managers.values():
            entity_manager.movement(context, camera, dt)

    def register_entity_manager_observer(self, observer: EntityManagerObserver) -> None:
        """
        Adds the provided class to the list of entity manager observers on this entity repository. Any entity managers
        created will send notifications to the observer. See EntityManagerObserver for more details.
        """
        self._manager_observers.append(observer)