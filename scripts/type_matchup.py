#!/usr/bin/env python3
"""Pokemon type-effectiveness lookup for text-first agent workflows."""

from __future__ import annotations

import argparse
import json
import sys
from functools import reduce
from operator import mul

TYPES = [
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy",
]

IMMUNE = {
    "normal": ["ghost"],
    "electric": ["ground"],
    "fighting": ["ghost"],
    "poison": ["steel"],
    "ground": ["flying"],
    "psychic": ["dark"],
    "ghost": ["normal"],
    "dragon": ["fairy"],
}

SUPER = {
    "fire": ["grass", "ice", "bug", "steel"],
    "water": ["fire", "ground", "rock"],
    "electric": ["water", "flying"],
    "grass": ["water", "ground", "rock"],
    "ice": ["grass", "ground", "flying", "dragon"],
    "fighting": ["normal", "ice", "rock", "dark", "steel"],
    "poison": ["grass", "fairy"],
    "ground": ["fire", "electric", "poison", "rock", "steel"],
    "flying": ["grass", "fighting", "bug"],
    "psychic": ["fighting", "poison"],
    "bug": ["grass", "psychic", "dark"],
    "rock": ["fire", "ice", "flying", "bug"],
    "ghost": ["psychic", "ghost"],
    "dragon": ["dragon"],
    "dark": ["psychic", "ghost"],
    "steel": ["ice", "rock", "fairy"],
    "fairy": ["fighting", "dragon", "dark"],
}

RESIST = {
    "normal": ["rock", "steel"],
    "fire": ["fire", "water", "rock", "dragon"],
    "water": ["water", "grass", "dragon"],
    "electric": ["electric", "grass", "dragon"],
    "grass": ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"],
    "ice": ["fire", "water", "ice", "steel"],
    "fighting": ["poison", "flying", "psychic", "bug", "fairy"],
    "poison": ["poison", "ground", "rock", "ghost"],
    "ground": ["grass", "bug"],
    "flying": ["electric", "rock", "steel"],
    "psychic": ["psychic", "steel"],
    "bug": ["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"],
    "rock": ["fighting", "ground", "steel"],
    "ghost": ["dark"],
    "dragon": ["steel"],
    "dark": ["fighting", "dark", "fairy"],
    "steel": ["fire", "water", "electric", "steel"],
    "fairy": ["fire", "poison", "steel"],
}


def normalize_type(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in TYPES:
        raise ValueError(f"unknown type: {value!r}; expected one of {', '.join(TYPES)}")
    return normalized


def multiplier(attack: str, defend: str) -> float:
    attack = normalize_type(attack)
    defend = normalize_type(defend)
    if defend in IMMUNE.get(attack, []):
        return 0.0
    if defend in SUPER.get(attack, []):
        return 2.0
    if defend in RESIST.get(attack, []):
        return 0.5
    return 1.0


def combined_multiplier(attack: str, defenders: list[str]) -> float:
    defenders = [normalize_type(t) for t in defenders]
    return reduce(mul, (multiplier(attack, defender) for defender in defenders), 1.0)


def label(value: float) -> str:
    labels = {
        0.0: "immune (0x)",
        0.25: "double resisted (0.25x)",
        0.5: "not very effective (0.5x)",
        1.0: "neutral (1x)",
        2.0: "super effective (2x)",
        4.0: "double super effective (4x)",
    }
    return labels.get(value, f"{value:g}x")


def matrix() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for attack in TYPES:
        row: dict[str, float | str] = {"attack": attack}
        for defend in TYPES:
            row[defend] = multiplier(attack, defend)
        rows.append(row)
    return rows


def markdown_matrix() -> str:
    header = "| attack \\ defend | " + " | ".join(TYPES) + " |"
    sep = "|" + "|".join(["---"] * (len(TYPES) + 1)) + "|"
    lines = [header, sep]
    for row in matrix():
        lines.append("| " + str(row["attack"]) + " | " + " | ".join(f"{row[t]:g}" for t in TYPES) + " |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute Pokemon type effectiveness.")
    parser.add_argument("--attack", help="Attacking move type.")
    parser.add_argument("--defend", nargs="+", help="One or two defending Pokemon types.")
    parser.add_argument("--defense-types", nargs="+", help="Show all attacking multipliers into these defending types.")
    parser.add_argument("--matrix", choices=["json", "markdown"], help="Print the full attack-by-defense type matrix.")
    args = parser.parse_args()

    try:
        if args.matrix:
            print(json.dumps(matrix(), indent=2) if args.matrix == "json" else markdown_matrix())
            return 0
        if args.attack and args.defend:
            value = combined_multiplier(args.attack, args.defend)
            print(json.dumps({
                "attack": normalize_type(args.attack),
                "defend": [normalize_type(t) for t in args.defend],
                "multiplier": value,
                "label": label(value),
            }, indent=2))
            return 0
        if args.defense_types:
            defenders = [normalize_type(t) for t in args.defense_types]
            result = [
                {"attack": attack, "multiplier": combined_multiplier(attack, defenders), "label": label(combined_multiplier(attack, defenders))}
                for attack in TYPES
            ]
            print(json.dumps({"defend": defenders, "incoming": result}, indent=2))
            return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    parser.error("provide --attack with --defend, --defense-types, or --matrix")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
