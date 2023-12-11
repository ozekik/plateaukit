import tempfile

from geopandas import GeoDataFrame


class Area:
    """This class represents an area of interest."""

    gdf: GeoDataFrame

    def __init__(self, gdf: GeoDataFrame) -> None:
        """Initialize an area from a GeoDataFrame.

        Args:
            gdf: GeoDataFrame of the area of interest.
        """
        self.gdf = gdf

    def __repr__(self) -> str:
        return f"Area()"

    def get_area(self, bbox: list[float] | None = None):
        """Get the specified area from the dataset.

        Args:
            bbox: Bounding box of the area of interest.
                   If not specified, the area of the entire dataset will be returned.
        """

        area_gdf = (
            self.gdf.cx[bbox[0] : bbox[2], bbox[1] : bbox[3]] if bbox else self.gdf
        )

        # TODO: Error handling when area_gdf is empty

        return Area(area_gdf)

    def get_centroid(self) -> list[float]:
        """Get the centroid of the area of interest."""

        bbox = self.gdf.total_bounds
        return [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]

    def show(self, embed: bool = True):
        import pydeck

        # cx, cy = self.get_centroid()

        bbox = self.gdf.total_bounds
        points = [(bbox[0], bbox[1]), (bbox[2], bbox[3])]
        # print(points)

        view_state = pydeck.data_utils.compute_view(points, view_proportion=1)
        view_state.pitch = 45

        deck = pydeck.Deck(
            layers=[
                # pydeck.Layer(
                #     "PolygonLayer",
                #     data=self.gdf,
                #     get_polygon="geometry.coordinates",
                #     filled=True,
                #     stroked=False,
                #     get_fill_color=[0, 0, 0, 20],
                #     get_line_color=[0, 0, 0, 20],
                # )
                pydeck.Layer(
                    "GeoJsonLayer",
                    data=self.gdf,
                    filled=True,
                    get_fill_color="fill_color || color || [255, 255, 255]",
                    # get_fill_color=[255, 255, 255, 240],
                    # get_line_color=[255, 255, 255],
                    extruded=True,
                    # wireframe=True,
                    get_elevation="measuredHeight",
                    pickable=True,
                )
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
                "html": "<b>ID:</b> {buildingId}",
                "style": {
                    "font-family": "sans-serif",
                    "font-size": "8px",
                    "color": "white",
                },
            },
        )

        try:
            if __IPYTHON__:  # type: ignore
                return deck.to_html()
        except:
            pass

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as fp:
            deck.to_html(fp.name, open_browser=True)

        # raise NotImplementedError()

    def dict(self):
        return self.gdf.to_dict()

    def to_geojson(self):
        """Convert the area to GeoJSON."""

        data = self.gdf.to_json()
        # print(data)
        return data

    def to_cityjson(self):
        """Convert the area to CityJSON."""

        raise NotImplementedError()

    @property
    def buildings(self):
        from plateaukit.models import Building

        # TODO: Filter and return buildings only

        for row in self.gdf.itertuples():
            df = self.gdf.loc[[row.Index]]

            yield Building(df)
