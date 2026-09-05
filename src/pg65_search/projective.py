"""Normalized projective points in PG(6,5)."""

from __future__ import annotations

from typing import Iterable

from .field import inv

Point = tuple[int, int, int, int, int, int, int]

# Deterministic ID mappings (stable across runs)
_point_to_id: dict[Point, int] = {}
_id_to_point: list[Point] = []


def normalize(v: Iterable[int]) -> Point:
    """Normalize a nonzero 7-vector so the first nonzero coordinate is 1."""
    coords = [int(x) % 5 for x in v]
    if all(c == 0 for c in coords):
        raise ValueError("Cannot normalize the zero vector")
    for i, c in enumerate(coords):
        if c != 0:
            scale = inv(c)
            return tuple((scale * x) % 5 for x in coords)
    raise RuntimeError("unreachable")


def generate_all_points() -> list[Point]:
    """Generate all (5^7 - 1)/(5 - 1) = 19531 normalized points."""
    global _point_to_id, _id_to_point
    points: list[Point] = []
    seen: set[Point] = set()
    for i in range(1, 5**7):  # skip zero
        coords = []
        n = i
        for _ in range(7):
            coords.append(n % 5)
            n //= 5
        coords = coords[::-1]
        p = normalize(coords)
        if p not in seen:
            seen.add(p)
            points.append(p)
    points.sort()  # deterministic order
    _id_to_point = points
    _point_to_id = {p: i for i, p in enumerate(points)}
    return points


def point_to_id(p: Point) -> int:
    if not _point_to_id:
        generate_all_points()
    return _point_to_id[p]


def id_to_point(i: int) -> Point:
    if not _id_to_point:
        generate_all_points()
    return _id_to_point[i]


def num_points() -> int:
    if not _id_to_point:
        generate_all_points()
    return len(_id_to_point)


# Basis points (standard projective basis)
BASIS: list[Point] = [
    (1, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 1, 0, 0),
    (0, 0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 0, 1),
]
