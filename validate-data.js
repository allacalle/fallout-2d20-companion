#!/usr/bin/env node
/**
 * validate-data.js
 * Validates all JSON data files for integrity:
 * - No duplicate IDs within each file
 * - All referenced IDs exist in their target files
 * - Required fields are present
 * - Cross-file references are valid
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');

// Load all JSON files
function loadJSON(filename) {
  const filepath = path.join(DATA_DIR, filename);
  if (!fs.existsSync(filepath)) {
    console.warn(`⚠️  File not found: ${filename}`);
    return null;
  }
  const content = fs.readFileSync(filepath, 'utf8');
  try {
    return JSON.parse(content);
  } catch (e) {
    console.error(`❌ Invalid JSON in ${filename}: ${e.message}`);
    process.exit(1);
  }
}

// Collect all errors and warnings
const errors = [];
const warnings = [];

function error(msg) {
  errors.push(msg);
  console.error(`❌ ${msg}`);
}

function warn(msg) {
  warnings.push(msg);
  console.warn(`⚠️  ${msg}`);
}

function info(msg) {
  console.log(`ℹ️  ${msg}`);
}

// Load all data files
const files = {
  skills: loadJSON('skills.json'),
  perks: loadJSON('perks.json'),
  calibers: loadJSON('calibers.json'),
  weapons: loadJSON('weapons.json'),
  mods: loadJSON('mods.json'),
  armor: loadJSON('armor.json'),
  armorSets: loadJSON('armor-sets.json'),
  armorMods: loadJSON('armor-mods.json'),
  clothing: loadJSON('clothing.json'),
  outfits: loadJSON('outfits.json'),
  consumables: loadJSON('consumables.json'),
  components: loadJSON('components.json'),
  effects: loadJSON('effects.json'),
  workbenches: loadJSON('crafting/workbenches.json'),
  chemRecipes: loadJSON('crafting/chem-recipes.json'),
  cookingRecipes: loadJSON('crafting/cooking-recipes.json'),
  paRecipes: loadJSON('crafting/power-armor-recipes.json'),
};

// Build ID lookup maps
function buildIdMap(data, filename) {
  if (!data) return new Map();
  const map = new Map();
  for (const item of data) {
    if (!item.id) {
      error(`${filename}: Item missing id field: ${JSON.stringify(item).slice(0, 100)}`);
      continue;
    }
    if (map.has(item.id)) {
      error(`${filename}: Duplicate id "${item.id}"`);
    }
    map.set(item.id, item);
  }
  return map;
}

const idMaps = {
  skills: buildIdMap(files.skills, 'skills.json'),
  perks: buildIdMap(files.perks, 'perks.json'),
  calibers: buildIdMap(files.calibers, 'calibers.json'),
  weapons: buildIdMap(files.weapons, 'weapons.json'),
  mods: buildIdMap(files.mods, 'mods.json'),
  armor: buildIdMap(files.armor, 'armor.json'),
  armorSets: buildIdMap(files.armorSets, 'armor-sets.json'),
  armorMods: buildIdMap(files.armorMods, 'armor-mods.json'),
  clothing: buildIdMap(files.clothing, 'clothing.json'),
  outfits: buildIdMap(files.outfits, 'outfits.json'),
  consumables: buildIdMap(files.consumables, 'consumables.json'),
  components: files.components?.tiers ? buildIdMap(files.components.tiers, 'components.json') : new Map(),
  workbenches: buildIdMap(files.workbenches, 'workbenches.json'),
  chemRecipes: buildIdMap(files.chemRecipes, 'chem-recipes.json'),
  cookingRecipes: buildIdMap(files.cookingRecipes, 'cooking-recipes.json'),
  paRecipes: buildIdMap(files.paRecipes, 'power-armor-recipes.json'),
};

// Check required fields
function checkRequiredFields(data, filename, requiredFields) {
  if (!data) return;
  for (const item of data) {
    for (const field of requiredFields) {
      if (item[field] === undefined || item[field] === null) {
        error(`${filename}: Item "${item.id || 'unknown'}" missing required field "${field}"`);
      }
    }
  }
}

// Check reference exists
function checkRef(refId, targetMap, sourceFile, sourceId, fieldName) {
  if (!refId) return;
  if (!targetMap.has(refId)) {
    error(`${sourceFile}: "${sourceId}" references non-existent ${fieldName} "${refId}"`);
  }
}

// Validate skills
info('Validating skills.json...');
checkRequiredFields(files.skills, 'skills.json', ['id', 'name', 'attribute', 'description']);
for (const skill of files.skills || []) {
  if (!['STR', 'PER', 'END', 'CHA', 'INT', 'AGI', 'LCK'].includes(skill.attribute)) {
    error(`skills.json: "${skill.id}" has invalid attribute "${skill.attribute}"`);
  }
}

// Validate perks
info('Validating perks.json...');
checkRequiredFields(files.perks, 'perks.json', ['id', 'name', 'ranks', 'requirements', 'effects']);

// Validate calibers
info('Validating calibers.json...');
checkRequiredFields(files.calibers, 'calibers.json', ['id', 'name', 'quantityFound', 'weight', 'cost', 'rarity']);

// Validate weapons
info('Validating weapons.json...');
checkRequiredFields(files.weapons, 'weapons.json', ['id', 'name', 'weaponType', 'skillId', 'damage', 'damageType', 'weight', 'cost', 'rarity']);
for (const weapon of files.weapons || []) {
  // Check skill reference
  checkRef(weapon.skillId, idMaps.skills, 'weapons.json', weapon.id, 'skillId');

  // Check ammo reference
  if (weapon.ammo) {
    checkRef(weapon.ammo, idMaps.calibers, 'weapons.json', weapon.id, 'ammo');
  }

  // Check mod references in parts
  if (weapon.parts) {
    for (const [partType, modIds] of Object.entries(weapon.parts)) {
      for (const modId of modIds) {
        checkRef(modId, idMaps.mods, 'weapons.json', weapon.id, `parts.${partType}`);
      }
    }
  }

  // Check weapon type
  const validWeaponTypes = ['small_guns', 'energy_weapons', 'big_guns', 'melee_weapons', 'throwing', 'unarmed', 'explosives'];
  if (!validWeaponTypes.includes(weapon.weaponType)) {
    error(`weapons.json: "${weapon.id}" has invalid weaponType "${weapon.weaponType}"`);
  }

  // Check damage type
  const validDamageTypes = ['Physical', 'Energy', 'Radiation', 'Poison', 'Physical/Energy'];
  if (!validDamageTypes.includes(weapon.damageType)) {
    error(`weapons.json: "${weapon.id}" has invalid damageType "${weapon.damageType}"`);
  }
}

// Validate effects reference data
info('Validating effects.json...');
if (files.effects) {
  if (!files.effects.damageEffects) error('effects.json: Missing damageEffects section');
  if (!files.effects.qualities) error('effects.json: Missing qualities section');
  if (!files.effects.damageTypes) error('effects.json: Missing damageTypes section');
  if (!files.effects.ranges) error('effects.json: Missing ranges section');
  if (!files.effects.bodyLocations) error('effects.json: Missing bodyLocations section');

  // Check that all damageEffects referenced in weapons exist
  const knownEffects = new Set(Object.keys(files.effects.damageEffects || {}));
  const knownQualities = new Set(Object.keys(files.effects.qualities || {}));
  const knownDamageTypes = new Set(Object.keys(files.effects.damageTypes || {}));
  const knownRanges = new Set(Object.keys(files.effects.ranges || {}));

  for (const weapon of files.weapons || []) {
    // Check damage effects
    for (const effect of weapon.damageEffects || []) {
      // Effects can be "Piercing 1", "Piercing 2", etc. - check base name
      const baseEffect = effect.replace(/\d+$/, '').trim();
      if (!knownEffects.has(effect) && !knownEffects.has(baseEffect)) {
        warn(`weapons.json: "${weapon.id}" references unknown damageEffect "${effect}"`);
      }
    }

    // Check qualities
    for (const quality of weapon.qualities || []) {
      if (!knownQualities.has(quality)) {
        warn(`weapons.json: "${weapon.id}" references unknown quality "${quality}"`);
      }
    }

    // Check damage type
    if (!knownDamageTypes.has(weapon.damageType)) {
      warn(`weapons.json: "${weapon.id}" has unknown damageType "${weapon.damageType}"`);
    }

    // Check range
    if (weapon.range && !knownRanges.has(weapon.range)) {
      warn(`weapons.json: "${weapon.id}" has unknown range "${weapon.range}"`);
    }
  }
}

// Validate mods
info('Validating mods.json...');
checkRequiredFields(files.mods, 'mods.json', ['id', 'name', 'partType', 'weaponTypes', 'effects', 'weightChange', 'costChange', 'skill', 'complexity', 'rarity']);
for (const mod of files.mods || []) {
  // Check perk references
  for (const perkRef of mod.perksRequired || []) {
    checkRef(perkRef.perkId, idMaps.perks, 'mods.json', mod.id, `perksRequired[${perkRef.perkId}]`);
  }

  // Check skill reference
  checkRef(mod.skill, idMaps.skills, 'mods.json', mod.id, 'skill');

  // Check weapon types
  const validWeaponTypes = ['small_guns', 'energy_weapons', 'big_guns', 'melee_weapons'];
  for (const wt of mod.weaponTypes) {
    if (!validWeaponTypes.includes(wt)) {
      error(`mods.json: "${mod.id}" has invalid weaponType "${wt}"`);
    }
  }
}

// Print summary
console.log('\n' + '='.repeat(50));
console.log('VALIDATION SUMMARY');
console.log('='.repeat(50));

const fileCounts = Object.entries(files)
  .filter(([_, data]) => data !== null)
  .map(([name, data]) => {
    if (name === 'components' && data?.tiers) {
      return `${name}: ${data.tiers.length} tiers`;
    }
    return `${name}: ${data.length} items`;
  })
  .join(', ');

console.log(`Files loaded: ${fileCounts}`);
console.log(`Errors: ${errors.length}`);
console.log(`Warnings: ${warnings.length}`);

if (errors.length === 0) {
  console.log('\n✅ All data files are valid!');
} else {
  console.log(`\n❌ ${errors.length} error(s) found. Fix these before proceeding.`);
  process.exit(1);
}
