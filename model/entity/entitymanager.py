import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from model.entity.entity import Entity
from model.entity.entitymanagerobserver import EntityManagerObserver
from model.world.modelcontext import ModelContext


class EntityManager(ABC):
    """
    Orchestrates frame actions and movement for one or many entity.
    """
    def __init__(self):
        self._manager_id: UUID = uuid.uuid4()
        self._observers: list[EntityManagerObserver] = []

    @abstractmethod
    def frame_actions(self, context: ModelContext, dt: float) -> None:
        """
        Actions to perform each frame. Actions can alter the state of the contained entity within this manager, other
        entity in the world space, or the player.
        """

    @abstractmethod
    def movement(self, context: ModelContext, dt: float) -> None:
        """
        Performs any necessary movement of tracked entity.
        """

    def get_manager_id(self) -> UUID:
        return self._manager_id

    def add_observer(self, observer: EntityManagerObserver) -> None:
        self._observers.append(observer)

    def notify_observers_entity_created(self, entity: Entity) -> None:
        for observer in self._observers:
            observer.notify_entity_created(entity)

    def notify_observers_entity_deleted(self, entity: Entity) -> None:
        for observer in self._observers:
            observer.notify_entity_deleted(entity)