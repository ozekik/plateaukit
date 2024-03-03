from pathlib import Path

from plateaukit.logger import logger


def geojson_to_gpkg(
    infiles,
    outfile,
):
    import geopandas as gpd

    for infile in infiles:
        logger.debug(infile)
        with open(infile, "r") as f:
            # print(infile)
            df = gpd.read_file(f, encoding="tuf-8")
            # print(df)
            if not Path(outfile).exists():
                df.to_file(outfile, driver="GPKG", mode="w")
            else:
                df.to_file(outfile, driver="GPKG", mode="a")
