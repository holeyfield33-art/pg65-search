"""Search state with reversible blocking counters."""

from __future__ import annotations

from .plane import projective_plane
from .projective import BASIS, Point, id_to_point, num_points, point_to_id


class SearchState:
    def __init__(self) -> None:
        n = num_points()
        self.blocked: list[int] = [0] * n
        self.selected: list[int] = []
        self.selected_set: set[int] = set()
        self._affected_stack: list[list[tuple[int, ...]]] = []

        for bp in BASIS:
            pid = point_to_id(bp)
            self.selected.append(pid)
            self.selected_set.add(pid)

        for i in range(7):
            for j in range(i + 1, 7):
                for k in range(j + 1, 7):
                    a = id_to_point(self.selected[i])
                    b = id_to_point(self.selected[j])
                    c = id_to_point(self.selected[k])
                    plane = projective_plane(a, b, c)
                    for x in plane:
                        self.blocked[x] += 1

    def is_legal(self, pid: int) -> bool:
        return self.blocked[pid] == 0 and pid not in self.selected_set

    def legal_candidates(self) -> list[int]:
        return [i for i in range(len(self.blocked)) if self.is_legal(i)]

    def add_point(self, pid: int) -> list[tuple[int, ...]]:
        if not self.is_legal(pid):
            raise ValueError(f"Point {pid} is not legal")
        p = id_to_point(pid)
        affected: list[tuple[int, ...]] = []
        for i in range(len(self.selected)):
            for j in range(i + 1, len(self.selected)):
                a = id_to_point(self.selected[i])
                b = id_to_point(self.selected[j])
                plane = projective_plane(p, a, b)
                for x in plane:
                    self.blocked[x] += 1
                affected.append(plane)
        self.selected.append(pid)
        self.selected_set.add(pid)
        self._affected_stack.append(affected)
        return affected

    def remove_point(self) -> None:
        if not self.selected or not self._affected_stack:
            raise RuntimeError("Nothing to remove")
        if len(self.selected) <= 7:
            raise RuntimeError("Cannot remove basis points")
        affected = self._affected_stack.pop()
        pid = self.selected.pop()
        self.selected_set.remove(pid)
        for plane in affected:
            for x in plane:
                self.blocked[x] -= 1
                if self.blocked[x] < 0:
                    raise AssertionError("Blocking counter went negative")

    def depth(self) -> int:
        return len(self.selected)

    def points(self) -> list[Point]:
        return [id_to_point(i) for i in self.selected]
