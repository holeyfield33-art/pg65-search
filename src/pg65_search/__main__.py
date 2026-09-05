"""CLI entry point for pg65-search."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .projective import generate_all_points
from .search import Searcher
from .verify import verify_json, verify_matrix_file


def cmd_generate(_args: argparse.Namespace) -> None:
    pts = generate_all_points()
    print(f"Generated {len(pts)} normalized points in PG(6,5)")
    assert len(pts) == 19531


def cmd_search(args: argparse.Namespace) -> None:
    searcher = Searcher(
        seed=args.seed,
        mode=args.mode,
        backtrack_depth=args.backtrack_depth,
        candidate_pool=args.candidate_pool,
        results_dir=args.results_dir,
    )
    searcher.search(restarts=args.restarts)


def cmd_verify(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if path.suffix == ".json":
        result = verify_json(path)
    else:
        result = verify_matrix_file(path)
    print(result)
    if result.get("verified"):
        print("VERIFIED OK")
        sys.exit(0)
    else:
        print("VERIFICATION FAILED")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pg65-search",
        description="Search for a 60-point spanning 4-general set in PG(6,5)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate", help="Generate and count projective points")
    p_gen.set_defaults(func=cmd_generate)

    p_search = sub.add_parser("search", help="Run constructive search")
    p_search.add_argument("--seed", type=int, default=42)
    p_search.add_argument("--mode", choices=["greedy", "backtrack"], default="greedy")
    p_search.add_argument("--restarts", type=int, default=100)
    p_search.add_argument("--backtrack-depth", type=int, default=6)
    p_search.add_argument("--candidate-pool", type=int, default=8)
    p_search.add_argument("--results-dir", type=str, default="results")
    p_search.set_defaults(func=cmd_search)

    p_ver = sub.add_parser("verify", help="Verify a saved configuration or matrix")
    p_ver.add_argument("path", type=str)
    p_ver.set_defaults(func=cmd_verify)

    p_vermat = sub.add_parser("verify-matrix", help="Verify an explicit H.txt matrix")
    p_vermat.add_argument("path", type=str)
    p_vermat.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
