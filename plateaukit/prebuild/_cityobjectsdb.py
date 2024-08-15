import glob
import json
from pathlib import Path

import pandas as pd

from plateaukit.core.dataset import load_dataset


def _prebuild_cityobjects_db(
    dataset_id: str,
    outfile: str = "/tmp/cityobjects.parquet",
    types: list[str] = ["bldg", "tran", "brid"],
    tmpdir: str = "/tmp",
    split: int = 10,
):
    dataset = load_dataset(dataset_id)

    for type in types:
        outfile_cityjsonl = Path(tmpdir, f"{dataset_id}.{type}.city.jsonl")
        dataset.to_cityjson(
            outfile_cityjsonl,
            types=[type],
            seq=True,
            split=split,
            progress_messages={"description": f"Generating CityJSONSeq files: {type}"},
            # simple_output=simple_output,
        )

    # decoder = msgspec.json.Decoder(dict)

    buffer = []

    if split > 1:
        filename_pattern = str(Path(tmpdir, "*.city.*.jsonl"))
    else:
        filename_pattern = str(Path(tmpdir, "*.city.jsonl"))

    for type in types:
        for filename in glob.glob(filename_pattern):
            if f".{type}." not in filename:
                continue

            with open(filename, "r") as f:
                next(f)  # Skip the first line

                for i, line in enumerate(f):
                    cityjson = line.strip()
                    # data = decoder.decode(cityjson)
                    data = json.loads(cityjson)

                    objects = [
                        {
                            "_id": k,
                            "cityjson": cityjson,
                        }
                        for k in data["CityObjects"].keys()
                    ]
                    buffer += objects

    # TODO: Avoid having entire buffer in memory
    # print(buffer)
    # convert buffer to DataFrame. both `_id`, `cityjson` columns are str type
    df = pd.DataFrame(buffer, dtype=str)
    # print(df.head())
    df.to_parquet(outfile, compression="zstd")

    # return df
