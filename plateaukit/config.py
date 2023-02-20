import json
from collections import defaultdict
from pathlib import Path

from pydantic import BaseModel, PrivateAttr
from xdg import (
    # xdg_cache_home,
    # xdg_config_dirs,
    xdg_config_home,
    # xdg_data_dirs, # eg. [PosixPath('/usr/local/share'), PosixPath('/usr/share')]
    xdg_data_home,  # eg. /.local/share
    # xdg_runtime_dir,
    # xdg_state_home,
)

# print(xdg_config_home(), xdg_data_home())


class Config(BaseModel):
    _path: str = PrivateAttr()
    _data_dir: str = str(Path(xdg_data_home(), "plateaukit"))
    data = defaultdict(dict)

    def __init__(self, path=None):
        # Set path
        if path is None:
            config_dir = Path(xdg_config_home(), "plateaukit")
            if not config_dir.exists():
                config_dir.mkdir(parents=True)
            path = Path(config_dir, "config.json")
        self._path = str(Path(path).resolve())
        # Ensure data dir
        Path(self._data_dir).mkdir(parents=True, exist_ok=True)
        # Load on init
        with open(self._path, "r") as f:
            data = json.load(f)
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
