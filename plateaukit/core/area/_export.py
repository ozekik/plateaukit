from pathlib import Path
from typing import TextIO

import pandas as pd

from plateaukit.config import Config
from plateaukit.logger import logger


def to_geojson(self, file: str | None = None):
    """Export the area in GeoJSON format."""

    # TODO: Support GeoJSONSeq

    data = self.gdf.to_json(ensure_ascii=False)

    if file is not None:
        with open(file, "w") as f:
            f.write(data)
    else:
        return data


def to_cityjson(
    self,
    file: str | TextIO,
    *,
    types: list[str] | None = None,
    ground: bool = False,
    seq: bool = False,
    target_epsg: int = 4326,
):
    """Export the area in CityJSON format."""

    # TODO: Support IOBase as file

    from plateaukit import Dataset

    if self._datasets is None:
        raise RuntimeError("Missing dataset information")

    types = list(self.layers.keys()) if types is None else types

    # TODO: Support non-building types
    # selection = self.gdf["buildingId"].tolist()
    selection = sum([layer.gdf["gmlId"].tolist() for layer in self.layers.values()], [])
    logger.debug(selection)

    config = Config()

    for dataset_id in self._datasets:
        # co_parquet_path = Path(config.data_dir, f"{dataset_id}.cityobjects.parquet")
        co_parquet_path = config.datasets.get(dataset_id, {}).get("cityobjects", None)
        co_parquet_path = Path(co_parquet_path) if co_parquet_path else None

        if seq and co_parquet_path is not None and target_epsg == 4326:
            selection = sum(
                [layer.gdf["gmlId"].tolist() for layer in self.layers.values()], []
            )
            df = pd.read_parquet(co_parquet_path)
            # Get rows where df._id in selection:
            df = df[df._id.isin(selection)]
            # Write value of `cityjson` row of each row to a line in the file.
            assert target_epsg == 4326
            cjseq_header = (
                '{"type":"CityJSON","version":"2.0","transform":{"scale":[1.0,1.0,1.0],"translate":[0.0,0.0,0.0]},'
                + f'"metadata":{{"referenceSystem":"https://www.opengis.net/def/crs/EPSG/0/{target_epsg}"}},"vertices":[]}}'
            )
            if isinstance(file, str):
                with open(file, "w") as f:
                    f.write(cjseq_header + "\n")
                    for row in df.itertuples():
                        f.write(str(row.cityjson) + "\n")
            else:
                file.write(cjseq_header + "\n")
                for row in df.itertuples():
                    file.write(str(row.cityjson) + "\n")
                file.seek(0)
        else:
            if not isinstance(file, str):
                raise ValueError("File-like object is not supported for direct export")

            dataset = Dataset(dataset_id)

            dataset.to_cityjson(
                file,
                types=types,
                ground=ground,
                selection=selection,
                target_epsg=target_epsg,
                seq=seq,
            )
