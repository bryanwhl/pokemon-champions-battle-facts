---
name: pokemon-champions-battle-facts
description: Verify factual Pokemon Champions and VGC battle claims before analysis. Use when researching Pokemon Champions, VGC, type matchups, Pokemon typings, base stats, abilities, moves, learnsets, legality, speed tiers, damage calculations, or matchup planning, especially when an answer could hallucinate battle mechanics or current rules.
license: MIT
---

# Pokemon Champions Battle Facts

Use this skill to ground Pokemon Champions and VGC research in checkable facts before making strategic claims. Do not rely on memory for typing, stats, move data, legality, or damage ranges when a bundled script or primary source can verify it.

## Fact Workflow

1. Classify each claim before analysis:
   - **Stable mechanics**: type chart, combined defensive typing, standard stat formula, standard level-50 damage formula.
   - **Canonical Pokemon data**: Pokemon species/form typings, base stats, abilities, move metadata, learnsets in known main-series version groups.
   - **Champions-current data**: legal roster, current regulation, in-game move availability, usage, items, and rule changes.
2. Verify stable mechanics with `scripts/type_matchup.py` or `references/type-chart.md`.
3. Verify Pokemon data with `scripts/pokeapi_lookup.py` or an official/user-provided source. Treat PokeAPI and Pokemon Showdown data as canonical-mainline references, not proof of current Champions legality.
4. Verify Champions-current data from official Pokemon Champions, Pokemon HOME Battle Data, official Play! Pokemon rules, or user-provided exports/screenshots. If those are unavailable, say the claim is unverified instead of filling the gap.
5. Use `scripts/damage_calc.mjs` for damage ranges when Node dependencies are installed. Otherwise use `references/damage-calculation.md` to compute and show assumptions.
6. Cite or name the source/tool used for every factual claim that affects strategic advice.

## Quick Commands

Use lowercase type names. Pokemon and move names may use spaces or hyphens.

```bash
python scripts/type_matchup.py --attack fire --defend grass steel
python scripts/type_matchup.py --defense-types dragon flying
python scripts/type_matchup.py --matrix markdown
python scripts/pokeapi_lookup.py pokemon incineroar
python scripts/pokeapi_lookup.py learnset incineroar --version-group scarlet-violet
python scripts/pokeapi_lookup.py move fake-out
npm install
node scripts/damage_calc.mjs examples/damage-request.json
```

## Answering Rules

- Never call a matchup "super effective", "resisted", or "immune" without checking the type chart when the claim matters.
- Never assume a Pokemon's Champions legality or Champions learnset from older games. Pokemon HOME can preserve different move sets by game, and moves may change when moved to software where they are unavailable.
- Distinguish a Pokemon's species/form data from a battle set. For example, "Flutter Mane has base 135 Speed" is data; "Flutter Mane is Booster Energy Timid" is a set assumption.
- State generation, level, format, terrain/weather/screens, items, abilities, EVs, IVs, nature, spread target, and doubles modifiers before trusting a damage calculation.
- For live metagame claims, prefer official in-game Battle Data or Pokemon HOME Battle Data. Fan usage sites can inspire hypotheses but must be labeled as non-official unless independently verified.

## References

- `references/type-chart.md`: text-form 18-type matchup matrix and combined-defense notes.
- `references/source-policy.md`: source hierarchy and how to avoid hallucinating Champions-current facts.
- `references/damage-calculation.md`: damage formula assumptions and common VGC modifiers.
- `references/data-sources.md`: API/tool notes for PokeAPI, Pokemon Showdown, and official Pokemon sources.
