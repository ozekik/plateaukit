import re
import zipfile
from os import PathLike
from pathlib import Path, PurePosixPath

from plateaukit.config import Config
from plateaukit.logger import logger


def to_geojson(
    self,
    outfile: str | PathLike,
    *,
    types: list[str] = ["bldg"],
    altitude: bool = True,
    include_type: bool = False,
    seq=False,
    split: int = 1,
    **kwargs,
):
    """Export GeoJSON from PLATEAU datasets.

    Args:
        outfile: Output file path.
        types: CityGML object types to include.
        split: Split the output into specified number of files.
        **kwargs: Keyword arguments for the generator.
    """
    # NOTE: exporters requires multiprocessing at the moment, unavailable in pyodide
    from plateaukit import exporters

    if not self.dataset_id:
        raise Exception("Missing dataset_id")

    if not types:
        raise Exception("Missing object types")

    # NOTE: this is intentional but to be refactored in the future
    config = Config()
    record = config.datasets[self.dataset_id]

    if "citygml" not in record:
        raise Exception("Missing CityGML data")
    file_path = Path(record["citygml"])

    infiles = []

    # TODO: Refactor
    for type in types:
        # TODO: Fix
        pat = re.compile(rf".*udx\/{type}\/.*\.gml$")
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path) as f:
                namelist = f.namelist()
                targets = list(filter(lambda x: pat.match(x), namelist))
                # print(targets)

                if not targets:
                    raise RuntimeError(
                        f"Data type '{type}' not found in '{self.dataset_id}'"
                    )

                # NOTE: zipfs requires POSIX path
                infiles += [str(PurePosixPath("/", target)) for target in targets]

                # f.extractall(tdir, members=targets)
                # infiles += [
                #     str(Path(tdir, Path(file_path).stem, "udx", type, "*.gml"))
                # ]
        else:
            infiles += [str(Path(file_path, "udx", type, "*.gml"))]

    logger.debug([types, infiles, outfile])

    # Codelists
    codelist_infiles = None
    if not zipfile.is_zipfile(file_path):
        # TODO: Test support for non-zip codelists
        codelist_infiles = [str(Path(file_path, "codelists", "*.xml"))]

    exporters.geojson.geojson_from_citygml(
        infiles,
        outfile,
        types=types,
        altitude=altitude,
        include_type=include_type,
        split=split,
        seq=seq,
        zipfile=file_path,
        codelist_infiles=codelist_infiles,
        **kwargs,
    )
