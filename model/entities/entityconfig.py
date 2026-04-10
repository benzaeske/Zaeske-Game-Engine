from dataclasses import dataclass

from model.entities.configbase import ConfigBase
from model.entities.entitytype import EntityType


@dataclass
class EntityConfig(ConfigBase):
    entity_type: EntityType

    @classmethod
    def from_dict(cls, data: dict) -> ConfigBase:
        data['entity_type'] = EntityType(data['entity_type'])
        return super().from_dict(data)