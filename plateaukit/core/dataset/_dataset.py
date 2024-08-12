from os import PathLike
from typing import Literal, Sequence

import geopandas as gpd

from plateaukit.core.dataset._area import (
    area_from_address,
    area_from_bbox,
    area_from_landmark,
    area_from_points,
    area_from_polygons,
    area_from_postcode,
    get_area,
)
from plateaukit.core.dataset._to_cityjson import to_cityjson
from plateaukit.core.dataset._to_geojson import to_geojson

try:
    from pyogrio import read_dataframe
except ImportError:
    read_dataframe = None

from plateaukit.config import Config
from plateaukit.logger import logger


class Dataset:
    """The Dataset class.

    Attributes:
        dataset_id: Dataset ID.
        gdf: The GeoDataFrame of the dataset.
        object_types: CityGML object types to include in the dataset.
    """

    dataset_id: str
    gdf: gpd.GeoDataFrame | None
    object_types: list[str] | None
    _gdf_cache: dict[str, gpd.GeoDataFrame] | None

    def __init__(self, dataset_id: str, *, object_types: list[str] | None = None):
        """Initialize a dataset.

        Args:
            dataset_id: Dataset ID
            object_types: CityGML object types to include in the dataset.
        """

        self.dataset_id = dataset_id
        self.gdf = None
        self.object_types = object_types

        self._gdf_cache = None

        # config = Config()
        # gpkg_path = config.data[dataset_id].get("gpkg")
        # self.gdf = read_dataframe(gpkg_path)

    def __repr__(self):
        return f"Dataset({self.dataset_id})"

    def load_gdf(self, format: Literal["parquet", "gpkg"] = "parquet"):
        """Load the GeoDataFrame from the prebuilt dataset."""

        if self._gdf_cache is not None:
            return self._gdf_cache

        self._gdf_cache = {}

        # NOTE: Fallback to GeoPackage
        def load_gdf_gpkg():
            if self._gdf_cache is None:
                self._gdf_cache = {}

            gpkg_path = config.datasets[self.dataset_id].get("gpkg")

            if gpkg_path:
                if not read_dataframe:
                    raise ImportError(
                        "Package `pyogrio` is required. Please install it using `pip install pyogrio`."
                    ) from None
                self._gdf_cache["bldg"] = read_dataframe(gpkg_path)  # TODO: Fix typing
            else:
                raise RuntimeError(
                    "Missing a prebuilt dataset; Please run `plateaukit prebuild <dataset_id>` first"
                )

            return self._gdf_cache

        config = Config()

        if format == "parquet":
            logger.debug("Loading Parquet file...")
            parquet_path_or_pathmap = config.datasets[self.dataset_id].get("parquet")

            if isinstance(
                parquet_path_or_pathmap, str
            ):  # NOTE For backward compatibility
                parquet_pathmap = {
                    "bldg": parquet_path_or_pathmap,
                }
            else:
                parquet_pathmap = parquet_path_or_pathmap

            if parquet_pathmap is not None:
                # parquet_path = parquet_paths[0]  # TODO: Fix this
                for k, parquet_path in parquet_pathmap.items():
                    if self.object_types and k not in self.object_types:
                        continue

                    self._gdf_cache[k] = gpd.read_parquet(parquet_path)

                # print(self._gdf_cache)
                return self._gdf_cache
            else:
                return load_gdf_gpkg()

        elif format == "gpkg":
            return load_gdf_gpkg()

        else:
            raise ValueError("Invalid format")

    def get_area(self):
        """Get the entire area of the dataset."""

        return get_area(self)

    def area_from_bbox(self, bbox: list[float] | None = None):
        """Get the specified area from the dataset.

        Args:
            bbox: Bounding box of the area of interest.
                   If not specified, the area of the entire dataset will be returned.
        """

        return area_from_bbox(self, bbox)

    def area_from_polygons(self, polygons: list[gpd.GeoDataFrame]):
        """Get an area from the dataset by polygons.

        Args:
            polygon: Polygon of the area of interest.
        """

        return area_from_polygons(self, polygons)

    def area_from_points(
        self, points: list[Sequence[float]], size: list[float] = [1000, 1000]
    ):
        """Get an area from the dataset by points.

        Args:
            points: List of points of the area of interest.
            size: Size of the area of interest in meters.
        """

        return area_from_points(self, points, size=size)

    def area_from_address(self, address: str, size: list[float] = [1000, 1000]):
        """Get an area from the dataset by an address.

        Args:
            address: Address of the area of interest.
            size: Size of the area of interest in meters.
        """

        return area_from_address(self, address, size=size)

    def area_from_postcode(self, postcode: str):
        """Get an area from the dataset by a postcode.

        Args:
            postcode: Postal code of the area of interest.
        """

        return area_from_postcode(self, postcode)

    def area_from_landmark(self, landmark: str, min_size: list[float] = [1000, 1000]):
        """Get an area from the dataset by a landmark.

        Args:
            landmark: Landmark of the area of interest.
        """

        return area_from_landmark(self, landmark, min_size=min_size)

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
        """Export GeoJSON from PLATEAU datasets.

        Args:
            outfile: Output file path.
            types: CityGML object types to include.
            split: Split the output into specified number of files.
            **kwargs: Keyword arguments for the generator.
        """

        return to_geojson(
            self,
            outfile,
            types=types,
            altitude=altitude,
            include_type=include_type,
            seq=seq,
            split=split,
            **kwargs,
        )

    def to_cityjson(
        self,
        outfile: str | PathLike,
        *,
        types: list[str] = ["bldg"],
        object_types=None,  # TODO: Handle this
        lod_mode: Literal["highest", "all", "values"] = "highest",
        lod_values: list[str] | None = None,
        ground: bool = False,
        seq: bool = False,
        split: int = 1,
        selection: list[str] | None = None,
        target_epsg: int | None = None,
        **kwargs,
    ):
        """Export CityJSON from PLATEAU datasets.

        Args:
            outfile: Output file path.
            types: CityGML feature types.
            split: Split the output into specified number of files.
            seq: Export CityJSONSeq.
            **kwargs: Keyword arguments for the generator.
        """

        return to_cityjson(
            self,
            outfile,
            types=types,
            object_types=object_types,
            lod_mode=lod_mode,
            lod_values=lod_values,
            ground=ground,
            seq=seq,
            split=split,
            selection=selection,
            target_epsg=target_epsg,
            **kwargs,
        )


def load_dataset(dataset_id: str, object_types: list[str] | None = None) -> Dataset:
    """Load a dataset.

    Args:
        dataset_id: Dataset ID.
        object_types: CityGML object types to include in the dataset. If not specified, all object types will be included.

    Returns:
        Dataset: Dataset object.
    """
    # TODO: Raise error if dataset_id is not in local datasets and not a cloud dataset

    return Dataset(dataset_id, object_types=object_types)
