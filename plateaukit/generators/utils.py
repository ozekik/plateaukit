import sys
from pathlib import Path

from tqdm import tqdm

from plateaukit.logger import logger


def geojson_to_gpkg(
    infiles,
    outfile,
):
    import geopandas as gpd

    with tqdm(infiles) as pbar:
        for infile in pbar:
            logger.debug(infile)
            with open(infile, "r") as f:
                # print(infile)
                df = gpd.read_file(f, encoding="tuf-8")
                # print(df)
                if not Path(outfile).exists():
                    df.to_file(outfile, driver="GPKG", mode="w")
                else:
                    df.to_file(outfile, driver="GPKG", mode="a")
