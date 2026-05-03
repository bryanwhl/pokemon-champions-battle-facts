# pokemon-champions-battle-facts

An [agentskills.io](https://agentskills.io) skill that helps AI agents verify
Pokemon Champions and Pokemon VGC battle facts before doing matchup analysis,
team analysis, damage calculations, or metagame research.

This skill exists because general-purpose AI agents often hallucinate basic
Pokemon battle facts: type matchups, dual-type effectiveness, base stats,
move properties, learnsets, legality, and damage ranges. The goal is to make
agents compute or fetch battle facts instead of guessing from memory.

---

## Capabilities

- **Type Matchups** with a complete text-form 18-type chart.
- **Dual-Type Defensive Calculations** such as Fire into Grass/Steel = 4x.
- **Incoming Weakness Tables** for any one- or two-type defensive profile.
- **Pokemon Data Lookup** using PokeAPI for typings, base stats, abilities,
  height, weight, and form-specific Pokemon entries.
- **Move Data Lookup** using PokeAPI for type, category, power, accuracy,
  priority, target, PP, and short effect text.
- **Learnset Lookup** using PokeAPI version-group data, with explicit caveats
  that this does not prove Pokemon Champions legality.
- **Damage Calculation Wrapper** using `@smogon/calc` for standard Pokemon
  damage ranges under explicit generation, spread, field, item, ability,
  nature, EV, IV, and level assumptions.
- **Source Policy** for separating stable mechanics, canonical Pokemon data,
  and volatile Pokemon Champions-current facts.
- **Anti-Hallucination Workflow** that instructs agents to cite or name the
  tool/source behind factual claims that affect strategy.

---

## Requirements

The core skill works as plain text instructions and reference files. The
bundled scripts require:

- **Python** 3.10+ for type matchup and PokeAPI lookup scripts.
- **Node.js** 18+ for the optional Smogon damage calculator wrapper.
- **npm** for installing `@smogon/calc`.
- Internet access for live PokeAPI lookups.

### Verify Requirements

```bash
python --version
node --version
npm --version
```

Install the optional Node dependency:

```bash
npm install
```

---

## Install the Skill

```bash
npx skills add pokemon-champions-battle-facts
```

Or clone directly:

```bash
git clone https://github.com/bryanwhl/pokemon-champions-battle-facts
cd pokemon-champions-battle-facts
npm install
```

The skill root is the repository root. The required Agent Skill entrypoint is
`SKILL.md`.

---

## Directory Structure

```text
pokemon-champions-battle-facts/
|-- SKILL.md                         # Agent skill definition and workflow
|-- README.md                        # This file
|-- LICENSE                          # MIT License
|-- package.json                     # Optional Node dependency for damage calc
|-- package-lock.json
|-- agents/
|   `-- openai.yaml                  # UI metadata for Agent Skills clients
|-- examples/
|   `-- damage-request.json          # Example @smogon/calc request
|-- scripts/
|   |-- type_matchup.py              # Type chart and dual-type calculations
|   |-- pokeapi_lookup.py            # Pokemon, move, and learnset lookup
|   `-- damage_calc.mjs              # @smogon/calc JSON wrapper
`-- references/
    |-- type-chart.md                # Full 18-type matchup matrix
    |-- source-policy.md             # Source hierarchy and disclaimers
    |-- damage-calculation.md        # Damage assumptions and modifiers
    `-- data-sources.md              # Official/API/community source notes
```

---

## Quick Start

### Check a Type Matchup

```bash
python scripts/type_matchup.py --attack fire --defend grass steel
```

Output:

```json
{
  "attack": "fire",
  "defend": ["grass", "steel"],
  "multiplier": 4.0,
  "label": "double super effective (4x)"
}
```

### List All Incoming Matchups for a Defensive Typing

```bash
python scripts/type_matchup.py --defense-types dragon flying
```

Use this before saying a Pokemon is weak to, resists, or is immune to a move
type.

### Print the Full Type Matrix

```bash
python scripts/type_matchup.py --matrix markdown
python scripts/type_matchup.py --matrix json
```

### Look Up Pokemon Data

```bash
python scripts/pokeapi_lookup.py pokemon incineroar
```

This returns PokeAPI-backed typing, base stats, abilities, and source metadata.

### Look Up Move Data

```bash
python scripts/pokeapi_lookup.py move fake-out
```

This returns move type, category, power, accuracy, PP, priority, target, effect
chance, and effect text.

### Look Up Learnsets by Version Group

```bash
python scripts/pokeapi_lookup.py learnset incineroar --version-group scarlet-violet
```

Important: PokeAPI learnsets are canonical data references, not Pokemon
Champions legality proof.

### Run a Damage Calculation

```bash
npm install
node scripts/damage_calc.mjs examples/damage-request.json
```

The damage wrapper returns damage rolls, percent range, assumptions, and a
human-readable `@smogon/calc` description.

---

## Script Reference

### `scripts/type_matchup.py`

```text
Usage:
  python scripts/type_matchup.py --attack <type> --defend <type> [type]
  python scripts/type_matchup.py --defense-types <type> [type]
  python scripts/type_matchup.py --matrix json
  python scripts/type_matchup.py --matrix markdown

Examples:
  python scripts/type_matchup.py --attack electric --defend water flying
  python scripts/type_matchup.py --attack electric --defend water ground
  python scripts/type_matchup.py --defense-types fire dark
```

### `scripts/pokeapi_lookup.py`

```text
Usage:
  python scripts/pokeapi_lookup.py pokemon <pokemon-name>
  python scripts/pokeapi_lookup.py move <move-name>
  python scripts/pokeapi_lookup.py learnset <pokemon-name> [--version-group <group>]

Examples:
  python scripts/pokeapi_lookup.py pokemon flutter-mane
  python scripts/pokeapi_lookup.py pokemon rotom-wash
  python scripts/pokeapi_lookup.py move protect
  python scripts/pokeapi_lookup.py learnset rillaboom --version-group scarlet-violet
```

### `scripts/damage_calc.mjs`

```text
Usage:
  node scripts/damage_calc.mjs <request.json>

Example:
  node scripts/damage_calc.mjs examples/damage-request.json
```

The JSON request should include:

- `gen`
- `attacker.species`
- `attacker.level`
- `attacker.ability`
- `attacker.item`
- `attacker.nature`
- `attacker.evs`
- `attacker.ivs`
- `defender` with the same relevant fields
- `move.name`
- `field.gameType`, usually `Doubles` for VGC-style calculations

---

## Reference Documents

| File | Contents |
|------|----------|
| `references/type-chart.md` | Full 18-type attack-by-defense matrix in text form |
| `references/source-policy.md` | Source hierarchy and required wording for uncertain claims |
| `references/damage-calculation.md` | Standard damage formula, assumptions, and common VGC modifiers |
| `references/data-sources.md` | Official Pokemon, PokeAPI, Pokemon Showdown, and Smogon calculator notes |

---

## How Agents Should Use This Skill

Agents should use this skill before making factual claims such as:

- "This move is super effective into that Pokemon."
- "This Pokemon is weak to Ground."
- "This Pokemon has base 135 Speed."
- "This Pokemon learns Fake Out."
- "This attack is an OHKO."
- "This Pokemon is legal in Pokemon Champions."
- "This item/move/set is common in the current metagame."

The intended workflow is:

1. Verify stable mechanics with `type_matchup.py` or `references/type-chart.md`.
2. Verify Pokemon and move data with `pokeapi_lookup.py` or an official source.
3. Verify damage claims with `damage_calc.mjs` and explicit assumptions.
4. Verify Pokemon Champions-current legality and usage from official Pokemon
   Champions, Pokemon HOME Battle Data, official Play! Pokemon rules, or
   user-provided game evidence.
5. Say when something is unverified instead of filling the gap with a guess.

---

## Important Disclaimers

### Pokemon Champions Is Current-Date Sensitive

Pokemon Champions legality, available Pokemon, available moves, item legality,
rulesets, patches, and metagame usage can change. This skill does not bundle a
live Pokemon Champions legality database. It instructs agents to verify those
facts from official or user-provided current sources.

### PokeAPI Is Not Champions Legality

PokeAPI is useful for canonical Pokemon data such as typings, base stats,
abilities, move metadata, and version-group learnsets. It does not prove that a
Pokemon, move, item, or set is currently legal in Pokemon Champions.

### Smogon Calculator Is Not an Official Pokemon Champions Ruling

`@smogon/calc` is a high-quality community-standard calculator for Pokemon
damage mechanics. Calculator output should be labeled with generation and
assumptions. If Pokemon Champions changes a mechanic, official Champions data
or patch notes take priority.

### Community Data Needs Labels

Community usage stats, rental teams, social posts, and fan resources can be
helpful for hypotheses. They should not be presented as official facts unless
cross-checked against official sources.

### Trademark Notice

Pokemon, Pokemon Champions, Pokemon HOME, and related names are trademarks of
Nintendo, Creatures Inc., GAME FREAK inc., and/or The Pokemon Company. This
repository is an unofficial fan-made Agent Skill and is not affiliated with,
endorsed by, or sponsored by Nintendo, Creatures Inc., GAME FREAK inc., or The
Pokemon Company.

---

## License

MIT - see [LICENSE](./LICENSE)
