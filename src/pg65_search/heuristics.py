"""Candidate scoring heuristics."""

from __future__ import annotations

from .state import SearchState
from .projective import id_to_point
from .plane import projective_plane


def score_candidate(pid: int, state: SearchState) -> int:
    """
    Fast approximate score: sample a few pairs and count newly blocked legal points.
    Lower score is preferred.
    """
    p = id_to_point(pid)
    newly_blocked = 0
    legal = set(state.legal_candidates())
    selected = state.selected
    n = len(selected)
    # Sample up to 20 pairs for speed
    step = max(1, n // 6)
    pairs = 0
    for i in range(0, n, step):
        for j in range(i + 1, n, step):
            a = id_to_point(selected[i])
            b = id_to_point(selected[j])
            plane = projective_plane(p, a, b)
            for x in plane:
                if x in legal and x != pid:
                    newly_blocked += 1
            pairs += 1
            if pairs >= 20:
                return newly_blocked
    return newly_blocked
