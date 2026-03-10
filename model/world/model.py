from uuid import UUID

from pygame.key import ScancodeWrapper

from model.entitymanagers.entitymanager import EntityManager, ModelContext
from model.player.player import Player
from model.world.entityrepository.entityrepository import EntityRepository
from model.world.gridspace.gridspace import GridSpace


class Model:
    def __init__(self, grid_cell_size: float, player: Player):
        self._grid_space: GridSpace = GridSpace(grid_cell_size)
        self._entity_repository: EntityRepository = EntityRepository()
        self._player: Player = player
        self._model_context: ModelContext = ModelContext(
            self._grid_space,
            self._entity_repository,
            self._player
        )

    def update(self, key_presses: ScancodeWrapper, dt: float) -> None:
        self._player.update(self._grid_space, self._entity_repository, dt)
        self._entity_repository.perform_frame_actions(self._model_context, dt)
        self._player.move_player(key_presses, dt)
        self._entity_repository.move_entities(self._model_context, dt)

    def add_entity_manager(self, entity_manager: EntityManager) -> None:
        self._entity_repository.add_entity_manager(entity_manager)

    def remove_entity_manager(self, manager_id: UUID) -> None:
        self._entity_repository.remove_entity_manager(manager_id)

    def get_model_context(self) -> ModelContext:
        return self._model_context