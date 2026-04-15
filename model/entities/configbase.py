import dataclasses
import json
from abc import ABC
from dataclasses import dataclass


@dataclass
class ConfigBase(ABC):
    """
    Base class for config data classes.
    """
    @classmethod
    def from_dict(cls, data: dict) -> 'ConfigBase':
        """
        Creates a config from the provided dictionary. Extra keys will not throw errors and will simply not be
        present as attributes the returned data class.
        """
        field_names = {field.name for field in dataclasses.fields(cls)}
        return cls(**{k : v for k, v in data.items() if k in field_names})

    @classmethod
    def from_file(cls, file_path: str) -> 'ConfigBase':
        """
        Creates a config from the provided JSON file.
        :param file_path: The path to the JSON file from the project root directory.
        """
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return cls.from_dict(data)