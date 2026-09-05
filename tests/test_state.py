"""Tests for reversible blocking state."""

from pg65_search.projective import generate_all_points
from pg65_search.state import SearchState


def test_initial_depth():
    generate_all_points()
    s = SearchState()
    assert s.depth() == 7


def test_add_remove_restores():
    generate_all_points()
    s = SearchState()
    before = s.blocked[:]
    cands = s.legal_candidates()
    assert cands
    pid = cands[0]
    s.add_point(pid)
    assert s.depth() == 8
    s.remove_point()
    assert s.depth() == 7
    assert s.blocked == before


def test_counter_never_negative():
    generate_all_points()
    s = SearchState()
    for _ in range(5):
        cands = s.legal_candidates()
        if not cands:
            break
        s.add_point(cands[0])
    while s.depth() > 7:
        s.remove_point()
    assert all(c >= 0 for c in s.blocked)
