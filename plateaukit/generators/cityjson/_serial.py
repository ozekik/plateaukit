import json

from plateaukit.logger import logger

from .converter import CityJSONConverter


def cityson_from_gml_serial_with_quit(
    infiles,
    outfile,
    *,
    object_types,
    lod,
    ground,
    codelist_infiles,
    seq=False,
    zipfile=None,
    selection: list[str] | None = None,
    target_epsg: int | None = 3857,
    task_id=None,
    quit=None,
    _progress=None,
    **opts,
):
    # TODO: logger does not work in multiprocessing; must use QueueHandler
    logger.debug("[*] cityson_from_gml_serial_with_quit")

    if not target_epsg:
        target_epsg = 3857  # Web Mercator
        # target_epsg = 4326  # WGS84
        # target_epsg = 32654  # WGS84 / UTM zone 54N
        # target_epsg = 6677  # JGD2011 / Japan Plane Rectangular CS IV

    if seq:
        converter = CityJSONConverter(target_epsg=target_epsg)

        with open(outfile, "w") as f:
            meta = converter.get_meta()
            json.dump(meta, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")

            features = converter.features(
                infiles,
                object_types=object_types,
                lod=lod,
                ground=ground,
                codelist_infiles=codelist_infiles,
                zipfile=zipfile,
                selection=selection,
                task_id=task_id,
                quit=quit,
                _progress=_progress,
            )

            for feature in features:
                json.dump(feature, f, ensure_ascii=False, separators=(",", ":"))
                f.write("\n")

    else:
        converter = CityJSONConverter(target_epsg=target_epsg)

        result = converter.convert(
            infiles,
            object_types=object_types,
            lod=lod,
            ground=ground,
            codelist_infiles=codelist_infiles,
            zipfile=zipfile,
            selection=selection,
            task_id=task_id,
            quit=quit,
            _progress=_progress,
        )

        with open(outfile, "w") as f:
            json.dump(result, f, ensure_ascii=False, separators=(",", ":"))

    total = len(infiles) + 1  # + 1 for geojson.dump

    # Complete the progress bar
    if _progress:
        _progress[task_id] = {"progress": total, "total": total}
