"""Independent verifier for 4-general sets / parity-check matrices over GF(5)."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Sequence

from .field import inv, mul
from .projective import Point, normalize


def rank_mod5(matrix: list[list[int]]) -> int:
    """Exact rank of a matrix over GF(5) via Gaussian elimination."""
    if not matrix:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    A = [[c % 5 for c in row] for row in matrix]
    rank = 0
    col = 0
    for r in range(rows):
        pivot = -1
        while col < cols:
            for i in range(r, rows):
                if A[i][col] != 0:
                    pivot = i
                    break
            if pivot != -1:
                break
            col += 1
        if pivot == -1:
            break
        A[r], A[pivot] = A[pivot], A[r]
        piv_val = A[r][col]
        scale = inv(piv_val)
        for j in range(cols):
            A[r][j] = mul(A[r][j], scale)
        for i in range(rows):
            if i != r and A[i][col] != 0:
                factor = A[i][col]
                for j in range(cols):
                    A[i][j] = (A[i][j] - mul(factor, A[r][j])) % 5
        rank += 1
        col += 1
    return rank


def verify_points(points: Sequence[Point]) -> dict:
    n = len(points)
    result = {
        "n": n, "rank": None, "quadruples_checked": 0,
        "dependent_quadruples": 0, "dependent_indices": [],
        "verified": False, "errors": [],
    }
    for i, p in enumerate(points):
        if all(c == 0 for c in p):
            result["errors"].append(f"Column {i} is zero")
        if p != normalize(p):
            result["errors"].append(f"Column {i} is not normalized")
    if len(set(points)) != n:
        result["errors"].append("Duplicate projective points present")
    if result["errors"]:
        return result
    H = [[points[j][i] for j in range(n)] for i in range(7)]
    r = rank_mod5(H)
    result["rank"] = r
    if r != 7:
        result["errors"].append(f"Matrix rank is {r}, expected 7")
    dependent = []
    checked = 0
    for idxs in itertools.combinations(range(n), 4):
        sub = [[H[row][c] for c in idxs] for row in range(7)]
        if rank_mod5(sub) < 4:
            dependent.append(list(idxs))
        checked += 1
        if len(dependent) >= 5:
            break
    result["quadruples_checked"] = checked
    result["dependent_quadruples"] = len(dependent)
    result["dependent_indices"] = dependent[:10]
    if not dependent and r == 7 and not result["errors"]:
        result["verified"] = True
    return result


def verify_matrix_file(path: str | Path) -> dict:
    path = Path(path)
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rows.append([int(x) for x in line.split()])
    if len(rows) != 7:
        return {"verified": False, "errors": [f"Expected 7 rows, got {len(rows)}"]}
    n = len(rows[0])
    points = [tuple(rows[r][c] for r in range(7)) for c in range(n)]
    points = [normalize(p) for p in points]
    return verify_points(points)


def verify_json(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text())
    points = [tuple(p) for p in data["points"]]
    return verify_points(points)
