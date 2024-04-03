import json
from collections import defaultdict
from pathlib import Path
from typing import Annotated, Any, DefaultDict

from platformdirs import user_config_dir, user_data_dir
from pydantic import __version__ as pydantic_version


def _get_data_items(entry: dict[str, str]):
    return dict(filter(lambda x: not x[0].startswith("_"), entry.items()))


def _sort_dataset_entry(entry: dict[str, str]):
    metadata_items = list(filter(lambda x: x[0].startswith("_"), entry.items()))
    data_items = list(filter(lambda x: not x[0].startswith("_"), entry.items()))

    metadata_items.sort(key=lambda x: x[0])
    data_items.sort(key=lambda x: x[0])

    return dict(metadata_items + data_items)


if pydantic_version.startswith("1"):
    from pydantic import BaseModel, Field, PrivateAttr, validator

    class ConfigV1(BaseModel):
        """Class representing the PlateauKit config."""

        path: str = Field(default=None)
        _data_dir: str = PrivateAttr(
            default=str(Path(user_data_dir("plateaukit"), "data"))
        )
        datasets: Any = Field(default_factory=lambda: defaultdict(dict))

        @validator("path", pre=True, always=True)
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
                data = self.json(
                    indent=2, exclude_none=True, exclude={"path"}, ensure_ascii=False
                )
                # TODO: remove
                # print("Saved:", data)
                f.write(data)

else:
    from pydantic import BaseModel, Field, PrivateAttr, field_validator

    class ConfigV2(BaseModel):
        """Class representing the PlateauKit config."""

        path: str = Field(default=None, validate_default=True)
        _data_dir: str = PrivateAttr(
            default=str(Path(user_data_dir("plateaukit"), "data"))
        )
        datasets: DefaultDict[str, Annotated[dict, Field(default_factory=dict)]] = (
            Field(default_factory=lambda: defaultdict(dict))
        )

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
                data = self.model_dump_json(
                    indent=2, exclude_none=True, exclude={"path"}
                )
                # TODO: remove
                # print("Saved:", data)
                f.write(data)


try:
    Config = ConfigV2
except NameError:
    Config = ConfigV1
