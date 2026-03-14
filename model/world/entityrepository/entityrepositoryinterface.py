from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from uuid import UUID

from model.world.entityrepository.entitymanagerindex import EntityManagerIndex

if TYPE_CHECKING:
    from model.entities.entitymanagers.entitymanager import EntityManager


class EntityRepositoryInterface(ABC):
    """
    Defines publicly accessible functionality for the entity repository.
    """
    def __init__(self):
        pass

    @abstractmethod
    def add_entity_manager(self, entity_manager: EntityManager) -> None:
        """
        Adds an entity manager to the repository.
        """
        pass

    @abstractmethod
    def remove_entity_manager(self, manager_id: UUID) -> None:
        """
        Removes an entity manager with the given id from the repository.
        """
        pass

    @abstractmethod
    def get_manager_ids(self, index: EntityManagerIndex) -> set[UUID]:
        """
        Gets all manager ids corresponding to the given index. Returns an empty set if none are found.
        """
        pass

