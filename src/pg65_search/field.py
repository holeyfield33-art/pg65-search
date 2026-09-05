"""GF(5) arithmetic utilities."""

from __future__ import annotations

# Multiplicative inverses modulo 5
INV = [0, 1, 3, 2, 4]  # 0 unused; 1*1=1, 2*3=6≡1, 3*2=6≡1, 4*4=16≡1


def add(a: int, b: int) -> int:
    return (a + b) % 5


def sub(a: int, b: int) -> int:
    return (a - b) % 5


def mul(a: int, b: int) -> int:
    return (a * b) % 5


def inv(a: int) -> int:
    if a % 5 == 0:
        raise ZeroDivisionError("No inverse for 0 in GF(5)")
    return INV[a % 5]


def neg(a: int) -> int:
    return (-a) % 5
