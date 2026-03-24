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
        """
        Performs actions on the observer when an entity is created by an entity manager.
        """
        pass

    @abstractmethod
    def notify_entity_deleted(self, entity: Entity):
        """
        Performs actions on the observer when an entity is deleted by an entity manager.
        """
        pass


