from typing import Optional
from uuid import UUID

from pygame.key import ScancodeWrapper

from model.entity.entitymanager import EntityManager, ModelContext
from model.entity.entitymanagerobserver import EntityManagerObserver
from model.player.player import Player
from model.world.entityrepository.entityrepository import EntityRepository
from model.world.entityrepository.entityrepositoryinterface import EntityRepositoryInterface
from model.world.gridspace.gridspace import GridSpace
from model.world.gridspace.gridspaceinterface import GridSpaceInterface


class Model:
    def __init__(self, grid_cell_size: float):
        self._grid_space: GridSpace = GridSpace(grid_cell_size)
        self._entity_repository: EntityRepository = EntityRepository()
        self._player: Optional[Player] = None
        self._model_context: ModelContext = ModelContext(self._grid_space, self._entity_repository, self._player)

    def register_player(self, player: Player) -> None:
        """
        Tracks the provided player on the model.
        """
        self._player = player
        self._model_context.player = player

    def update(self, key_presses: ScancodeWrapper, dt: float) -> None:
        """
        Updates the model for a single frame.
        """
        self._player.frame_actions(self._grid_space, self._entity_repository, dt)
        self._entity_repository.perform_frame_actions(self._model_context, dt)
        self._player.move(key_presses, dt)
        self._entity_repository.move_entities(self._model_context, dt)

    def add_entity_manager(self, entity_manager: EntityManager) -> None:
        self._entity_repository.add_entity_manager(entity_manager)

    def remove_entity_manager(self, manager_id: UUID) -> None:
        self._entity_repository.remove_entity_manager(manager_id)

    def register_entity_manager_observer(self, observer: EntityManagerObserver) -> None:
        """
        Adds the provided class to the list of entity manager observers in the model. Any entity managers created will
        send notifications to the observer. See EntityManagerObserver for more details.
        """
        self._entity_repository.register_entity_manager_observer(observer)

    def get_model_context(self) -> ModelContext:
        return self._model_context

    def get_grid_space(self) -> GridSpaceInterface:
        return self._grid_space

    def get_entity_repository(self) -> EntityRepositoryInterface:
        return self._entity_repository