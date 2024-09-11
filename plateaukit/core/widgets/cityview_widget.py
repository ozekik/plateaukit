from typing import Literal
import cityview as cv
import geopandas as gpd
import ipywidgets as widgets
from IPython.display import display

import plateaukit.core as core


class CityViewWidget:
    def __init__(
        self,
        area,
        *,
        mode: Literal["virtual", "map"] = "virtual",
        theme: Literal["light", "dark"] = "light",
    ) -> None:
        from io import StringIO

        sink = StringIO()
        area.to_cityjson(sink, target_epsg=4326, seq=True)
        cjseq_data = sink.read()

        self.cjseq_data = cjseq_data

        if mode == "map":
            self.cityview = cv.MapView(theme=theme)
        else:
            self.cityview = cv.VirtualView(theme=theme)

        layers = [cv.CityJSONLayer(data=cjseq_data, format="cityjsonseq")]
        self.cityview.layers = layers
        self.cityview.update()

        self.widget = self.cityview

        # TODO: Fix code below; somehow not working in Google Colab

        # # Set selection area
        # empty_gdf = gpd.GeoDataFrame()

        # # TODO: Fix this; related to circular import
        # layer = core.area.GeoDataFrameLayer(empty_gdf)

        # # TODO: Fix this; related to circular import
        # self.selection = core.area.Area(layer, base_layer_name="bldg")

        # self._widget_df = area.gdf.copy()

        # self.out = widgets.Output()

        # def display_df():
        #     with self.out:
        #         display(self._widget_df, clear=True)

        #     return self.out

        # # self.cityview.observe(self.click_handler, names="click")

        # self.widget = widgets.VBox([self.cityview, self.out])

    def click_handler(self, change):
        pass
        # feature = change["new"]
        # print("clicked", feature)

        # if "fill_color" in feature["properties"]:
        #     del feature["properties"]["fill_color"]

        # pyogrio_invalid_chars_regex = re.compile(r"[;]")

        # for key, value in feature["properties"].items():
        #     if isinstance(value, str) and pyogrio_invalid_chars_regex.search(value):
        #         feature["properties"][key] = feature["properties"][key].replace(
        #             ";", ","
        #         )

        # # NOTE: https://github.com/heremaps/xyz-spaces-python/pull/115
        # buf = json.dumps(feature)
        # row = gpd.read_file(StringIO(buf))

        # if self.selection.gdf.empty:
        #     self.selection.gdf = row
        # else:
        #     # If self.selection.gdf contains the row, remove it
        #     if row.at[0, "buildingId"] in self.selection.gdf["buildingId"].values:
        #         self.selection.gdf = self.selection.gdf[
        #             ~self.selection.gdf.loc[:, "buildingId"].isin(row["buildingId"])
        #         ]
        #     else:
        #         self.selection.gdf = pd.concat([self.selection.gdf, row])

        # overlap_df = self._widget_df.loc[
        #     self._widget_df.loc[:, "buildingId"].isin(self.selection.gdf["buildingId"])
        # ]

        # # Add fill_color column to df if it doesn't exist
        # if "fill_color" not in self._widget_df.columns:
        #     self._widget_df.loc[:, "fill_color"] = None

        # self._widget_df["fill_color"] = self._widget_df.loc[
        #     self._widget_df.index.isin(overlap_df.index), "fill_color"
        # ].apply(lambda x: [255, 0, 0])

        # updated_layer = self._create_building_layer(self._widget_df)
        # self.deck.layers = [updated_layer]

        # self.deck.update()

        # # Delete fill_color column
        # self._widget_df.drop(columns=["fill_color"], inplace=True)

        # with self.out:
        #     # print("clicked", feature)
        #     display(
        #         self._widget_df.iloc[self._widget_df.index.isin(overlap_df.index)],
        #         clear=True,
        #     )
