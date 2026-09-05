"""Greedy restart and limited-backtrack search."""

from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import Optional

from .certificate import export_certificate
from .heuristics import score_candidate
from .projective import Point, num_points
from .state import SearchState
from .verify import verify_points


class Searcher:
    def __init__(
        self,
        seed: int = 42,
        mode: str = "greedy",
        backtrack_depth: int = 6,
        candidate_pool: int = 8,
        results_dir: str | Path = "results",
    ) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.mode = mode
        self.backtrack_depth = backtrack_depth
        self.candidate_pool = candidate_pool
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.nodes = 0
        self.restarts = 0
        self.best_depth = 7
        self.best_points: list[Point] = []
        self.start_time = time.time()

    def _choose_candidate(self, state: SearchState) -> Optional[int]:
        cands = state.legal_candidates()
        if not cands:
            return None
        scored = [(score_candidate(c, state), c) for c in cands]
        scored.sort()
        pool = scored[: self.candidate_pool]
        return self.rng.choice(pool)[1]

    def _save_record(self, state: SearchState) -> None:
        depth = state.depth()
        points = state.points()
        stem = f"best-{depth:03d}-seed-{self.seed}"
        data = {
            "field": 5,
            "projective_dimension": 6,
            "size": depth,
            "seed": self.seed,
            "nodes": self.nodes,
            "restarts": self.restarts,
            "points": [list(p) for p in points],
        }
        (self.results_dir / f"{stem}.json").write_text(json.dumps(data, indent=2))
        with (self.results_dir / f"{stem}.txt").open("w") as f:
            for p in points:
                f.write(" ".join(str(x) for x in p) + "\n")
        print(f"NEW RECORD: {depth}  seed={self.seed}  nodes={self.nodes}")

    def _run_one(self) -> int:
        state = SearchState()
        path: list[int] = []
        while True:
            self.nodes += 1
            cand = self._choose_candidate(state)
            if cand is None:
                break
            state.add_point(cand)
            path.append(cand)
            depth = state.depth()
            if depth > self.best_depth:
                self.best_depth = depth
                self.best_points = state.points()
                self._save_record(state)
            if depth >= 60:
                return depth
            if self.mode == "backtrack" and len(path) > self.backtrack_depth:
                if len(state.legal_candidates()) < 5:
                    undo = self.rng.randint(1, self.backtrack_depth)
                    for _ in range(undo):
                        if len(state.selected) <= 7:
                            break
                        state.remove_point()
                        if path:
                            path.pop()
        return state.depth()

    def search(self, restarts: int = 100) -> dict:
        print(f"Starting search mode={self.mode} seed={self.seed} restarts={restarts}")
        print(f"Total projective points: {num_points()}")
        for r in range(restarts):
            self.restarts = r + 1
            self.rng.seed(self.seed + r * 9973)
            depth = self._run_one()
            if depth >= 60:
                v = verify_points(self.best_points)
                if v["verified"]:
                    export_certificate(self.best_points, seed=self.seed)
                    print("F5 FLOOR ACHIEVED: r5=7")
                    print("Verified linear [60,53,>=5]_5 code.")
                    print("Parity-check matrix written to certificate/H.txt")
                    print(f"Checked {v['quadruples_checked']} four-column subsets.")
                    print(f"Dependent quadruples: {v['dependent_quadruples']}")
                    return {"success": True, "depth": 60, "seed": self.seed}
                else:
                    print("WARNING: size-60 found but independent verifier FAILED")
                    print(v)
            if (r + 1) % 10 == 0:
                elapsed = time.time() - self.start_time
                print(
                    f"  restart {r+1}/{restarts}  best={self.best_depth}  "
                    f"nodes={self.nodes}  elapsed={elapsed:.1f}s"
                )
        print("SEARCH FINISHED WITHOUT CONSTRUCTION")
        print(f"best size: {self.best_depth}")
        return {
            "success": False,
            "best_depth": self.best_depth,
            "seed": self.seed,
            "nodes": self.nodes,
            "restarts": self.restarts,
        }
