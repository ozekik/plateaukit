import tempfile
from pathlib import Path
from textwrap import dedent
from typing import Literal

import ipydeck
import pandas as pd
import pydeck

from plateaukit.config import Config
from plateaukit.core.layer import BaseLayer, GeoDataFrameLayer
from plateaukit.core.widgets.interactive_deck import InteractiveDeck
from plateaukit.logger import logger


def _is_colab():
    import sys

    return "google.colab.output" in sys.modules


class Area:
    """This class represents an area of interest."""

    layers: dict[str, BaseLayer]

    def __init__(
        self,
        layer_or_layers: BaseLayer | dict[str, BaseLayer],
        *,
        base_layer_name: str = "bldg",
    ) -> None:
        """Initialize an area of interest.

        Args:
            layer_or_layers: Layer or a dictionary of layers.
            base_layer_name: Name of the base layer. Default is "bldg".
        """
        if isinstance(layer_or_layers, BaseLayer):
            base_layer = layer_or_layers
            layers = {base_layer_name: base_layer}
        elif isinstance(layer_or_layers, dict):
            if base_layer_name is None:
                raise ValueError(
                    "base_layer_name is required when layer_or_layers is a dictionary"
                )
            layers = layer_or_layers
            base_layer = layers[base_layer_name]

        self.layers = layers
        self.base_layer = base_layer
        self.base_layer_name = base_layer_name

        self._datasets: list[str] | None = None

    def __repr__(self) -> str:
        return "Area()"

    @property
    def gdf(self):
        # NOTE: For backward compatibility
        if "bldg" in self.layers and isinstance(self.layers["bldg"], GeoDataFrameLayer):
            return self.layers["bldg"].gdf
        else:
            raise RuntimeError()

    @gdf.setter
    def gdf(self, value):
        # NOTE: For backward compatibility
        if "bldg" in self.layers and isinstance(self.layers["bldg"], GeoDataFrameLayer):
            self.layers["bldg"].gdf = value
        else:
            raise RuntimeError()

    def get_area(self, bbox: list[float] | None = None):
        """Get the specified area from the dataset.

        Args:
            bbox: Bounding box of the area of interest.
                   If not specified, the area of the entire dataset will be returned.
        """

        layers = {name: layer.get_area(bbox) for name, layer in self.layers.items()}

        return Area(layers, base_layer_name=self.base_layer_name)

    def get_centroid(self) -> list[float]:
        """Get the centroid of the area of interest."""

        bbox = self.gdf.total_bounds
        return [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]

    def pydeck(self, opacity: float = 1):
        # cx, cy = self.get_centroid()

        bbox = self.gdf.total_bounds
        points = [(bbox[0], bbox[1]), (bbox[2], bbox[3])]
        # print(points)

        view_state = pydeck.data_utils.compute_view(points, view_proportion=1)
        view_state.pitch = 45

        deck = pydeck.Deck(
            layers=[
                pydeck.Layer(
                    "GeoJsonLayer",
                    data=self.gdf,
                    filled=True,
                    get_fill_color="fill_color || color || [255, 255, 255]",
                    # get_fill_color=[255, 255, 255, 240],
                    # get_line_color=[255, 255, 255],
                    opacity=opacity,
                    extruded=True,
                    # wireframe=True,
                    get_elevation="measuredHeight",
                    pickable=True,
                    auto_highlight=True,
                )
                # pydeck.Layer(
                #     "PolygonLayer",
                #     data=self.gdf,
                #     get_polygon="geometry.coordinates",
                #     filled=True,
                #     stroked=False,
                #     get_fill_color=[0, 0, 0, 20],
                #     get_line_color=[0, 0, 0, 20],
                # )
            ],
            initial_view_state=view_state,
            # initial_view_state=pydeck.ViewState(
            #     latitude=cy,
            #     longitude=cx,
            #     zoom=1,
            #     pitch=0,
            #     bearing=0,
            # ),
            tooltip={
                "style": {
                    "font-family": "sans-serif",
                    "font-size": "8px",
                    "color": "white",
                },
            },
        )

        return deck

    def ipydeck(self, opacity: float = 1):
        bbox = self.gdf.total_bounds
        points = [(bbox[0], bbox[1]), (bbox[2], bbox[3])]
        # print(points)

        view_state = pydeck.data_utils.compute_view(points, view_proportion=1)
        # print(view_state, type(view_state))
        view_state.pitch = 45

        view_state = ipydeck.ViewState(
            **{
                "longitude": view_state.longitude,
                "latitude": view_state.latitude,
                "zoom": view_state.zoom,
                "min_zoom": view_state.min_zoom,
                "max_zoom": view_state.max_zoom,
                "pitch": view_state.pitch,
                "bearing": view_state.bearing,
            }
        )

        deck = ipydeck.Deck(
            layers=[
                ipydeck.Layer(
                    "GeoJsonLayer",
                    data=self.gdf,
                    filled=True,
                    get_fill_color="@@=(properties.fill_color || properties.color || [255, 255, 255])",
                    # get_fill_color=[255, 255, 255, 240],
                    # get_line_color=[255, 255, 255],
                    opacity=opacity,
                    extruded=True,
                    # wireframe=True,
                    get_elevation="@@=properties.measuredHeight",
                    pickable=True,
                    auto_highlight=True,
                )
            ],
            initial_view_state=view_state,
            # tooltip={
            #     "style": {
            #         "font-family": "sans-serif",
            #         "font-size": "8px",
            #         "color": "white",
            #     },
            # },
        )

        return deck

    def _show_pydeck(self):
        deck = self.pydeck()

        deck._tooltip = {
            "html": "<b>ID:</b> {buildingId}",
            "style": {
                "font-family": "sans-serif",
                "font-size": "8px",
                "color": "white",
            },
        }

        try:
            if __IPYTHON__:  # type: ignore
                return deck.to_html()
        except Exception:
            pass

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as fp:
            deck.to_html(fp.name, open_browser=True)

    def _show_ipydeck(self):
        deck = InteractiveDeck(self.gdf)

        self.selection = deck.selection

        if _is_colab():
            return deck.deck
        else:
            return deck.widget

    def show(
        self,
        renderer: Literal["pydeck", "ipydeck"] = "ipydeck",
        # interactive: bool = True,
        embed: bool = True,
    ):
        if renderer == "pydeck":
            return self._show_pydeck()
        elif renderer == "ipydeck":
            return self._show_ipydeck()
        else:
            raise ValueError(f"Unknown renderer: {renderer}")

    def dict(self):
        return self.gdf.to_dict()

    def to_geojson(self, file: str | None = None):
        """Export the area in GeoJSON format."""

        # TODO: Support GeoJSONSeq

        data = self.gdf.to_json(ensure_ascii=False)

        if file is not None:
            with open(file, "w") as f:
                f.write(data)
        else:
            return data

    def to_cityjson(
        self,
        file: str,
        *,
        types: list[str] | None = None,
        ground: bool = False,
        seq: bool = False,
        target_epsg: int | None = None,
    ):
        """Export the area in CityJSON format."""

        # TODO: Support IOBase as file

        from plateaukit import Dataset

        if self._datasets is None:
            raise RuntimeError("Missing dataset information")

        # TODO: Support non-building types
        # selection = self.gdf["buildingId"].tolist()
        selection = sum(
            [layer.gdf["gmlId"].tolist() for layer in self.layers.values()], []
        )
        logger.debug(selection)

        config = Config()

        for dataset_id in self._datasets:
            # TODO: The path must be in config
            co_parquet_path = Path(config.data_dir, f"{dataset_id}.cityobjects.parquet")

            if seq and co_parquet_path.exists():
                selection = sum(
                    [layer.gdf["gmlId"].tolist() for layer in self.layers.values()], []
                )
                df = pd.read_parquet(co_parquet_path)
                # Get rows where df._id in selection:
                df = df[df._id.isin(selection)]
                # Write value of `cityjson` row of each row to a line in the file.
                cjseq_header = (
                    '{"type":"CityJSON","version":"2.0","transform":{"scale":[1.0,1.0,1.0],"translate":[0.0,0.0,0.0]},'
                    + '"metadata":{"referenceSystem":"https://www.opengis.net/def/crs/EPSG/0/3857"},"vertices":[]}'
                )
                with open(file, "w") as f:
                    f.write(cjseq_header + "\n")
                    for row in df.itertuples():
                        f.write(str(row.cityjson) + "\n")
            else:
                dataset = Dataset(dataset_id)
                types = list(self.layers.keys()) if types is None else types
                dataset.to_cityjson(
                    file,
                    types=types,
                    ground=ground,
                    selection=selection,
                    target_epsg=target_epsg,
                    seq=seq,
                )

    def set_llm(self, llm):
        self.llm = llm

    def chat(
        self, message: str, *, output_format: Literal["map", "dataframe"] | None = "map"
    ):
        """LLM-based chat interface for the area of interest using LangChain."""

        import geopandas as gpd

        try:
            from langchain_core.output_parsers.openai_tools import (
                JsonOutputKeyToolsParser,
            )
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_experimental.tools import PythonAstREPLTool
        except ImportError:
            raise ImportError(
                "Please install langchain-core and langchain-experimental to use this feature."
            )

        if not hasattr(self, "llm") or self.llm is None:
            raise RuntimeError(
                "Set LangChain's LLM instance with set_llm() method first."
            )

        llm = self.llm

        df = self.gdf.copy()

        tool = PythonAstREPLTool(globals={"df": df}, verbose=True)
        tool.locals = tool.globals
        llm_with_tools = llm.bind_tools([tool], tool_choice=tool.name)
        parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)

        system = dedent(
            f"""You have access to a geopandas dataframe called `df`.
            Please output Python code in response to the user's instructions. Do not output anything else.
            The following is the result of executing `df.head().to_markdown()`:
            {df.head().to_markdown()}
            The following is a description of the items in this dataframe:
            - buildingId: The ID of the building
            - name: The name of the building. Always look for the name of the building in this field
            - measuredHeight: The measured height of the building
            - storeysAboveGround: The number of floors above ground
            - storeysBelowGround: The number of floors below ground
            - usage: The usage of the building
            - longitude: The latitude of the building
            - latitude: The longitude of the building
            The following is a list of buildings whose names exist in this dataframe:
            {df['name'].unique()}
            The following is a list of the usage types of buildings that exist in this data frame:
            {df['usage'].unique()}
            Again, please output Python code in response to the user's instructions. Do not output anything else.
            Do not use any knowledge about the coordinates other than the dataframe.
            Only the standard Python libraries, pandas, and geopandas can be used as libraries.
            Be sure to write Python code that returns a pandas dataframe."""
        )

        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", "{input}")]
        )

        chain = prompt | llm_with_tools | parser | tool

        response = chain.invoke(message)

        if isinstance(response, gpd.GeoDataFrame) and output_format == "map":
            deck = InteractiveDeck(response)

            self.selection = deck.selection

            if _is_colab():
                return deck.deck
            else:
                return deck.widget

        return response

    @property
    def buildings(self):
        from plateaukit.core.models import Building

        # TODO: Filter and return buildings only

        for row in self.gdf.itertuples():
            df = self.gdf.loc[[row.Index]]

            yield Building(df)
