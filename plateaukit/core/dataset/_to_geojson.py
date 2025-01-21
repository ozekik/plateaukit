import re
import zipfile
from os import PathLike
from pathlib import Path, PurePosixPath

from plateaukit.config import Config
from plateaukit.exporters.geojson2.writer import GeoJSONWriter
from plateaukit.exporters.parallel_writer import ParallelWriter
from plateaukit.logger import logger
from plateaukit.readers.citygml.reader import CityGMLReader
from plateaukit.transformers.reprojection import ReprojectionTransformer
# from plateaukit.transformers.simplify import SimplifyTransformer


def to_geojson(
    self,
    outfile: str | PathLike,
    *,
    altitude: bool = True,
    types: list[str] = ["bldg"],
    # group_by_type: bool = True,
    object_types=None,  # TODO: Handle this
    include_object_type: bool = True,
    ground: bool = False,
    seq=False,
    split: int = 1,
    selection: list[str] | None = None,
    target_epsg: int | None = None,
    progress_messages: dict | None = None,
    **kwargs,
):
    """Export GeoJSON from PLATEAU datasets.

    Args:
        outfile: Output file path.
        types: CityGML object types to include.
        split: Split the output into specified number of files.
        seq: Export GeoJSONSeq.
        **kwargs: Keyword arguments for the generator.
    """
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
    transformers = []

    # transformers: list = [
    #     LODFilteringTransformer(mode=lod_mode, values=lod_values),
    # ]

    if target_epsg:
        transformers.append(ReprojectionTransformer(target_epsg=target_epsg))

    for transformer in transformers:
        readable = transformer.transform(readable)

    parallel_writer = ParallelWriter(GeoJSONWriter)
    parallel_writer.transform(
        readable,
        str(outfile),
        altitude=altitude,
        include_object_type=include_object_type,
        seq=seq,
        split=split,
        progress_messages=progress_messages,
    )

    # if group_by_type:
    #     stem = Path(outfile).stem

    #     for type in types:
    #         if len(types) > 1:
    #             type_outfile = Path(outfile).with_stem(f"{stem}.{type}")
    #         else:
    #             type_outfile = outfile

    #         if type == "bldg":
    #             """建築物、建築物部分、建築物付属物、及びこれらの境界面"""
    #             pass
    #             # _geojson_from_citygml(
    #             #     infiles,
    #             #     type_outfile,
    #             #     codelist_infiles=codelist_infiles,
    #             #     types=["Building"],
    #             #     include_type=include_type,
    #             #     seq=seq,
    #             #     split=split,
    #             #     lod=["0"],
    #             #     altitude=altitude,
    #             #     allow_geometry_collection=False,
    #             #     zipfile=zipfile,
    #             #     **kwargs,
    #             # )
    #         elif type == "brid":
    #             """橋梁"""
    #             pass
    #             # _geojson_from_citygml(
    #             #     infiles,
    #             #     type_outfile,
    #             #     codelist_infiles=codelist_infiles,
    #             #     types=["Bridge"],
    #             #     include_type=include_type,
    #             #     seq=seq,
    #             #     split=split,
    #             #     lod=["2"],
    #             #     attributes=[],
    #             #     altitude=altitude,
    #             #     allow_geometry_collection=True,
    #             #     zipfile=zipfile,
    #             #     **kwargs,
    #             # )
    #         elif type == "tran":
    #             """道路"""
    #             pass
    #             # _geojson_from_citygml(
    #             #     infiles,
    #             #     type_outfile,
    #             #     codelist_infiles=codelist_infiles,
    #             #     types=["Road"],
    #             #     include_type=include_type,
    #             #     seq=seq,
    #             #     split=split,
    #             #     lod=["1"],
    #             #     attributes=[],
    #             #     altitude=altitude,  # TODO: can be False
    #             #     allow_geometry_collection=True,
    #             #     zipfile=zipfile,
    #             #     **kwargs,
    #             # )
    #         elif type == "dem":
    #             """地形(起伏)"""
    #             raise NotImplementedError("dem")
    #         elif type == "fld":
    #             """洪水浸水想定区域"""
    #             raise NotImplementedError("fld")
    #         elif type == "lsld":
    #             """土砂災害警戒区域"""
    #             raise NotImplementedError("lsld")
    #         elif type == "luse":
    #             """土地利用"""
    #             raise NotImplementedError("luse")
    #         elif type == "urf":
    #             """都市計画区域、区域区分、地域地区"""
    #             raise NotImplementedError("urf")
    #         else:
    #             raise NotImplementedError(type)

    #         parallel_writer = ParallelWriter(GeoJSONWriter)
    #         parallel_writer.transform(
    #             readable,
    #             str(type_outfile),
    #             altitude=altitude,
    #             include_object_type=include_object_type,
    #             seq=seq,
    #             split=split,
    #             progress_messages=progress_messages,
    #         )

    # else:
    #     parallel_writer = ParallelWriter(GeoJSONWriter)
    #     parallel_writer.transform(
    #         readable,
    #         str(outfile),
    #         altitude=altitude,
    #         include_object_type=include_object_type,
    #         seq=seq,
    #         split=split,
    #         progress_messages=progress_messages,
    #     )

    # exporters.geojson.geojson_from_citygml(
    #     infiles,
    #     outfile,
    #     types=types,
    #     altitude=altitude,
    #     include_type=include_type,
    #     split=split,
    #     seq=seq,
    #     zipfile=file_path,
    #     codelist_infiles=codelist_infiles,
    #     **kwargs,
    # )


def dem_to_geojson(
    self,
    outfile: str | PathLike,
    *,
    seq=False,
    split: int = 1,
    selection: list[str] | None = None,
    target_epsg: int | None = None,
    target_reduction: float | None = None,
    progress_messages: dict | None = None,
    **kwargs,
):
    """Export GeoJSON from PLATEAU dataset DEMs.

    Args:
        outfile: Output file path.
        types: CityGML object types to include.
        split: Split the output into specified number of files.
        seq: Export GeoJSONSeq.
        **kwargs: Keyword arguments for the generator.
    """
    if not self.dataset_id:
        raise Exception("Missing dataset_id")

    # NOTE: this is intentional but to be refactored in the future
    config = Config()
    record = config.datasets[self.dataset_id]

    if "citygml" not in record:
        raise Exception("Missing CityGML data")

    file_path = Path(record["citygml"])

    infiles = []

    # TODO: Refactor
    type = "dem"

    # TODO: Fix
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

    logger.debug([type, infiles, outfile])

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
    transformers: list = []

    # if target_reduction:
    #     transformers += [
    #         ReprojectionTransformer(target_epsg=3857),
    #         SimplifyTransformer(target_reduction=target_reduction),
    #     ]

    if target_epsg:
        transformers.append(ReprojectionTransformer(target_epsg=target_epsg))

    for transformer in transformers:
        readable = transformer.transform(readable)

    parallel_writer = ParallelWriter(GeoJSONWriter)
    parallel_writer.transform(
        readable,
        str(outfile),
        seq=seq,
        split=split,
        progress_messages=progress_messages,
        altitude=True,
    )
