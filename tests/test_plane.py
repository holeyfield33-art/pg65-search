"""Tests for projective plane generation."""

from pg65_search.plane import projective_plane
from pg65_search.projective import BASIS, generate_all_points, point_to_id


def test_plane_size():
    generate_all_points()
    a, b, c = BASIS[0], BASIS[1], BASIS[2]
    plane = projective_plane(a, b, c)
    assert len(plane) == 31
    assert len(set(plane)) == 31


def test_plane_contains_generators():
    generate_all_points()
    a, b, c = BASIS[0], BASIS[1], BASIS[2]
    plane = set(projective_plane(a, b, c))
    assert point_to_id(a) in plane
    assert point_to_id(b) in plane
    assert point_to_id(c) in plane
