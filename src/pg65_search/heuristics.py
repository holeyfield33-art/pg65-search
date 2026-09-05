"""Candidate scoring heuristics."""

from __future__ import annotations

from .state import SearchState
from .projective import id_to_point
from .plane import projective_plane


def score_candidate(pid: int, state: SearchState) -> int:
    """Estimate newly blocked legal points; lower is better."""
    p = id_to_point(pid)
    newly_blocked = 0
    legal = set(state.legal_candidates())
    for i in range(len(state.selected)):
        for j in range(i + 1, len(state.selected)):
            a = id_to_point(state.selected[i])
            b = id_to_point(state.selected[j])
            plane = projective_plane(p, a, b)
            for x in plane:
                if x in legal and x != pid:
                    newly_blocked += 1
    return newly_blocked
