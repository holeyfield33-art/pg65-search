"""Tests for rank and verifier."""

from pg65_search.verify import rank_mod5, verify_points
from pg65_search.projective import BASIS


def test_rank_identity():
    I = [[1 if i == j else 0 for j in range(7)] for i in range(7)]
    assert rank_mod5(I) == 7


def test_rank_deficient():
    M = [[1, 0, 0], [0, 1, 0], [2, 3, 0]]
    assert rank_mod5(M) == 2


def test_rank_full_small():
    M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert rank_mod5(M) == 3


def test_verifier_accepts_basis():
    v = verify_points(BASIS)
    assert v["rank"] == 7
    assert v["dependent_quadruples"] == 0
    assert v["verified"] is True


def test_verifier_rejects_dependent():
    pts = [BASIS[0], BASIS[0], BASIS[1], BASIS[2], BASIS[3], BASIS[4], BASIS[5]]
    v = verify_points(pts)
    assert v["verified"] is False
