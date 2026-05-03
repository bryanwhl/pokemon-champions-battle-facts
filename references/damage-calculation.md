# Damage Calculation Notes

Prefer `scripts/damage_calc.mjs` when Node dependencies are installed. If calculating manually, show assumptions and use the standard Pokemon damage structure:

```text
base = floor(floor(floor((2 * level) / 5 + 2) * power * attack / defense) / 50) + 2
damage = floor(base * modifiers)
```

Important modifiers include targets spread-move reduction in doubles, weather, critical hits, random factor, STAB, type effectiveness, burn, screen effects, terrain, abilities, items, Helping Hand, Friend Guard, and move-specific rules.

For VGC:

- Default level is usually 50 unless a source says otherwise.
- Doubles spread moves commonly receive a 0.75 target modifier when hitting multiple Pokemon.
- The random factor is 85 through 100 percent in 16 integer rolls.
- STAB is normally 1.5x, or 2x with Adaptability, before game-specific mechanics such as Tera are considered.
- Type effectiveness multiplies across both defending types: 0x, 0.25x, 0.5x, 1x, 2x, or 4x.

Do not trust a damage range unless attacker stats, defender stats, move, item, ability, nature, EVs, IVs, level, field, weather, terrain, screens, side conditions, and relevant boosts are explicit.
