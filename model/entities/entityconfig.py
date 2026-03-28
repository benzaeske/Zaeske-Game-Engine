from dataclasses import dataclass

from model.entities.configbase import ConfigBase
from model.entities.entitytype import EntityType


@dataclass
class EntityConfig(ConfigBase):
    entity_type: EntityType