import re
import sys
import zipfile
from os import PathLike
from pathlib import Path, PurePosixPath
from typing import Literal, Sequence, cast

import flatgeobuf as fgb
import geopandas as gpd

from plateaukit.exporters.cityjson.parallel_writer import ParallelWriter
from plateaukit.exporters.cityjson.writer import CityJSONWriter
from plateaukit.readers.citygml.reader import CityGMLReader
from plateaukit.transformers.filter_lod import LODFilteringTransformer

try:
    from pyogrio import read_dataframe
except ImportError:
    read_dataframe = None

from plateaukit import defaults, geocoding
from plateaukit.config import Config
from plateaukit.core.area import Area, GeoDataFrameLayer
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

        if self.dataset_id.endswith(".cloud"):
            raise Exception("Not supported for cloud datasets")

        dataframes = self.load_gdf()

        layers = {}

        for k, gdf in dataframes.items():
            if self.object_types is None or k in self.object_types:
                layers[k] = GeoDataFrameLayer(gdf)

        if "bldg" not in layers:
            raise RuntimeError("Missing building data")

        area = Area(layers, base_layer_name="bldg")
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
                    bbox=tuple(bbox) if bbox else None,
                )
                area_gdf = cast(gpd.GeoDataFrame, area_gdf)
            else:
                feature_collection = fgb.load_http(
                    remote_fgb,
                    bbox=tuple(bbox) if bbox else None,
                )
                area_gdf = gpd.GeoDataFrame.from_features(feature_collection)

            layers = {}
            layers["bldg"] = GeoDataFrameLayer(area_gdf)
            area = Area(layers, base_layer_name="bldg")

        else:
            dataframes = self.load_gdf()

            layers = {}

            for k, gdf in dataframes.items():
                if self.object_types is None or k in self.object_types:
                    # TODO: Error handling when area_gdf is empty
                    area_gdf = (
                        gdf.cx[bbox[0] : bbox[2], bbox[1] : bbox[3]] if bbox else gdf
                    )
                    layers[k] = GeoDataFrameLayer(area_gdf)

            if "bldg" not in layers:
                raise RuntimeError("`bldg` layer is required")

            area = Area(layers, base_layer_name="bldg")

        area._datasets = [self.dataset_id]

        return area

    def area_from_polygons(self, polygons: list[gpd.GeoDataFrame]):
        """Get an area from the dataset by polygons.

        Args:
            polygon: Polygon of the area of interest.
        """

        if self.dataset_id.endswith(".cloud"):
            raise Exception("Not supported for cloud datasets")

        dataframes = self.load_gdf()

        layers = {}

        for k, gdf in dataframes.items():
            if self.object_types is None or k in self.object_types:
                # TODO: Error handling when area_gdf is empty
                area_gdf = gdf[gdf.geometry.intersects(polygons)]
                layers[k] = GeoDataFrameLayer(area_gdf)

        if "bldg" not in layers:
            raise RuntimeError("`bldg` layer is required")

        area = Area(layers, base_layer_name="bldg")

        return area

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
        """Export GeoJSON from PLATEAU datasets.

        Args:
            outfile: Output file path.
            types: CityGML object types to include.
            split: Split the output into specified number of files.
            **kwargs: Keyword arguments for the generator.
        """
        # NOTE: exporters requires multiprocessing at the moment, unavailable in pyodide
        from plateaukit import exporters

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
                        raise RuntimeError(
                            f"Data type '{type}' not found in '{self.dataset_id}'"
                        )

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
        codelist_infiles = None
        if not zipfile.is_zipfile(file_path):
            # TODO: Test support for non-zip codelists
            codelist_infiles = [str(Path(file_path, "codelists", "*.xml"))]

        exporters.geojson.geojson_from_citygml(
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
        # NOTE: (check) generators requires multiprocessing at the moment, unavailable in pyodide
        # params = {}

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
                        raise RuntimeError(
                            f"Data type '{type}' not found in '{self.dataset_id}'"
                        )

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
        codelist_infiles = None
        if not zipfile.is_zipfile(file_path):
            # TODO: Test support for non-zip codelists
            codelist_infiles = [str(Path(file_path, "codelists", "*.xml"))]

        reader = CityGMLReader()

        readable = reader.scan_files(
            infiles,
            codelist_infiles=codelist_infiles,
            zipfile=file_path,
            selection=selection,
        )

        transformers = [LODFilteringTransformer(mode=lod_mode, values=lod_values)]

        for transformer in transformers:
            readable = transformer.transform(readable)

        parallel_writer = ParallelWriter(CityJSONWriter)
        parallel_writer.transform(readable, str(outfile), seq=False, split=split)

        # writer = CityJSONWriter()
        # result = writer.transform(document, seq=seq)

        # import json

        # if seq:
        #     with open(outfile, "w") as f:
        #         for line in result:
        #             f.write(json.dumps(line, separators=(",", ":")) + "\n")
        # else:
        #     with open(outfile, "w") as f:
        #         f.write(json.dumps(result, separators=(",", ":")))

        # generators.cityjson.cityjson_from_citygml(
        #     infiles,
        #     outfile,
        #     split=split,
        #     zipfile=file_path,
        #     lod=lod,
        #     use_highest_lod=use_highest_lod,
        #     ground=ground,
        #     seq=seq,
        #     codelist_infiles=codelist_infiles,
        #     selection=selection,
        #     target_epsg=target_epsg,
        #     **kwargs,
        # )


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
