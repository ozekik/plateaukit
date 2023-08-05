import json
from collections import defaultdict
from pathlib import Path

from pydantic import BaseModel, PrivateAttr
from platformdirs import (
    user_config_dir,
    user_data_dir,
)

# print(user_config_dir(), user_data_dir())


class Config(BaseModel):
    _path: str = PrivateAttr()
    _data_dir: str = str(user_data_dir("plateaukit"))
    data = defaultdict(dict)

    def __init__(self, path=None):
        # Set path
        if path is None:
            config_dir = Path(user_config_dir("plateaukit"))
            if not config_dir.exists():
                config_dir.mkdir(parents=True)
            path = Path(config_dir, "config.json")
        self._path = str(Path(path).resolve())
        # Ensure data dir
        Path(self._data_dir).mkdir(parents=True, exist_ok=True)
        # Load on init
        if Path(self._path).exists():
            with open(self._path, "r") as f:
                data = json.load(f)
        else:
            data = {}
        super().__init__(**data)
        # TODO: fix
        self.data = defaultdict(dict, self.data)

    def get_path(self):
        return self._path

    @property
    def data_dir(self):
        return self._data_dir

    def save(self):
        with open(self._path, "w") as f:
            data = self.json(indent=2, ensure_ascii=False)
            # TODO: remove
            print("Saved:", data)
            f.write(data)
