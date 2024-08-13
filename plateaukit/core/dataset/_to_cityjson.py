import re
import zipfile
from os import PathLike
from pathlib import Path, PurePosixPath
from typing import Literal

from plateaukit.config import Config
from plateaukit.exporters.cityjson.parallel_writer import ParallelWriter
from plateaukit.exporters.cityjson.writer import CityJSONWriter
from plateaukit.logger import logger
from plateaukit.readers.citygml.reader import CityGMLReader
from plateaukit.transformers.filter_lod import LODFilteringTransformer
from plateaukit.transformers.reprojection import ReprojectionTransformer


def to_cityjson(
    self,
    outfile: str | PathLike,
    *,
    types: list[str] = ["bldg"],
    object_types=None,  # TODO: Handle this
    lod_mode: Literal["highest", "all", "values"] = "highest",
    lod_values: list[str] | None = None,
    ground: bool = False,
    seq: bool = False,
    split: int = 1,
    selection: list[str] | None = None,
    target_epsg: int | None = None,
    **kwargs,
):
    """Export CityJSON from PLATEAU datasets.

    Args:
        outfile: Output file path.
        types: CityGML feature types.
        split: Split the output into specified number of files.
        seq: Export CityJSONSeq.
        **kwargs: Keyword arguments for the generator.
    """
    # NOTE: (check) generators requires multiprocessing at the moment, unavailable in pyodide
    # params = {}

    # if precision:
    #     params["precision"] = precision

    if not self.dataset_id:
        raise Exception("Missing dataset_id")

    config = Config()
    record = config.datasets[self.dataset_id]

    if "citygml" not in record:
        raise Exception("Missing CityGML data")

    file_path = Path(record["citygml"])

    infiles = []

    for type in types:
        # TODO: fix
        pat = re.compile(rf".*udx\/{type}\/.*\.gml$")

        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path) as f:
                namelist = f.namelist()
                targets = list(filter(lambda x: pat.match(x), namelist))

                if not targets:
                    raise RuntimeError(
                        f"Data type '{type}' not found in '{self.dataset_id}'"
                    )

                # NOTE: zipfs requires POSIX path
                infiles += [str(PurePosixPath("/", target)) for target in targets]
        else:
            infiles += [str(Path(file_path, "udx", type, "*.gml"))]

        logger.debug([types, infiles, outfile])

    # Sort by a part of filename to group by areas; TODO: Update this
    # try:
    #     infiles = sorted(infiles, key=lambda x: Path(x).stem.split("_")[0])
    # except:
    #     infiles = sorted(infiles)
    infiles = sorted(infiles)

    # Codelists
    codelist_infiles = None
    if not zipfile.is_zipfile(file_path):
        # TODO: Test support for non-zip codelists
        codelist_infiles = [str(Path(file_path, "codelists", "*.xml"))]

    reader = CityGMLReader()

    readable = reader.scan_files(
        infiles,
        codelist_infiles=codelist_infiles,
        zipfile=file_path,
        selection=selection,
    )

    # TODO: Fix typing
    transformers: list = [
        LODFilteringTransformer(mode=lod_mode, values=lod_values),
    ]

    if target_epsg:
        transformers.append(ReprojectionTransformer(target_epsg=target_epsg))

    for transformer in transformers:
        readable = transformer.transform(readable)

    parallel_writer = ParallelWriter(CityJSONWriter)
    parallel_writer.transform(readable, str(outfile), seq=seq, split=split)

    # generators.cityjson.cityjson_from_citygml(
    #     infiles,
    #     outfile,
    #     split=split,
    #     zipfile=file_path,
    #     lod=lod,
    #     use_highest_lod=use_highest_lod,
    #     ground=ground,
    #     seq=seq,
    #     codelist_infiles=codelist_infiles,
    #     selection=selection,
    #     target_epsg=target_epsg,
    #     **kwargs,
    # )
