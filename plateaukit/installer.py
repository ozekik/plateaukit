import os
from os import PathLike
from pathlib import Path

from plateaukit.config import Config
from plateaukit.download import downloader


def is_dataset_installed(dataset_id, format):
    config = Config()
    path = config.datasets.get(dataset_id, {}).get(format)
    return True if path else False
    # return path and Path(path).exists()


def install_dataset(
    dataset_id: str, format: str, local: str | PathLike, force: bool = False
):
    """Download and install PLATEAU datasets."""

    from plateaukit.download import city_list

    if not dataset_id:
        raise RuntimeError("Missing dataset_id")

    city = next(filter(lambda x: x["dataset_id"] == dataset_id, city_list), None)

    if not city:
        raise RuntimeError("Invalid dataset name")

    if local:
        local = Path(local).resolve()
        if not local.exists():
            raise RuntimeError("Local file not found")
        # print(local)
        config = Config()
        config.datasets[dataset_id][format] = local
        config.save()
        return
    else:
        # Abort if a dataset is already installed
        installed = is_dataset_installed(dataset_id, format)
        if not force and installed:
            RuntimeError(
                f'ERROR: Dataset "{dataset_id}" ({format}) is already installed'
            )
            return

        # TODO: Check beforehand if specified format is available in city_list
        resource_id = city[format]

        # print(dataset_id, resource_id)

        config = Config()
        destfile_path = downloader.download_resource(resource_id, dest=config.data_dir)
        config.datasets[dataset_id][format] = destfile_path
        config.save()
        return


def uninstall_dataset(dataset_id: str, format: str, keep_files: bool = False):
    """Uninstall PLATEAU datasets."""

    if not keep_files:
        config = Config()
        path = config.datasets[dataset_id][format]
        if not path:
            raise RuntimeError("Missing files in record")
        os.remove(path)

    config = Config()
    del config.datasets[dataset_id][format]
    if len(config.datasets[dataset_id].items()) == 0:
        del config.datasets[dataset_id]
    config.save()