import re
import zipfile
from os import PathLike
from pathlib import Path

import geopandas as gpd

from plateaukit import generators, geocoding
from plateaukit.area import Area
from plateaukit.config import Config
from plateaukit.logger import logger

# from pyogrio import read_dataframe


class Dataset:
    """This class represents a dataset.

    Attributes:
        dataset_id: Dataset ID.
        gdf: The GeoDataFrame of the dataset.
    """

    dataset_id: str
    gdf: gpd.GeoDataFrame | None = None

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

    def get_area(self):
        """Get the entire area of the dataset."""

        if self.gdf is None:
            self.load_gdf()

        area_gdf = self.gdf

        return Area(area_gdf)

    def area_from_bbox(self, bbox: list[float] | None = None):
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

    def area_from_polygons(self, polygons: list[gpd.GeoDataFrame]):
        """Get an area from the dataset by polygons.

        Args:
            polygon: Polygon of the area of interest.
        """

        if self.gdf is None:
            self.load_gdf()

        area_gdf = self.gdf[self.gdf.geometry.intersects(polygons)]

        return Area(area_gdf)

    def area_from_points(
        self, points: list[list[float]], size: list[float] = [1000, 1000]
    ):
        """Get an area from the dataset by points.

        Args:
            points: List of points of the area of interest.
            size: Size of the area of interest in meters.
        """

        if self.gdf is None:
            self.load_gdf()

        bbox = geocoding._get_bbox(points)
        bbox = geocoding._pad_bbox(bbox, size)

        return self.area_from_bbox(bbox)

    def area_from_address(self, address: str, size: list[float] = [1000, 1000]):
        """Get an area from the dataset by an address.

        Args:
            address: Address of the area of interest.
            size: Size of the area of interest in meters.
        """

        if self.gdf is None:
            self.load_gdf()

        bbox = geocoding.bbox_from_address(address, min_size=size)

        return self.area_from_bbox(bbox)

    def area_from_postcode(self, postcode: str):
        """Get an area from the dataset by a postcode.

        Args:
            postcode: Postal code of the area of interest.
        """

        if self.gdf is None:
            self.load_gdf()

        bbox = geocoding.bbox_from_postcode(postcode)

        return self.area_from_bbox(bbox)

    def area_from_landmark(self, landmark: str, min_size: list[float] = [1000, 1000]):
        """Get an area from the dataset by a landmark.

        Args:
            landmark: Landmark of the area of interest.
        """

        if self.gdf is None:
            self.load_gdf()

        bbox = geocoding.bbox_from_landmark(landmark, min_size=min_size)

        return self.area_from_bbox(bbox)

    # def search_area(self, keyword: str):
    #     print(keyword)

    def to_geojson(
        self,
        outfile: str | PathLike,
        *,
        types: list[str] = ["bldg"],
        altitude: bool = True,
        include_type: bool = False,
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
                    # print(targets)
                    infiles += [str(Path("/", target)) for target in targets]
                    # f.extractall(tdir, members=targets)
                    # infiles += [
                    #     str(Path(tdir, Path(file_path).stem, "udx", type, "*.gml"))
                    # ]
            else:
                infiles += [str(Path(file_path, "udx", type, "*.gml"))]

        logger.debug([types, infiles, outfile])

        # Codelists
        codelist_infiles = []
        pat = re.compile(rf".*codelists\/.*\.xml$")
        with zipfile.ZipFile(file_path) as f:
            namelist = f.namelist()
            codelist_infiles = list(filter(lambda x: pat.match(x), namelist))
            codelist_infiles = [str(Path("/", target)) for target in codelist_infiles]

        generators.geojson.geojson_from_citygml(
            infiles,
            outfile,
            types=types,
            altitude=altitude,
            include_type=include_type,
            split=split,
            zipfile=file_path,
            codelist_infiles=codelist_infiles,
            **kwargs,
        )

    def to_cityjson(
        self,
        outfile: str | PathLike,
        types: list[str] = ["bldg"],
        object_types=None,  # TODO: Handle this
        lod=[1, 2],
        ground: bool = False,
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

        config = Config()
        record = config.datasets[self.dataset_id]

        if "citygml" not in record:
            raise Exception("Missing CityGML data")

        file_path = Path(record["citygml"])

        infiles = []

        for type in types:
            # TODO: fix
            pat = re.compile(rf".*udx\/{type}\/.*\.gml$")

            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as f:
                    namelist = f.namelist()
                    targets = list(filter(lambda x: pat.match(x), namelist))
                    infiles += [str(Path("/", target)) for target in targets]
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
        codelist_infiles = []
        pat = re.compile(rf".*codelists\/.*\.xml$")
        with zipfile.ZipFile(file_path) as f:
            namelist = f.namelist()
            codelist_infiles = list(filter(lambda x: pat.match(x), namelist))
            codelist_infiles = [str(Path("/", target)) for target in codelist_infiles]

        generators.simplecityjson.cityjson_from_citygml(
            infiles,
            outfile,
            split=split,
            zipfile=file_path,
            lod=lod,
            ground=ground,
            codelist_infiles=codelist_infiles,
        )


def load_dataset(dataset_id: str) -> Dataset:
    """Load a dataset.

    Args:
        dataset_id: Dataset ID.

    Returns:
        Dataset: Dataset object.
    """
    return Dataset(dataset_id)
