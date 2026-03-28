from model.entities.entityconfig import EntityConfig
from model.entities.entitytype import EntityType
from model.entities.fish.fishconfig import FishConfig


class EntityConfigurations:
    """
    Source of truth entity stats in the model and sprite/animation assets in the view. Loads all known entity
    configurations at the beginning of the game.
    """
    def __init__(self):
        self._entity_configs: dict[EntityType, EntityConfig] = {}
        self._load_entity_configs()

    def _load_entity_configs(self):
        self._entity_configs[EntityType.RED_FISH] = FishConfig.from_file('assets/entityconfigurations/red_fish.json')
        self._entity_configs[EntityType.YELLOW_FISH] = FishConfig.from_file('assets/entityconfigurations/yellow_fish.json')
        self._entity_configs[EntityType.GREEN_FISH] = FishConfig.from_file('assets/entityconfigurations/green_fish.json')
        self._entity_configs[EntityType.RED_JELLYFISH] = FishConfig.from_file('assets/entityconfigurations/red_jellyfish.json')

    def get_entity_config(self, entity_type: EntityType) -> EntityConfig:
        if entity_type in self._entity_configs:
            return self._entity_configs.get(entity_type)
        else:
            raise ValueError(f"Entity type {entity_type} has no loaded configuration.")