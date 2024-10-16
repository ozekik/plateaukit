import glob
from pathlib import Path

import geopandas as gpd
import pandas as pd

from plateaukit.core.dataset import load_dataset


def _prebuild_dem(
    dataset_id: str,
    outfile: str = "/tmp/dem.parquet",
    tmpdir: str = "/tmp",
    split: int = 10,
):
    dataset = load_dataset(dataset_id)

    type = "dem"

    outfile_geojsonl = Path(tmpdir, f"{dataset_id}.dem.geojsonl")
    dataset.dem_to_geojson(
        outfile_geojsonl,
        seq=True,
        split=split,
        target_reduction=0.9,
        progress_messages={"description": f"Generating GeoJSONSeq files: {type}"},
    )

    # decoder = msgspec.json.Decoder(dict)

    if split > 1:
        filename_pattern = str(Path(tmpdir, "*.dem.*.geojsonl"))
    else:
        filename_pattern = str(Path(tmpdir, "*.dem.geojsonl"))

    tmp_file_paths = []

    for filename in glob.glob(filename_pattern):
        if f".{type}." not in filename:
            continue

        try:
            df = gpd.read_file(filename)
        except Exception:
            raise RuntimeError(f"Failed to read {filename}")
            # import shutil

            # # copy dir to /tmp for debugging:
            # shutil.copytree(tmpdir, "/tmp/failed")
            # raise

        df = df.drop(columns=["gmlId", "type"])
        # Explode
        df = df.explode(column="geometry")
        tmp_dest_path = str(Path(tmpdir, f"{filename}.parquet"))
        df.to_parquet(tmp_dest_path, index=False)

        tmp_file_paths.append(tmp_dest_path)

    df = None
    for filename in tmp_file_paths:
        subdf = gpd.read_parquet(filename)
        # NOTE: set ignore_index True for re-indexing
        df = (
            pd.concat([df, subdf], ignore_index=True)
            if df is not None
            else subdf
        )

    if df is None:
        raise RuntimeError("Data is empty")

    df.to_parquet(outfile, compression="zstd")
    # return df
