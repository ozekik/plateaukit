from __future__ import annotations

import os
import sys
from os import PathLike
from pathlib import Path
from typing import Optional

from plateaukit.config import Config
from plateaukit.download import downloader


def is_dataset_installed(dataset_id, format):
    config = Config()
    path = config.datasets.get(dataset_id, {}).get(format)
    return True if path else False
    # return path and Path(path).exists()


def list_installed_datasets():
    config = Config()
    return list(config.datasets.keys())


def install_dataset(
    dataset_id: str,
    format: str = "citygml",
    local: str | PathLike | None = None,
    force: bool = False,
):
    """Download and install PLATEAU datasets."""

    from plateaukit.download import city_list

    if not dataset_id:
        raise RuntimeError("Missing dataset_id")

    city = next(filter(lambda x: x["dataset_id"] == dataset_id, city_list), None)

    if not city:
        raise RuntimeError("Invalid dataset name")

    installed = is_dataset_installed(dataset_id, format)

    # Abort if a dataset is already installed
    if not force and installed:
        raise RuntimeError(
            f'ERROR: Dataset "{dataset_id}" ({format}) is already installed'
        )

    if local:
        local = Path(local).resolve()

        if not local.exists():
            raise RuntimeError("Local file not found")

        config = Config()
        config.datasets[dataset_id][format] = local
        config.save()

        return
    else:
        # TODO: Check beforehand if specified format is available in city_list
        resource_id = city.get(format, None)

        if not resource_id:
            raise RuntimeError(f"Format '{format}' is not available for '{dataset_id}'")

        config = Config()
        destfile_path = downloader.download_resource(resource_id, dest=config.data_dir)

        config.datasets[dataset_id][format] = destfile_path
        config.save()

        return


def uninstall_dataset(
    dataset_id: str, formats: Optional[list[str]] = None, keep_files: bool = False
):
    """Uninstall PLATEAU datasets."""

    config = Config()
    formats = formats or list(config.datasets[dataset_id].keys())

    if not keep_files:
        paths = []
        for format in formats:
            path = config.datasets[dataset_id].get(format)
            if not path:
                raise RuntimeError(f"Missing files in record for '{format}'")
            paths.append(path)
            try:
                os.remove(path)
            except Exception as e:
                print(e, file=sys.stderr)

    for format in formats:
        if format in config.datasets[dataset_id]:
            del config.datasets[dataset_id][format]

    if len(config.datasets[dataset_id].items()) == 0:
        del config.datasets[dataset_id]

    config.save()
