import re
import sys
import zipfile
from os import PathLike
from pathlib import Path, PurePosixPath
from typing import Literal, Sequence

import flatgeobuf as fgb
import geopandas as gpd

try:
    from pyogrio import read_dataframe
except ImportError:
    read_dataframe = None

from plateaukit import defaults, geocoding
from plateaukit.config import Config
from plateaukit.core.area import Area
from plateaukit.logger import logger


class Dataset:
    """This class represents a dataset.

    Attributes:
        dataset_id: Dataset ID.
        gdf: The GeoDataFrame of the dataset.
    """

    dataset_id: str
    gdf: gpd.GeoDataFrame | None

    def __init__(self, dataset_id: str):
        """Initialize a dataset.

        Args:
            dataset_id: Dataset ID
        """

        self.dataset_id = dataset_id
        self.gdf = None

        # config = Config()
        # gpkg_path = config.data[dataset_id].get("gpkg")
        # self.gdf = read_dataframe(gpkg_path)

    def __repr__(self):
        return f"Dataset({self.dataset_id})"

    def load_gdf(self, format: Literal["parquet", "gpkg"] = "parquet"):
        """Load the GeoDataFrame from the prebuilt dataset."""

        # NOTE: Fallback to GeoPackage
        def load_gdf_gpkg():
            gpkg_path = config.datasets[self.dataset_id].get("gpkg")

            if gpkg_path:
                if not read_dataframe:
                    raise ImportError(
                        "Package pyogrio is required. Please install it using `pip install pyogrio`."
                    ) from None
                self.gdf = read_dataframe(gpkg_path)
            else:
                raise RuntimeError(
                    "Missing GeoPackage; Please prebuild the dataset first"
                )

        config = Config()

        if format == "parquet":
            logger.debug("Loading Parquet file...")
            parquet_path = config.datasets[self.dataset_id].get("parquet")

            if parquet_path:
                self.gdf = gpd.read_parquet(parquet_path)
            else:
                load_gdf_gpkg()

        elif format == "gpkg":
            load_gdf_gpkg()

        else:
            raise ValueError("Invalid format")

    def get_area(self):
        """Get the entire area of the dataset."""

        if self.dataset_id.endswith(".cloud"):
            raise Exception("Not supported for cloud datasets")

        if self.gdf is None:
            self.load_gdf()

        area_gdf = self.gdf

        area = Area(area_gdf)
        area._datasets = [self.dataset_id]

        return area

    def area_from_bbox(self, bbox: list[float] | None = None):
        """Get the specified area from the dataset.

        Args:
            bbox: Bounding box of the area of interest.
                   If not specified, the area of the entire dataset will be returned.
        """

        if self.dataset_id.endswith(".cloud"):
            if "pyodide" in sys.modules:
                try:
                    import pyodide_http  # type: ignore

                    pyodide_http.patch_all()
                except Exception:
                    pass

            # Load data from remote flatgeobuf
            remote_fgb = defaults.cloud_base_url + self.dataset_id.replace(
                ".cloud", ".fgb"
            )
            if read_dataframe:
                area_gdf = read_dataframe(
                    remote_fgb,
                    bbox=tuple(bbox),
                )
            else:
                feature_collection = fgb.load_http(
                    remote_fgb,
                    bbox=tuple(bbox),
                )
                area_gdf = gpd.GeoDataFrame.from_features(feature_collection)
        else:
            if self.gdf is None:
                self.load_gdf()

            area_gdf = (
                self.gdf.cx[bbox[0] : bbox[2], bbox[1] : bbox[3]] if bbox else self.gdf
            )

        # TODO: Error handling when area_gdf is empty

        area = Area(area_gdf)
        area._datasets = [self.dataset_id]

        return area

    def area_from_polygons(self, polygons: list[gpd.GeoDataFrame]):
        """Get an area from the dataset by polygons.

        Args:
            polygon: Polygon of the area of interest.
        """

        if self.dataset_id.endswith(".cloud"):
            raise Exception("Not supported for cloud datasets")

        if self.gdf is None:
            self.load_gdf()

        area_gdf = self.gdf[self.gdf.geometry.intersects(polygons)]

        return Area(area_gdf)

    def area_from_points(
        self, points: list[Sequence[float]], size: list[float] = [1000, 1000]
    ):
        """Get an area from the dataset by points.

        Args:
            points: List of points of the area of interest.
            size: Size of the area of interest in meters.
        """

        bbox = geocoding._get_bbox(points)
        bbox = geocoding._pad_bbox(bbox, size)

        return self.area_from_bbox(bbox)

    def area_from_address(self, address: str, size: list[float] = [1000, 1000]):
        """Get an area from the dataset by an address.

        Args:
            address: Address of the area of interest.
            size: Size of the area of interest in meters.
        """

        bbox = geocoding.bbox_from_address(address, min_size=size)

        return self.area_from_bbox(bbox)

    def area_from_postcode(self, postcode: str):
        """Get an area from the dataset by a postcode.

        Args:
            postcode: Postal code of the area of interest.
        """

        bbox = geocoding.bbox_from_postcode(postcode)

        return self.area_from_bbox(bbox)

    def area_from_landmark(self, landmark: str, min_size: list[float] = [1000, 1000]):
        """Get an area from the dataset by a landmark.

        Args:
            landmark: Landmark of the area of interest.
        """
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
        seq=False,
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
        # NOTE: generators requires multiprocessing at the moment, unavailable in pyodide
        from plateaukit import generators

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

                    if not targets:
                        raise RuntimeError(f"Data type '{type}' not found in '{self.dataset_id}'")

                    # NOTE: zipfs requires POSIX path
                    infiles += [str(PurePosixPath("/", target)) for target in targets]

                    # f.extractall(tdir, members=targets)
                    # infiles += [
                    #     str(Path(tdir, Path(file_path).stem, "udx", type, "*.gml"))
                    # ]
            else:
                infiles += [str(Path(file_path, "udx", type, "*.gml"))]

        logger.debug([types, infiles, outfile])

        # Codelists
        codelist_infiles = []
        pat = re.compile(r".*codelists\/.*\.xml$")

        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path) as f:
                namelist = f.namelist()
                codelist_infiles = list(filter(lambda x: pat.match(x), namelist))
                # NOTE: zipfs requires POSIX path
                codelist_infiles = [
                    str(PurePosixPath("/", target)) for target in codelist_infiles
                ]
        else:
            # TODO: Test support for non-zip codelists
            codelist_infiles += [str(Path(file_path, "codelists", "*.xml"))]

        generators.geojson.geojson_from_citygml(
            infiles,
            outfile,
            types=types,
            altitude=altitude,
            include_type=include_type,
            split=split,
            seq=seq,
            zipfile=file_path,
            codelist_infiles=codelist_infiles,
            **kwargs,
        )

    def to_cityjson(
        self,
        outfile: str | PathLike,
        *,
        types: list[str] = ["bldg"],
        object_types=None,  # TODO: Handle this
        lod=[1, 2],
        ground: bool = False,
        seq: bool = False,
        split: int = 1,
        selection: list[str] | None = None,
        target_epsg: int | None = None,
        **kwargs,
    ):
        """Generate CityJSON from PLATEAU datasets.

        Args:
            outfile: Output file path.
            types: CityGML feature types.
            split: Split the output into specified number of files.
            seq: Generate CityJSONSeq.
            **kwargs: Keyword arguments for the generator.
        """
        # NOTE: generators requires multiprocessing at the moment, unavailable in pyodide
        from plateaukit import generators

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

                    if not targets:
                        raise RuntimeError(f"Data type '{type}' not found in '{self.dataset_id}'")

                    # NOTE: zipfs requires POSIX path
                    infiles += [str(PurePosixPath("/", target)) for target in targets]
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
        pat = re.compile(r".*codelists\/.*\.xml$")

        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path) as f:
                namelist = f.namelist()
                codelist_infiles = list(filter(lambda x: pat.match(x), namelist))
                # NOTE: zipfs requires POSIX path
                codelist_infiles = [
                    str(Path("/", target)) for target in codelist_infiles
                ]
        else:
            # TODO: Test support for non-zip codelists
            codelist_infiles += [str(Path(file_path, "codelists", "*.xml"))]

        generators.cityjson.cityjson_from_citygml(
            infiles,
            outfile,
            split=split,
            zipfile=file_path,
            lod=lod,
            ground=ground,
            seq=seq,
            codelist_infiles=codelist_infiles,
            selection=selection,
            target_epsg=target_epsg,
            **kwargs,
        )


def load_dataset(dataset_id: str) -> Dataset:
    """Load a dataset.

    Args:
        dataset_id: Dataset ID.

    Returns:
        Dataset: Dataset object.
    """
    return Dataset(dataset_id)
