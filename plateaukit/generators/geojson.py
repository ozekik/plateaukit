import concurrent.futures
import math
import sys
from multiprocessing import Manager
from os import PathLike
from pathlib import Path

import geojson
from geojson import Feature, FeatureCollection, GeometryCollection, Polygon
from loguru import logger
from rich.progress import Progress

from plateaukit import utils
from plateaukit.parsers import PLATEAUCityGMLParser
from plateaukit.utils import dict_key_to_camel_case

# TODO: Should be controlled by -v option:
logger.remove()
logger.add(sys.stderr, level="INFO")


def geojson_from_gml_single(
    infile,
    types=None,
    target_epsg=4326,  # WGS
    altitude=False,
    lod=[0],
    attributes=["measuredHeight"],
    allow_geometry_collection=False,
):
    # logger.debug("geojson_from_gml_single")

    parser = PLATEAUCityGMLParser(target_epsg=target_epsg)
    citygml = parser.parse(infile)

    # logger.debug(f"citygml: {citygml}")

    features = []

    if len(lod) > 1:
        raise NotImplementedError("too many LOD values")

    for i, obj in enumerate(citygml.city_objects):
        logger.debug(f"{obj.id}")

        if types and obj.type not in types:
            continue

        polygons = []

        if 0 in lod:
            geom = next(filter(lambda x: x["lod"] == 0, obj.geometry), None)
        if 1 in lod:
            geom = next(filter(lambda x: x["lod"] == 1, obj.geometry), None)
            # raise NotImplementedError("LOD 1")
        if 2 in lod:
            geom = next(filter(lambda x: x["lod"] == 2, obj.geometry), None)

        if geom is None:
            continue

        # WIP: exterior only; TODO: Fix this
        base_polygons = [surface[0] for surface in geom["boundaries"]]

        if altitude:
            base_polygons = [
                list(map(lambda x: [x[1], x[0], x[2]], base_polygon))
                for base_polygon in base_polygons
            ]
        else:
            base_polygons = [
                list(map(lambda x: [x[1], x[0]], base_polygon))
                for base_polygon in base_polygons
            ]

        polygons = [Polygon([base_polygon]) for base_polygon in base_polygons]

        def to_feature(feature_geometry):
            properties = {}
            # properties["id"] = obj.id
            properties |= dict_key_to_camel_case(obj.attributes)
            # if attributes:
            #     properties |= attribute_values

            feat = Feature(
                geometry=feature_geometry,
                properties=properties,
            )

            return feat

        if len(polygons) == 1:
            feat = to_feature(polygons[0])
            features.append(feat)
        else:
            if allow_geometry_collection:
                feat = to_feature(GeometryCollection(polygons))
                features.append(feat)
            else:
                for polygon in polygons:
                    feat = to_feature(polygon)
                    features.append(feat)
                # raise AssertionError("No geometry")

    collection = FeatureCollection(features)

    return collection


def geojson_from_gml_serial_with_quit(
    infiles,
    outfile,
    types=None,
    task_id=None,
    quit=None,
    _progress=None,
    **kwargs,
):
    features = []

    # with tqdm(
    #     infiles, desc=f"#{group_num + 1:>3} ", position=group_num + 1, leave=False
    # ) as pbar:
    total = len(infiles)
    for i, infile in enumerate(infiles):
        if task_id is not None and _progress is not None:
            _progress[task_id] = {"progress": i + 1, "total": total}

        if quit and quit.is_set():
            return

        logger.debug(f"infile: {infile}")

        with open(infile, "r") as f:
            collection = geojson_from_gml_single(f, types=types, **kwargs)
            # TODO: fix
            try:
                features.extend(collection["features"])
            except Exception as err:
                logger.debug(err)
                pass

    collection = FeatureCollection(features)

    # NOTE: Precision https://github.com/jazzband/geojson#default-and-custom-precision
    with open(outfile, "w") as f:
        geojson.dump(collection, f, ensure_ascii=False, separators=(",", ":"))


def _geojson_from_citygml(infiles, outfile, types=None, split=1, progress={}, **kwargs):
    group_size = math.ceil(len(infiles) / split)
    logger.debug(f"GMLs per GeoJSON: {group_size}")
    infile_groups = utils.chunker(infiles, group_size)

    # https://www.deanmontgomery.com/2022/03/24/rich-progress-and-multiprocessing/
    with Progress() as rprogress:
        overall_progress_description = progress.get("description", "Processing...")
        overall_task_id = rprogress.add_task(description=overall_progress_description)

        with Manager() as manager:
            quit = manager.Event()
            _progress = manager.dict()
            with concurrent.futures.ProcessPoolExecutor(max_workers=None) as pool:
                futures = []
                for i, infile_group in enumerate(infile_groups):
                    stem = Path(outfile).stem
                    if split > 1:
                        group_outfile = Path(outfile).with_stem(f"{stem}.{i + 1}")
                    else:
                        group_outfile = outfile
                    task_id = rprogress.add_task(
                        f"[cyan]Progress #{i + 1}", total=len(infile_group)
                    )
                    futures.append(
                        pool.submit(
                            geojson_from_gml_serial_with_quit,
                            infile_group,
                            group_outfile,
                            types=types,
                            task_id=task_id,
                            _progress=_progress,
                            quit=None,
                            **kwargs,
                        )
                    )
                # with tqdm(
                #     concurrent.futures.as_completed(futures), total=len(futures)
                # ) as pbar:
                try:
                    while (
                        n_finished := sum([future.done() for future in futures])
                    ) < len(futures):
                        rprogress.update(
                            overall_task_id,
                            completed=n_finished,
                            total=len(futures),
                        )
                        for task_id, status in _progress.items():
                            latest = status["progress"]
                            total = status["total"]

                            rprogress.update(
                                task_id,
                                completed=latest,
                                total=total,
                                visible=latest < total,
                            )

                    # Finish up the overall progress bar
                    rprogress.update(
                        overall_task_id,
                        completed=n_finished,
                        total=len(futures),
                        description=f"{overall_progress_description} [green]Done",
                    )

                except KeyboardInterrupt:
                    quit.set()
                    pool.shutdown(wait=True, cancel_futures=True)
                    # pool._processes.clear()
                    # concurrent.futures.thread._threads_queues.clear()
                    raise


def geojson_from_citygml(
    infiles: list[str | PathLike],
    outfile: str | PathLike,
    types: list[str],
    split: int,
    **kwargs,
):
    """Generate GeoJSON file(s) from CityGML files."""

    import glob

    expanded_infiles = []
    for infile in infiles:
        expanded_infiles.extend(glob.glob(infile))

    expanded_infiles = sorted(expanded_infiles)

    stem = Path(outfile).stem

    for type in types:
        if len(types) > 1:
            type_outfile = Path(outfile).with_stem(f"{stem}.{type}")
        else:
            type_outfile = outfile

        if type == "bldg":
            """建築物、建築物部分、建築物付属物、及びこれらの境界面"""
            _geojson_from_citygml(
                expanded_infiles,
                type_outfile,
                types=["Building"],
                split=split,
                lod=[0],
                altitude=True,
                allow_geometry_collection=False,
                **kwargs,
            )
        elif type == "brid":
            """橋梁"""
            _geojson_from_citygml(
                expanded_infiles,
                type_outfile,
                types=["Bridge"],
                split=split,
                lod=[2],
                attributes=[],
                altitude=True,
                allow_geometry_collection=True,
                **kwargs,
            )
        elif type == "tran":
            """道路"""
            _geojson_from_citygml(
                expanded_infiles,
                type_outfile,
                types=["Road"],
                split=split,
                lod=[1],
                attributes=[],
                altitude=True,  # TODO: can be False
                allow_geometry_collection=True,
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
