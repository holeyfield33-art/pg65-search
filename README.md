# pg65-search

Research tool to search for a **spanning 60-point 4-general set** in $\mathrm{PG}(6,5)$.

## Problem

A linear code $[60,53,5]_5$ exists if and only if there is a set of 60 points in the projective space $\mathrm{PG}(6,5)$ that spans the whole space and has **no four points coplanar** (a 4-general set).

Equivalently, we seek a $7\times 60$ parity-check matrix $H$ over $\mathbb{F}_5$ of rank 7 such that every set of four columns is linearly independent.

## Current mathematical status

- Known: a linear $[60,52,\ge 5]_5$ code exists (Grassl / codetables.de).
- Unresolved target: existence of $[60,53,5]_5$ (i.e. $r_5=7$).

Grassl’s tables give $4\le d_5(60,53)\le 5$; no construction achieving distance 5 is recorded.

## Important disclaimer

**A failed heuristic search does not prove nonexistence.**

This tool is a constructive hunter. Absence of a solution after any finite number of restarts or limited backtracks is **not** a mathematical nonexistence proof.

## Success criterion

One independently verified $7\times 60$ matrix over $\mathbb{F}_5$ whose every four columns are linearly independent.

When that certificate is produced the tool prints:

```
F5 FLOOR ACHIEVED: r5=7
```

## Usage

```bash
# Generate the 19531 normalized points
python -m pg65_search generate

# Greedy restart search
python -m pg65_search search --seed 12345 --mode greedy --restarts 100

# Limited backtracking
python -m pg65_search search --seed 12345 --mode backtrack --restarts 50 --backtrack-depth 6

# Verify a saved configuration
python -m pg65_search verify results/best-054-seed-12345.json

# Verify an explicit matrix
python -m pg65_search verify-matrix certificate/H.txt
```

## Project layout

```
src/pg65_search/
  field.py          GF(5) arithmetic
  projective.py     normalized points + IDs
  plane.py          31-point projective planes
  state.py          reversible blocking counters
  heuristics.py     low-conflict candidate scoring
  search.py         greedy / limited-backtrack search
  verify.py         independent rank & 4-column verifier
  certificate.py    export H.txt / verification.json
```

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
