import concurrent.futures
import math
import sys
from multiprocessing import Manager
from os import PathLike
from pathlib import Path
from typing import List

import geojson
import pyproj
from geojson import Feature, FeatureCollection, GeometryCollection, Polygon
from loguru import logger
from lxml import etree
from rich.progress import Progress

from plateaukit import extractors, utils
from plateaukit.constants import nsmap

# TODO: Should be controlled by -v option:
logger.remove()
logger.add(sys.stderr, level="INFO")


def geojson_from_gml_single(
    infile,
    target_epsg=4326,  # WGS
    altitude=False,
    lod=[0],
    attributes=["measuredHeight"],
    allow_geometry_collection=False,
):
    logger.debug(f"infile: {infile}")

    tree = etree.parse(infile)

    src_epsg = extractors.utils.extract_epsg(tree)  # 6697
    # logger.debug(src_epsg)
    crs_orig = pyproj.CRS(src_epsg)
    # logger.debug(repr(crs_orig))

    logger.debug(f"EPSG:{src_epsg} → EPSG:{target_epsg}")

    transformer = pyproj.Transformer.from_crs(src_epsg, target_epsg)

    features = []

    # logger.debug(
    #     f"""elements#: {len(list(tree.iterfind(f"./{nsmap['core']}cityObjectMember/*")))}"""
    # )

    for i, el in enumerate(tree.iterfind(f"./{nsmap['core']}cityObjectMember/*")):
        # building_id = extract.utils.extract_string_attribute_value(el, "建物ID")
        try:
            building_id = extractors.utils.extract_gml_id(el)
        except Exception as err:
            logger.error(err)
            building_id = None
        # name = extract.utils.extract_name(el)
        # print(building_id)
        # tqdm.write(f"{building_id} {name}")
        # entity = Entity(ns="plateau", uid=building_id, name=name)
        # entities.append(entity)

        ## Attributes
        attribute_values = None
        if attributes:
            attribute_values = {}
            for attribute in attributes:
                value = extractors.utils.exract_bldg_attribute(el, attribute)
                # TODO: fix
                try:
                    value = float(value) if value else None
                except:
                    pass
                attribute_values[attribute] = value

        ## EXTRACT LODs
        if len(lod) > 1:
            raise NotImplementedError("too many LOD values")

        poslists = None

        logger.debug(f"lod: {lod}")

        if 0 in lod:
            poslists = extractors.utils.extract_lod0_poslists(el)
            # print(lod0_poslist)
        if 1 in lod:
            try:
                poslists = extractors.utils.extract_lod1_poslists(el)
            except Exception as err:
                logger.error(err)
                poslists = []

        polygons = []

        logger.debug(f"poslists: {poslists}")

        # TODO: fix
        if not poslists:
            return

        for poslist in poslists:
            chunked = utils.chunker(poslist, 3)

            base_polygon = [transformer.transform(*coord) for coord in chunked]

            # print(list(utils.chunker(lod0_poslist, 3)))
            # print(base_polygon)

            if altitude:
                # raise NotImplementedError()
                base_polygon = list(map(lambda x: [x[1], x[0], x[2]], base_polygon))
            else:
                base_polygon = list(map(lambda x: [x[1], x[0]], base_polygon))

            poly = Polygon([base_polygon])
            # print(poly)

            polygons.append(poly)

        def to_feature(feature_geometry):
            properties = {}
            if building_id:
                properties["id"] = building_id
            if attributes:
                properties |= attribute_values

            feat = Feature(
                geometry=feature_geometry,
                properties=properties,
            )
            # print(feat)

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
    task_id=None,
    quit=None,
    _progress=None,
    **opts,
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

        logger.debug(infile)
        with open(infile, "r") as f:
            collection = geojson_from_gml_single(f, **opts)
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


def geojson_from_gml(infiles, outfile, split, progress={}, **opts):
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
                            task_id=task_id,
                            _progress=_progress,
                            quit=None,
                            # **opts,
                        )
                    )
                # with tqdm(
                #     concurrent.futures.as_completed(futures), total=len(futures)
                # ) as pbar:
                try:
                    # for future in track(
                    #     concurrent.futures.as_completed(futures), total=len(futures)
                    # ):
                    #     task_id = progress.add_task("", total=len(futures))
                    #     for future in concurrent.futures.as_completed(futures):
                    #         result = future.result()
                    #         progress.update(task_id, advance=1)
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
    infiles: List[str | PathLike],
    outfile: str | PathLike,
    type: str,
    split: int,
    **kwargs,
):
    """Generate GeoJSON file(s) from CityGML files."""

    import glob

    expanded_infiles = []
    for infile in infiles:
        expanded_infiles.extend(glob.glob(infile))

    expanded_infiles = sorted(expanded_infiles)

    if type == "bldg":
        geojson_from_gml(
            expanded_infiles,
            outfile,
            split=split,
            lod=[0],
            altitude=True,
            allow_geometry_collection=False,
            **kwargs,
        )
    elif type == "brid":
        geojson_from_gml(
            expanded_infiles,
            outfile,
            split=split,
            lod=[1],
            attributes=[],
            altitude=True,
            allow_geometry_collection=True,
            **kwargs,
        )
    elif type == "dem":
        # TODO: implement
        raise NotImplementedError("dem")
    elif type == "fld":
        raise NotImplementedError("fld")
    elif type == "lsld":
        raise NotImplementedError("lsld")
    elif type == "luse":
        raise NotImplementedError("luse")
        # generate.geojson_from_gml(
        #     expanded_infiles,
        #     outfile,
        #     split=split,
        #     lod=[1],
        #     attributes=[],
        #     altitude=True,
        #     allow_geometry_collection=True,
        # )
    elif type == "tran":
        geojson_from_gml(
            expanded_infiles,
            outfile,
            split=split,
            lod=[1],
            attributes=[],
            altitude=True,  # TODO: can be False
            allow_geometry_collection=True,
            **kwargs,
        )
    elif type == "urf":
        raise NotImplementedError("urf")
        # generate.geojson_from_gml(
        #     expanded_infiles,
        #     outfile,
        #     split=split,
        #     lod=[0],
        #     attributes=[],
        #     altitude=True,
        #     allow_geometry_collection=False,
        # )
    else:
        raise NotImplementedError(type)
