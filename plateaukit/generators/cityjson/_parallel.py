import concurrent.futures
import math
from multiprocessing import Manager
from pathlib import Path

from rich.progress import Progress

from plateaukit import parallel, utils
from plateaukit.logger import logger

from ._serial import cityson_from_gml_serial_with_quit


def cityjson_from_citygml(
    infiles,
    outfile,
    *,
    split: int = 1,
    zipfile=None,
    precision=16,
    object_types=None,
    lod: list[int] = [1, 2],
    ground: bool = False,
    seq=False,
    codelist_infiles=None,
    selection: list[str] | None = None,
    target_epsg: int | None = None,
    progress={},
):
    logger.debug("[*] cityjson_from_citygml")
    # vertices_map = VerticesMap()
    # city_objects = {}

    group_size = math.ceil(len(infiles) / split)
    logger.debug(f"GMLs per GeoJSON: {group_size}")
    infile_groups = utils.chunker(infiles, group_size)

    with Progress() as rprogress:
        overall_progress_description = progress.get("description", "Processing...")
        overall_task_id = rprogress.add_task(overall_progress_description)

        with Manager() as manager:
            quit = manager.Event()
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

                    task_id = rprogress.add_task(
                        f"[cyan]Progress #{i + 1}", total=len(infile_group)
                    )
                    # task_id = None

                    logger.debug(f"group_outfile: {group_outfile}")

                    future = pool.submit(
                        cityson_from_gml_serial_with_quit,
                        infile_group,
                        group_outfile,
                        object_types=object_types,
                        lod=lod,
                        ground=ground,
                        codelist_infiles=codelist_infiles,
                        seq=seq,
                        zipfile=zipfile,
                        selection=selection,
                        target_epsg=target_epsg,
                        task_id=task_id,
                        _progress=_progress,
                        quit=quit,
                        # **kwargs,
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
                    quit,
                    futures_status,
                    overall_progress={
                        "task_id": overall_task_id,
                        "description": overall_progress_description,
                    },
                    rich_progress=rprogress,
                    shared_progress_status=_progress,
                )
