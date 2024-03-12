import io
import os.path
from pathlib import Path

import geojson
from fs import open_fs
from geojson import FeatureCollection

from plateaukit.logger import logger
from ._single import geojson_from_gml_single


def geojson_from_gml_serial_with_quit(
    infiles,
    outfile,
    codelist_infiles=None,
    types=None,
    include_type=False,
    zipfile=None,
    task_id=None,
    _quit=None,
    _progress=None,
    **kwargs,
):
    """Generate GeoJSON from multiple CityGML files."""
    features = []

    # Load codelists
    codelist_file_map = None

    if zipfile is not None:
        zip_fs = open_fs(f"zip://{zipfile}")
    else:
        zip_fs = None

    if codelist_infiles and infiles:
        base_path = Path(infiles[0]).parent  # TODO: Fix this
        codelist_file_map = dict()

        for codelist_infile in codelist_infiles:
            if zip_fs is not None:
                with zip_fs.openbin(codelist_infile, "r") as f:
                    relative_path = os.path.relpath(codelist_infile, base_path)
                    codelist_file_map[relative_path] = io.BytesIO(f.read())
            else:
                with open(codelist_infile, "rb") as f:
                    relative_path = os.path.relpath(codelist_infile, base_path)
                    codelist_file_map[relative_path] = io.BytesIO(f.read())

    total = len(infiles) + 1  # + 1 for geojson.dump

    for i, infile in enumerate(infiles):
        if task_id is not None and _progress is not None:
            _progress[task_id] = {"progress": i + 1, "total": total}

        if _quit and _quit.is_set():
            return

        logger.debug(f"infile: {infile}")

        if zip_fs:
            with zip_fs.openbin(infile, "r") as f:
                collection = geojson_from_gml_single(
                    f,
                    types=types,
                    codelist_file_map=codelist_file_map,
                    include_type=include_type,
                    **kwargs,
                )
        else:
            with open(infile, "rb") as f:
                collection = geojson_from_gml_single(
                    f,
                    types=types,
                    codelist_file_map=codelist_file_map,
                    include_type=include_type,
                    **kwargs,
                )
                # TODO: fix

        try:
            features.extend(collection["features"])
        except Exception as err:
            logger.debug(err)

    if zip_fs:
        zip_fs.close()

    collection = FeatureCollection(features)

    # NOTE: Precision https://github.com/jazzband/geojson#default-and-custom-precision
    with open(outfile, "w") as f:
        geojson.dump(collection, f, ensure_ascii=False, separators=(",", ":"))

    # Complete progress
    if _progress:
        _progress[task_id] = {"progress": total, "total": total}
