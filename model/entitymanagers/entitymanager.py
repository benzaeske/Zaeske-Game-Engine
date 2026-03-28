import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from controller.camerainterface import CameraInterface
from model.entities.entity import Entity
from model.entitymanagers.entitymanagerobserver import EntityManagerObserver
from model.world.modelcontext import ModelContext


class EntityManager(ABC):
    """
    Orchestrates frame actions and movement for a collection of entities.
    """
    def __init__(self):
        self._manager_id: UUID = uuid.uuid4()
        self._observers: list[EntityManagerObserver] = []

    @abstractmethod
    def frame_actions(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        """
        Actions to perform each frame. Actions can alter the state of the contained entity within this manager, other
        entities in the world space, or the player.
        """
        pass

    @abstractmethod
    def movement(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        """
        Performs any necessary movement of tracked entities.
        """
        pass

    def get_manager_id(self) -> UUID:
        return self._manager_id

    def add_observers(self, observers: list[EntityManagerObserver]) -> None:
        self._observers.extend(observers)

    def _notify_observers_entity_created(self, entity: Entity) -> None:
        """
        Entity manager implementations are responsible for notifying observers when new entities are created
        """
        for observer in self._observers:
            observer.notify_entity_created(entity)

    def _notify_observers_entity_deleted(self, entity: Entity) -> None:
        """
        Entity manager implementations are responsible for notifying observers when existing entities are deleted
        """
        for observer in self._observers:
            observer.notify_entity_deleted(entity)