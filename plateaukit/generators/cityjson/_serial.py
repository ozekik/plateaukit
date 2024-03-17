import json

from plateaukit.logger import logger

from .converter import CityJSONConverter


def cityson_from_gml_serial_with_quit(
    infiles,
    outfile,
    object_types,
    lod,
    ground,
    codelist_infiles,
    zipfile=None,
    task_id=None,
    quit=None,
    _progress=None,
    **opts,
):
    # TODO: logger does not work; must use QueueHandler
    logger.debug("[*] cityson_from_gml_serial_with_quit")

    target_epsg = 3857  # Web Mercator
    # target_epsg = 4326  # WGS84
    # target_epsg = 32654  # WGS84 / UTM zone 54N
    # target_epsg = 6677  # JGD2011 / Japan Plane Rectangular CS IV

    converter = CityJSONConverter(target_epsg=target_epsg)

    city_objects = dict(
        converter.generate_city_object(
            infiles,
            object_types=object_types,
            lod=lod,
            ground=ground,
            codelist_infiles=codelist_infiles,
            zipfile=zipfile,
            task_id=task_id,
            quit=quit,
            _progress=_progress,
        )
    )

    # print(city_objects)

    # vertices = [
    #     transformer.transform(*vertice) for vertice in converter.vertices_map.vertices
    # ]
    vertices = converter.vertices_map.vertices

    result = {
        "type": "CityJSON",
        "version": "2.0",
        "extensions": {},
        "transform": {"scale": [1.0, 1.0, 1.0], "translate": [0.0, 0.0, 0.0]},
        "metadata": {
            "referenceSystem": f"https://www.opengis.net/def/crs/EPSG/0/{target_epsg}",
        },
        "CityObjects": city_objects,
        "vertices": vertices,
        # "appearance": {},
        # "geometry-templates": {},
    }
    # result_debug = json.dumps(result, indent=2, ensure_ascii=False)
    # print(result_debug)

    with open(outfile, "w") as f:
        json.dump(result, f, ensure_ascii=False, separators=(",", ":"))

    total = len(infiles) + 1  # + 1 for geojson.dump

    # Complete the progress bar
    if _progress:
        _progress[task_id] = {"progress": total, "total": total}
