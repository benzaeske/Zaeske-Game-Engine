from model.player.playerinterface import PlayerInterface
from model.world.entityrepository.entityrepositoryinterface import EntityRepositoryInterface
from model.world.gridspace.gridspaceinterface import GridSpaceInterface


class ModelContext:
    """
    Provides controlled access into the current state of the world model. Other classes that need to interact with the
    model should do so through this context.
    """
    def __init__(
            self,
            grid_space: GridSpaceInterface,
            entity_repository: EntityRepositoryInterface,
            player: PlayerInterface
    ) -> None:
        self.grid_space: GridSpaceInterface = grid_space
        self.entity_repository: EntityRepositoryInterface = entity_repository
        self.player: PlayerInterface = player

