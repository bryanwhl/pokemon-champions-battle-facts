#!/usr/bin/env python3
"""Fetch Pokemon facts from PokeAPI with explicit source metadata."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

BASE_URL = "https://pokeapi.co/api/v2"


def slug(value: str) -> str:
    return value.strip().lower().replace(" ", "-").replace("_", "-")


def fetch(endpoint: str, name: str) -> dict[str, Any]:
    url = f"{BASE_URL}/{endpoint}/{urllib.parse.quote(slug(name))}/"
    request = urllib.request.Request(url, headers={
        "User-Agent": "pokemon-champions-battle-facts-skill/0.1 (+https://agentskills.io)",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise SystemExit(f"not found in PokeAPI: {endpoint}/{name}") from exc
        raise


def english_name(names: list[dict[str, Any]], fallback: str) -> str:
    for item in names:
        if item.get("language", {}).get("name") == "en":
            return item.get("name", fallback)
    return fallback


def source_meta(endpoint: str, name: str) -> dict[str, str]:
    normalized = slug(name)
    return {
        "source": "PokeAPI",
        "source_url": f"{BASE_URL}/{endpoint}/{normalized}/",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "caveat": "PokeAPI is a canonical Pokemon data reference, not proof of current Pokemon Champions legality or in-game usage.",
    }


def pokemon(name: str) -> dict[str, Any]:
    data = fetch("pokemon", name)
    species = fetch("pokemon-species", data["species"]["name"])
    return {
        **source_meta("pokemon", name),
        "id": data["id"],
        "name": data["name"],
        "display_name": english_name(species.get("names", []), data["name"]),
        "types": [slot["type"]["name"] for slot in sorted(data["types"], key=lambda x: x["slot"])],
        "base_stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
        "abilities": [
            {"name": ability["ability"]["name"], "hidden": ability["is_hidden"], "slot": ability["slot"]}
            for ability in data["abilities"]
        ],
        "height_dm": data["height"],
        "weight_hg": data["weight"],
    }


def move(name: str) -> dict[str, Any]:
    data = fetch("move", name)
    effect = None
    for item in data.get("effect_entries", []):
        if item.get("language", {}).get("name") == "en":
            effect = item.get("short_effect") or item.get("effect")
            break
    return {
        **source_meta("move", name),
        "id": data["id"],
        "name": data["name"],
        "type": data["type"]["name"],
        "damage_class": data["damage_class"]["name"],
        "power": data["power"],
        "accuracy": data["accuracy"],
        "pp": data["pp"],
        "priority": data["priority"],
        "target": data["target"]["name"],
        "effect_chance": data["effect_chance"],
        "effect": effect,
    }


def learnset(name: str, version_group: str | None) -> dict[str, Any]:
    data = fetch("pokemon", name)
    moves = []
    requested = slug(version_group) if version_group else None
    for item in data["moves"]:
        details = item["version_group_details"]
        if requested:
            details = [detail for detail in details if detail["version_group"]["name"] == requested]
        if not details:
            continue
        moves.append({
            "move": item["move"]["name"],
            "methods": sorted({
                detail["move_learn_method"]["name"]
                for detail in details
            }),
            "version_groups": sorted({
                detail["version_group"]["name"]
                for detail in details
            }),
            "min_level": min((detail["level_learned_at"] for detail in details if detail["level_learned_at"]), default=0),
        })
    moves.sort(key=lambda item: item["move"])
    return {
        **source_meta("pokemon", name),
        "name": data["name"],
        "version_group_filter": requested,
        "move_count": len(moves),
        "moves": moves,
        "caveat": "This learnset is from PokeAPI version-group data. Verify Pokemon Champions move availability from official Champions/HOME data before making legality claims.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Look up Pokemon, move, and learnset facts from PokeAPI.")
    sub = parser.add_subparsers(dest="command", required=True)

    pokemon_parser = sub.add_parser("pokemon", help="Fetch typing, base stats, and abilities.")
    pokemon_parser.add_argument("name")

    move_parser = sub.add_parser("move", help="Fetch move metadata.")
    move_parser.add_argument("name")

    learnset_parser = sub.add_parser("learnset", help="Fetch learnset entries.")
    learnset_parser.add_argument("name")
    learnset_parser.add_argument("--version-group", help="Filter, for example scarlet-violet.")

    args = parser.parse_args()
    if args.command == "pokemon":
        print(json.dumps(pokemon(args.name), indent=2, ensure_ascii=False))
    elif args.command == "move":
        print(json.dumps(move(args.name), indent=2, ensure_ascii=False))
    elif args.command == "learnset":
        print(json.dumps(learnset(args.name, args.version_group), indent=2, ensure_ascii=False))
    else:
        parser.error("unknown command")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
