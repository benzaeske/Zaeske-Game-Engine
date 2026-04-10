from model.player.playerconfig import PlayerConfig


class PlayerConfigurations:
    """
    Source of truth for player configurations and settings in the model and sprites/animations in the view
    """
    def __init__(self) -> None:
        self._player_config: PlayerConfig
        self._load_player_config()

    def _load_player_config(self) -> None:
        # Hard coded for now until I decide what I want to do with player classes/types
        self._player_config = PlayerConfig.from_file('assets/playerconfigurations/turtle.json')

    def get_config(self) -> PlayerConfig:
        """
        Only one type for now until I decide what to do with player classes/types
        """
        return self._player_config