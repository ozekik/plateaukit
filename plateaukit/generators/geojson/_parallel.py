import concurrent.futures
import math
from multiprocessing import Manager
from os import PathLike
from pathlib import Path

from rich.progress import Progress

from plateaukit import parallel, utils
from plateaukit.logger import logger

from ._serial import geojson_from_gml_serial_with_quit


def _geojson_from_citygml(
    infiles,
    outfile,
    *,
    codelist_infiles,
    types,
    split,
    zipfile,
    seq: bool,
    progress={},
    simple_output=False,
    **kwargs,
):
    group_size = math.ceil(len(infiles) / split)
    logger.debug(f"GMLs per GeoJSON: {group_size}")
    infile_groups = utils.chunker(infiles, group_size)

    # https://www.deanmontgomery.com/2022/03/24/rich-progress-and-multiprocessing/
    with Progress() as rprogress:
        overall_progress_description = progress.get("description", "Processing...")
        overall_task_id = rprogress.add_task(description=overall_progress_description)

        with Manager() as manager:
            _quit = manager.Event()
            _progress = manager.dict()
            with concurrent.futures.ProcessPoolExecutor(max_workers=None) as pool:
                futures = []
                futures_status = dict()
                for i, infile_group in enumerate(infile_groups):
                    stem = Path(outfile).stem
                    if split > 1:
                        group_outfile = Path(outfile).with_stem(f"{stem}.{i + 1}")
                    else:
                        group_outfile = outfile
                    if simple_output:
                        task_id = None
                    else:
                        task_id = rprogress.add_task(
                            f"[cyan]Progress #{i + 1}", total=len(infile_group)
                        )
                    future = pool.submit(
                        geojson_from_gml_serial_with_quit,
                        infile_group,
                        group_outfile,
                        codelist_infiles=codelist_infiles,
                        types=types,
                        seq=seq,
                        zipfile=zipfile,
                        task_id=task_id,
                        _progress=_progress,
                        _quit=_quit,
                        **kwargs,
                    )
                    futures.append(future)
                    futures_status[future] = {
                        "task_id": task_id,
                        "counter": i + 1,
                        "failed": False,
                    }

                parallel.wait_futures(
                    futures,
                    pool,
                    _quit,
                    futures_status,
                    overall_progress={
                        "task_id": overall_task_id,
                        "description": overall_progress_description,
                    },
                    rich_progress=rprogress,
                    shared_progress_status=_progress,
                )


def geojson_from_citygml(
    infiles: list[str | PathLike],
    outfile: str | PathLike,
    *,
    types: list[str],
    altitude: bool = True,
    seq: bool = False,
    split: int,
    include_type: bool = False,
    zipfile: str | PathLike | None = None,
    codelist_infiles=None,
    **kwargs,
):
    """Generate GeoJSON file(s) from CityGML files."""

    import glob

    if zipfile is None:
        expanded_infiles = []
        for infile in infiles:
            expanded_infiles.extend(glob.glob(infile))

        infiles = expanded_infiles

    infiles = sorted(infiles)

    stem = Path(outfile).stem

    for type in types:
        if len(types) > 1:
            type_outfile = Path(outfile).with_stem(f"{stem}.{type}")
        else:
            type_outfile = outfile

        if type == "bldg":
            """建築物、建築物部分、建築物付属物、及びこれらの境界面"""
            _geojson_from_citygml(
                infiles,
                type_outfile,
                codelist_infiles=codelist_infiles,
                types=["Building"],
                include_type=include_type,
                seq=seq,
                split=split,
                lod=[0],
                altitude=altitude,
                allow_geometry_collection=False,
                zipfile=zipfile,
                **kwargs,
            )
        elif type == "brid":
            """橋梁"""
            _geojson_from_citygml(
                infiles,
                type_outfile,
                codelist_infiles=codelist_infiles,
                types=["Bridge"],
                include_type=include_type,
                seq=seq,
                split=split,
                lod=[2],
                attributes=[],
                altitude=altitude,
                allow_geometry_collection=True,
                zipfile=zipfile,
                **kwargs,
            )
        elif type == "tran":
            """道路"""
            _geojson_from_citygml(
                infiles,
                type_outfile,
                codelist_infiles=codelist_infiles,
                types=["Road"],
                include_type=include_type,
                seq=seq,
                split=split,
                lod=[1],
                attributes=[],
                altitude=altitude,  # TODO: can be False
                allow_geometry_collection=True,
                zipfile=zipfile,
                **kwargs,
            )
        elif type == "dem":
            """地形(起伏)"""
            raise NotImplementedError("dem")
        elif type == "fld":
            """洪水浸水想定区域"""
            raise NotImplementedError("fld")
        elif type == "lsld":
            """土砂災害警戒区域"""
            raise NotImplementedError("lsld")
        elif type == "luse":
            """土地利用"""
            raise NotImplementedError("luse")
        elif type == "urf":
            """都市計画区域、区域区分、地域地区"""
            raise NotImplementedError("urf")
        else:
            raise NotImplementedError(type)
