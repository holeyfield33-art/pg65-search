"""Tests for projective point generation."""

from pg65_search.projective import (
    BASIS, generate_all_points, id_to_point, normalize, num_points, point_to_id,
)


def test_count():
    pts = generate_all_points()
    assert len(pts) == 19531
    assert num_points() == 19531


def test_normalization():
    pts = generate_all_points()
    for p in pts:
        for c in p:
            if c != 0:
                assert c == 1
                break


def test_scalar_equivalence():
    v = (2, 3, 0, 1, 4, 0, 2)
    p1 = normalize(v)
    p2 = normalize([(3 * x) % 5 for x in v])
    assert p1 == p2


def test_basis():
    for bp in BASIS:
        assert normalize(bp) == bp


def test_id_roundtrip():
    generate_all_points()
    for i in range(100):
        p = id_to_point(i)
        assert point_to_id(p) == i
