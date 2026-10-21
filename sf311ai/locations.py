"""Validate explicit image locations before any submission."""

import math
from typing import TypedDict


class Location(TypedDict):
    lat: float
    long: float


def validate_location(value: object) -> Location:
    if not isinstance(value, dict):
        raise ValueError(
            "Each submitted image requires an explicit lat/long location"
        )
    lat, lon = value.get("lat"), value.get("long")
    if (
        isinstance(lat, bool)
        or isinstance(lon, bool)
        or not isinstance(lat, (int, float))
        or not isinstance(lon, (int, float))
        or not math.isfinite(lat)
        or not math.isfinite(lon)
        or not -90 <= lat <= 90
        or not -180 <= lon <= 180
        or (lat == 0 and lon == 0)
    ):
        raise ValueError(
            "Location requires finite coordinates and cannot be 0,0"
        )
    return {"lat": float(lat), "long": float(lon)}
