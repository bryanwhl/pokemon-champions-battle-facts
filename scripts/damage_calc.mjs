#!/usr/bin/env node
import fs from "node:fs";
import {Generations, Pokemon, Move, Field, calculate} from "@smogon/calc";

const STAT_KEYS = ["hp", "atk", "def", "spa", "spd", "spe"];

function usage() {
  console.error("usage: node scripts/damage_calc.mjs <request.json>");
  process.exit(2);
}

function readRequest(path) {
  if (!path) usage();
  return JSON.parse(fs.readFileSync(path, "utf8"));
}

function normalizeStats(stats) {
  if (!stats) return undefined;
  const normalized = {};
  for (const key of STAT_KEYS) {
    if (stats[key] !== undefined) normalized[key] = Number(stats[key]);
  }
  return normalized;
}

function buildPokemon(gen, input) {
  const options = {
    level: input.level ?? 50,
    ability: input.ability,
    item: input.item,
    nature: input.nature,
    evs: normalizeStats(input.evs),
    ivs: normalizeStats(input.ivs),
    boosts: input.boosts,
    status: input.status,
    teraType: input.teraType,
  };
  return new Pokemon(gen, input.species, options);
}

function buildMove(gen, input) {
  if (typeof input === "string") return new Move(gen, input);
  return new Move(gen, input.name, {
    ability: input.ability,
    item: input.item,
    useZ: input.useZ,
    isCrit: input.isCrit,
    hits: input.hits,
  });
}

function buildField(input = {}) {
  return new Field({
    gameType: input.gameType ?? "Doubles",
    weather: input.weather,
    terrain: input.terrain,
    isGravity: input.isGravity,
    isMagicRoom: input.isMagicRoom,
    isWonderRoom: input.isWonderRoom,
    isAuraBreak: input.isAuraBreak,
    attackerSide: input.attackerSide,
    defenderSide: input.defenderSide,
  });
}

function main() {
  const request = readRequest(process.argv[2]);
  const gen = Generations.get(request.gen ?? 9);
  const attacker = buildPokemon(gen, request.attacker);
  const defender = buildPokemon(gen, request.defender);
  const move = buildMove(gen, request.move);
  const field = buildField(request.field);
  const result = calculate(gen, attacker, defender, move, field);
  const damage = Array.isArray(result.damage) ? result.damage.flat(Infinity) : [result.damage];
  const defenderHp = defender.maxHP();
  const percents = damage.map((value) => Number(((value / defenderHp) * 100).toFixed(1)));
  const output = {
    source: "@smogon/calc",
    caveat: "Verify Pokemon Champions-specific rule changes, legality, and move availability before treating this as an official Champions result.",
    gen: request.gen ?? 9,
    attacker: attacker.name,
    defender: defender.name,
    move: move.name,
    assumptions: {
      field: request.field ?? {},
      attacker: request.attacker,
      defender: request.defender,
    },
    damage,
    defenderHp,
    percentRange: [Math.min(...percents), Math.max(...percents)],
    description: result.desc?.() ?? String(result),
  };
  console.log(JSON.stringify(output, null, 2));
}

main();
