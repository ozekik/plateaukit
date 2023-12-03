import json
from collections import defaultdict
from pathlib import Path
import re
from typing import Annotated, Any, DefaultDict, Optional

from platformdirs import user_config_dir, user_data_dir
from pydantic import BaseModel, Field, PrivateAttr, field_validator

# print(user_config_dir(), user_data_dir())


class Config(BaseModel):
    """Class representing the PlateauKit config."""

    path: str = Field(default=None, validate_default=True)
    _data_dir: str = PrivateAttr(default=str(Path(user_data_dir("plateaukit"), "data")))
    datasets: Optional[
        DefaultDict[str, Annotated[dict, Field(default_factory=dict)]]
    ] = None

    @field_validator("path", mode="before")
    @classmethod
    def validate_path(cls, path):
        if path is None:
            config_dir = Path(user_config_dir("plateaukit"))
            if not config_dir.exists():
                config_dir.mkdir(parents=True)
            path = Path(config_dir, "config.json")

        _path = str(Path(path).resolve())
        return _path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Ensure data directory exists
        Path(self._data_dir).mkdir(parents=True, exist_ok=True)

        # Load config on init
        if Path(self.path).exists():
            with open(self.path, "r") as f:
                try:
                    config_content = json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    if f.read() == "":
                        config_content = {}
                    else:
                        raise
        else:
            config_content = {}

        # TODO: fix
        self.datasets = defaultdict(dict, config_content.get("datasets", {}))

    @property
    def data_dir(self):
        return self._data_dir

    def save(self):
        with open(self.path, "w") as f:
            data = self.model_dump_json(indent=2, exclude_none=True, exclude=["path"])
            # TODO: remove
            # print("Saved:", data)
            f.write(data)
