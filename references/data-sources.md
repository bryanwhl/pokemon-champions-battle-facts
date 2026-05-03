# Data Sources

## Official Pokemon

- Pokemon Champions site: `https://champions.pokemon.com/`
- Pokemon Support says Pokemon HOME Battle Data shows online competition rankings and Pokemon rankings with moves, Abilities, and items in the mobile app.
- Pokemon Support says a Pokemon's moves can differ by linked game, and moves may be replaced when moved to software where they are unavailable.

Use these sources for Champions-current facts when available. If a web page is blocked or stale, ask for a screenshot/export from the game or Pokemon HOME rather than guessing.

## PokeAPI

Use `scripts/pokeapi_lookup.py` for:

- Species/form typing.
- Base stats.
- Ability slots.
- Move metadata.
- Version-group learnsets.

PokeAPI does not prove Pokemon Champions legality. Its version-group learnsets are still useful for checking a claim like "Incineroar is Fire/Dark" or "Fake Out is a Normal physical move with +3 priority."

## Pokemon Showdown / Smogon Calculator

Use `scripts/damage_calc.mjs` after `npm install` for standard damage ranges. It delegates to `@smogon/calc`, which is the programmatic package behind the community-standard Pokemon Showdown damage calculator.

Showdown data is excellent for mechanical calculations, but it may lead or lag official Champions changes. Always label the generation and calculator assumptions.
