"""Export verified certificates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from .projective import Point
from .verify import verify_points


def export_certificate(
    points: Sequence[Point],
    out_dir: str | Path = "certificate",
    seed: int | None = None,
) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n = len(points)
    H = [[points[j][i] for j in range(n)] for i in range(7)]
    h_txt = out_dir / "H.txt"
    with h_txt.open("w") as f:
        f.write(f"# Parity-check matrix for [60,53,>=5]_5 over GF(5)\n")
        f.write(f"# seed={seed}\n")
        for row in H:
            f.write(" ".join(str(x) for x in row) + "\n")
    h_json = {
        "field": 5, "n": n, "k": n - 7, "seed": seed,
        "matrix": H, "points": [list(p) for p in points],
    }
    (out_dir / "H.json").write_text(json.dumps(h_json, indent=2))
    v = verify_points(points)
    v["field"] = 5
    v["k"] = n - (v.get("rank") or 0)
    (out_dir / "verification.json").write_text(json.dumps(v, indent=2))
    return v
