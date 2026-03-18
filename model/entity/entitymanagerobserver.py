from abc import ABC, abstractmethod

from model.entity.entity import Entity


class EntityManagerObserver(ABC):
    """
    Observer pattern for watching entity managers
    """
    def __init__(self):
        pass

    @abstractmethod
    def notify_entity_created(self, entity: Entity):
        pass

    @abstractmethod
    def notify_entity_deleted(self, entity: Entity):
        pass


