import glob
import re
import tempfile
import zipfile
from os import PathLike
from pathlib import Path
from typing import List, Optional

import geopandas as gpd
from loguru import logger

from plateaukit import generators
from plateaukit.area import Area
from plateaukit.config import Config

# from pyogrio import read_dataframe


class Dataset:
    """This class represents a dataset.

    Attributes:
        dataset_id: Dataset ID.
        gdf: The GeoDataFrame of the dataset.
    """

    dataset_id: str
    gdf: Optional[gpd.GeoDataFrame] = None

    def __init__(self, dataset_id: str):
        """Initialize a dataset.

        Args:
            dataset_id: Dataset ID
        """
        self.dataset_id = dataset_id
        # config = Config()
        # gpkg_path = config.data[dataset_id].get("gpkg")
        # self.gdf = read_dataframe(gpkg_path)

    def __repr__(self):
        return f"Dataset({self.dataset_id})"

    def load_gdf(self):
        """Load the GeoDataFrame from the prebuilt dataset."""

        from pyogrio import read_dataframe

        config = Config()
        gpkg_path = config.datasets[self.dataset_id].get("gpkg")

        if gpkg_path:
            self.gdf = read_dataframe(gpkg_path)
        else:
            raise RuntimeError("Missing GeoPackage; Please prebuild the dataset first")

    def get_area(self, bbox: Optional[List[float]] = None):
        """Get the specified area from the dataset.

        Args:
            bbox: Bounding box of the area of interest.
                   If not specified, the area of the entire dataset will be returned.
        """

        if self.gdf is None:
            self.load_gdf()

        area_gdf = (
            self.gdf.cx[bbox[0] : bbox[2], bbox[1] : bbox[3]] if bbox else self.gdf
        )

        # TODO: Error handling when area_gdf is empty

        return Area(area_gdf)

    # def search_area(self, keyword: str):
    #     print(keyword)

    def to_geojson(
        self,
        outfile: str | PathLike,
        types: List[str] = ["bldg"],
        split: int = 1,
        **kwargs,
    ):
        """Generate GeoJSON from PLATEAU datasets.

        Args:
            outfile: Output file path.
            types: CityGML object types to include.
            split: Split the output into specified number of files.
            **kwargs: Keyword arguments for the generator.
        """
        if not self.dataset_id:
            raise Exception("Missing dataset_id")

        if not types:
            raise Exception("Missing object types")

        # NOTE: this is intentional but to be refactored in the future
        with tempfile.TemporaryDirectory() as tdir:
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
                        # print(targets, tdir)
                        f.extractall(tdir, members=targets)
                        # TODO: fix
                        infiles = [
                            str(Path(tdir, Path(file_path).stem, "udx", type, "*.gml"))
                        ]
                else:
                    infiles += [str(Path(file_path, "udx", type, "*.gml"))]
                logger.debug([infiles, outfile])

            generators.geojson.geojson_from_citygml(
                infiles, outfile, types=types, split=split, **kwargs
            )

    def to_cityjson(
        self,
        outfile: str | PathLike,
        types: List[str] = ["bldg"],
        split: int = 1,
        **kwargs,
    ):
        """Generate CityJSON from PLATEAU datasets.

        Args:
            outfile: Output file path.
            types: CityGML feature types.
            split: Split the output into specified number of files.
            **kwargs: Keyword arguments for the generator.
        """
        params = {}

        # if precision:
        #     params["precision"] = precision

        if not self.dataset_id:
            raise Exception("Missing dataset_id")

        with tempfile.TemporaryDirectory() as tdir:
            config = Config()
            record = config.datasets[self.dataset_id]

            if "citygml" not in record:
                raise Exception("Missing CityGML data")

            file_path = Path(record["citygml"])

            for type in types:
                # TODO: fix
                pat = re.compile(rf".*udx\/{type}\/.*\.gml$")

                if zipfile.is_zipfile(file_path):
                    with zipfile.ZipFile(file_path) as f:
                        namelist = f.namelist()
                        targets = list(filter(lambda x: pat.match(x), namelist))
                        # print(targets, tdir)
                        f.extractall(tdir, members=targets)
                        # TODO: fix
                        infiles = [
                            str(Path(tdir, Path(file_path).stem, "udx", type, "*.gml"))
                        ]
                else:
                    infiles = [str(Path(file_path, "udx", type, "*.gml"))]

                logger.debug([infiles, outfile])

                expanded_infiles = []

                for infile in infiles:
                    expanded_infiles.extend(glob.glob(infile))

                expanded_infiles = sorted(expanded_infiles)

                # print(infiles, expanded_infiles)

                generators.simplecityjson.cityjson_from_citygml(
                    expanded_infiles,
                    outfile,
                    split=split,
                    lod=[1],
                )


def load_dataset(dataset_id: str) -> Dataset:
    """Load a dataset.

    Args:
        dataset_id: Dataset ID.

    Returns:
        Dataset: Dataset object.
    """
    return Dataset(dataset_id)
