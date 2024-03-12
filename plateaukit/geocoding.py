# %%
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Annotated, Optional, Sequence

import requests
from normalize_japanese_addresses import normalize
from pyproj import Transformer
from pyproj.enums import TransformDirection

wgs84_to_sm = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)


@dataclass
class PostalAddress:
    prefecture: str
    address1: str
    address2: str
    address3: str
    address4: str


@dataclass
class AddressPoint:
    lat: Optional[float]
    lng: Optional[float]
    prefecture: str
    city: str
    town: str
    addr: Optional[str]


@dataclass
class LandmarkPoint:
    lat: float
    lng: float
    name: str


@dataclass
class ResultPoint:
    lng: float
    lat: float
    all: Optional[list[AddressPoint | LandmarkPoint]] = None


def _get_bbox(
    points: list[Annotated[Sequence[float], 2] | Annotated[Sequence[float], 3]]
):
    """Returns a bounding box from a list of points."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    return [min(xs), min(ys), max(xs), max(ys)]


def _get_bbox_centroid(bbox: list[float]):
    """Returns a centroid from a bounding box."""
    return [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]


def _pad_bbox(bbox: list[float], min_size: Annotated[Sequence[float], 2]):
    """Returns a padded bounding box."""

    # print(bbox)

    bbox_sm = wgs84_to_sm.itransform([(bbox[0], bbox[1]), (bbox[2], bbox[3])])
    bbox_sm = list(bbox_sm)

    top_left, bottom_right = list(map(list, bbox_sm))

    # print(bbox_sm)

    if top_left[0] - bottom_right[0] < min_size[0]:
        top_left[0] -= (min_size[0] - (top_left[0] - bottom_right[0])) / 2
        bottom_right[0] += (min_size[0] - (top_left[0] - bottom_right[0])) / 2
    if top_left[1] - bottom_right[1] < min_size[1]:
        top_left[1] -= (min_size[1] - (top_left[1] - bottom_right[1])) / 2
        bottom_right[1] += (min_size[1] - (top_left[1] - bottom_right[1])) / 2

    bbox_wgs84 = wgs84_to_sm.itransform(
        [top_left, bottom_right], direction=TransformDirection.INVERSE
    )
    bbox_wgs84 = list(map(list, bbox_wgs84))
    bbox_wgs84 = sum(bbox_wgs84, [])
    # print(bbox_wgs84)

    return bbox_wgs84


def address_from_postcode(code: str):
    """Returns an address from a Japanese postal code.

    >>> address_from_postcode("108-0073")
    PostalAddress(prefecture='東京都', address1='港区', address2='三田', address3='', address4='')
    """

    parsed = re.match(r"^([0-9]{3})\-?([0-9]{4})$", code)

    if not parsed:
        raise RuntimeError("Invalid postal code")

    first, second = parsed.groups()
    # Using a fork by arrow-payment of https://madefor.github.io/postal-code-api/api/v1/ . Thanks!
    resp = requests.get(
        f"https://arrow-payment.github.io/postal-code-api/api/v2/{first}/{second}.json"
    )

    if resp.status_code != 200:
        raise RuntimeError("Address not found")

    body = resp.json()
    data = body["data"]

    # # TODO: Support multiple addresses

    try:
        return PostalAddress(
            data[0]["ja"]["prefecture"],
            data[0]["ja"]["address1"],
            data[0]["ja"]["address2"],
            data[0]["ja"]["address3"],
            data[0]["ja"]["address4"],
        )
    except:
        raise RuntimeError()


def point_from_address(address: str):
    """Returns a point from an address.

    >>> from_address("大阪府大阪市北区梅田２丁目２−２")
    Address(prefecture='大阪府', city='大阪市北区', town='梅田二丁目', addr='2-2', lat=34.698571, lng=135.49385)
    """
    normalized_addr = normalize(address)

    return AddressPoint(
        lat=normalized_addr["lat"],
        lng=normalized_addr["lng"],
        prefecture=normalized_addr["pref"],
        city=normalized_addr["city"],
        town=normalized_addr["town"],
        addr=normalized_addr["addr"],
    )


def bbox_from_address(
    address: str, min_size: Annotated[Sequence[float], 2] = [1000, 1000]
):
    """Returns a bounding box from an address."""

    point = point_from_address(address)
    bbox = _get_bbox([(point.lng, point.lat)])
    bbox = _pad_bbox(bbox, min_size)
    return bbox


def point_from_postcode(code: str):
    """Returns a coordinate from a Japanese postal code.

    >>> from_postcode("108-0073")  # doctest: +ELLIPSIS
    Result(lng=139.74034749999998, lat=35.648897000000005, all=[...])
    """
    postal_address = address_from_postcode(code)
    resp = requests.get(
        f"https://geolonia.github.io/japanese-addresses/api/ja/{postal_address.prefecture}/{postal_address.address1}.json"
    )

    if resp.status_code != 200:
        raise RuntimeError("Address not found")

    city_data = resp.json()

    if postal_address.address2:
        town_data = list(
            filter(lambda x: x["town"].startswith(postal_address.address2), city_data)
        )
        # print(town_data)

        bbox = _get_bbox([(x["lng"], x["lat"]) for x in town_data])
        # print(bbox)

        centroid = _get_bbox_centroid(bbox)
        # print(centroid)

        return ResultPoint(
            lng=centroid[0],
            lat=centroid[1],
            all=[
                AddressPoint(
                    lat=x["lat"],
                    lng=x["lng"],
                    prefecture=postal_address.prefecture,
                    city=postal_address.address1,
                    town=x["town"],
                    addr=None,
                )
                for x in town_data
            ],
        )
    else:
        raise NotImplementedError()


def bbox_from_postcode(
    code: str, min_size: Annotated[Sequence[float], 2] = [1000, 1000]
):
    """Returns a bounding box from a Japanese postal code."""

    point = point_from_postcode(code)
    bbox = _get_bbox([(point.lng, point.lat)])
    bbox = _pad_bbox(bbox, min_size)
    return bbox


def point_from_landmark(landmark_name: str):
    """Returns a coordinate from a landmark.

    >>> from_landmark("東京タワー")
    Result(lng=139.745555555, lat=35.658611111, all=[Landmark(name='東京タワー', lat=139.745555555, lng=35.658611111)])
    """
    # Query Wikidata for the coordinate from a landmark name.
    query = """SELECT distinct ?item ?itemLabel ?coordinate_location WHERE {{
        ?item ?label "{label}"@ja;
              wdt:P625 ?coordinate_location.
        ?article schema:about ?item .
        ?article schema:inLanguage "ja" .
        ?article schema:isPartOf <https://ja.wikipedia.org/>.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ja". }}
    }}
    """.format(
        label=landmark_name
    )

    url = "https://query.wikidata.org/sparql"

    r = requests.get(url, params={"format": "json", "query": query})
    data = r.json()

    # print(data)

    records = data["results"]["bindings"]

    if len(records) == 0:
        return None

    def parse_point(literal):
        m = re.match(r"^Point\(([0-9\.]+) ([0-9\.]+)\)$", literal)
        if not m:
            raise RuntimeError("Failed to parse coordinate")

        lng, lat = m.groups()

        return [float(lng), float(lat)]

    coordinate_raw = records[0]["coordinate_location"]["value"]
    lng, lat = parse_point(coordinate_raw)

    return ResultPoint(
        lng=lng,
        lat=lat,
        all=[
            LandmarkPoint(
                *parse_point(record["coordinate_location"]["value"]),
                record["itemLabel"]["value"],
            )
            for record in records
        ],
    )


def bbox_from_landmark(
    landmark_name: str, min_size: Annotated[Sequence[float], 2] = [1000, 1000]
):
    """Returns a bounding box from a landmark."""

    point = point_from_landmark(landmark_name)

    if point is None:
        return None

    bbox = _get_bbox([(point.lng, point.lat)])
    bbox = _pad_bbox(bbox, min_size)

    return bbox
