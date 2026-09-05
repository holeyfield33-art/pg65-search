"""Projective plane generation over GF(5)."""

from __future__ import annotations

from .field import mul
from .projective import Point, normalize, point_to_id


def projective_plane(a: Point, b: Point, c: Point) -> tuple[int, ...]:
    """
    Return the 31 distinct normalized point IDs in the projective plane
    spanned by three linearly independent points a, b, c.
    """
    ids: set[int] = set()
    for alpha in range(5):
        for beta in range(5):
            for gamma in range(5):
                if alpha == 0 and beta == 0 and gamma == 0:
                    continue
                vec = [
                    (mul(alpha, a[i]) + mul(beta, b[i]) + mul(gamma, c[i])) % 5
                    for i in range(7)
                ]
                p = normalize(vec)
                ids.add(point_to_id(p))
    if len(ids) != 31:
        raise AssertionError(
            f"Expected 31 points in plane, got {len(ids)}. "
            "Input triple may be linearly dependent."
        )
    return tuple(sorted(ids))
