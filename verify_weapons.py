#!/usr/bin/env python3
"""Verify weapons.json against PDF manual data."""

import json

with open("data/weapons.json") as f:
    weapons = json.load(f)

weapons_by_name = {w["name"]: w for w in weapons}

# Manually extracted from PDF tables (pages 95-114)
# Format: {name: {field: value}}
# Fields: damageRating, damageEffects, damageType, fireRate, range, qualities, weight, cost, rarity, ammo

pdf_data = {
    # === SMALL GUNS (pages 95-98) ===
    ".44 Pistol": {
        "damage": "6", "damageEffects": ["Vicious"], "damageType": "Physical",
        "fireRate": 1, "range": "close", "qualities": ["Close Quarters"],
        "ammo": ".44 Magnum", "weight": 4, "cost": 99, "rarity": 2,
        "description": "double-action revolver, chambered to use the .44 Magnum cartridge"
    },
    "10mm Pistol": {
        "damage": "4", "damageEffects": [], "damageType": "Physical",
        "fireRate": 2, "range": "close", "qualities": ["Close Quarters", "Reliable"],
        "ammo": "10mm", "weight": 4, "cost": 50, "rarity": 1,
        "description": "Small, dependable, reasonably powerful"
    },
    "Flare Gun": {
        "damage": "3", "damageEffects": [], "damageType": "Physical",
        "fireRate": 0, "range": "medium", "qualities": ["Reliable"],
        "ammo": "Flare", "weight": 2, "cost": 50, "rarity": 1,
        "description": "simple, single-shot weapon"
    },
    "Assault Rifle": {
        "damage": "5", "damageEffects": ["Burst"], "damageType": "Physical",
        "fireRate": 2, "range": "medium", "qualities": ["Two-Handed"],
        "ammo": "5.56mm", "weight": 13, "cost": 144, "rarity": 2,
        "description": "gas-operated rifle"
    },
    "Combat Rifle": {
        "damage": "5", "damageEffects": [], "damageType": "Physical",
        "fireRate": 2, "range": "medium", "qualities": ["Two-Handed"],
        "ammo": ".45", "weight": 11, "cost": 117, "rarity": 2,
        "description": "rugged and adaptable design"
    },
    "Gauss Rifle": {
        "damage": "10", "damageEffects": ["Piercing 1"], "damageType": "Physical",
        "fireRate": 1, "range": "long", "qualities": ["Two-Handed"],
        "ammo": "2mm EC", "weight": 16, "cost": 228, "rarity": 4,
        "description": "magnetic induction to propel a projectile"
    },
    "Hunting Rifle": {
        "damage": "6", "damageEffects": ["Piercing 1"], "damageType": "Physical",
        "fireRate": 0, "range": "medium", "qualities": ["Two-Handed"],
        "ammo": ".308", "weight": 10, "cost": 55, "rarity": 2,
        "description": "bolt-action rifle"
    },
    "Submachine Gun": {
        "damage": "3", "damageEffects": ["Burst"], "damageType": "Physical",
        "fireRate": 3, "range": "close", "qualities": ["Inaccurate", "Two-Handed"],
        "ammo": ".45", "weight": 12, "cost": 109, "rarity": 1,
        "description": "hideously inaccurate, their rate-of-fire means you don't need to be accurate"
    },
    "Combat Shotgun": {
        "damage": "5", "damageEffects": ["Spread"], "damageType": "Physical",
        "fireRate": 2, "range": "close", "qualities": ["Inaccurate", "Two-Handed"], # Note: PDF says Inaccurate, not Close Quarters + Reliable
        "ammo": "Shotgun Shell", "weight": 11, "cost": 87, "rarity": 2,
        "description": "combat shotgun description"
    },
    "Double-Barrel Shotgun": {
        "damage": "5", "damageEffects": ["Spread", "Vicious"], "damageType": "Physical",
        "fireRate": 0, "range": "close", "qualities": ["Inaccurate", "Two-Handed"],
        "ammo": "Shotgun Shell", "weight": 9, "cost": 39, "rarity": 1,
        "description": ""
    },
    "Pipe Bolt-Action": {
        "damage": "5", "damageEffects": ["Piercing 1"], "damageType": "Physical",
        "fireRate": 0, "range": "close", "qualities": ["Unreliable"],
        "ammo": ".308", "weight": 3, "cost": 30, "rarity": 0,
        "description": ""
    },
    "Pipe Gun": {
        "damage": "3", "damageEffects": [], "damageType": "Physical",
        "fireRate": 2, "range": "close", "qualities": ["Close Quarters", "Unreliable"],
        "ammo": ".38", "weight": 2, "cost": 30, "rarity": 0,
        "description": ""
    },
    "Pipe Revolver": {
        "damage": "4", "damageEffects": [], "damageType": "Physical",
        "fireRate": 1, "range": "close", "qualities": ["Close Quarters", "Unreliable"],
        "ammo": ".45", "weight": 4, "cost": 25, "rarity": 0,
        "description": ""
    },
    "Railway Rifle": {
        "damage": "10", "damageEffects": ["Breaking"], "damageType": "Physical",
        "fireRate": 0, "range": "medium", "qualities": ["Two-Handed", "Unreliable"],
        "ammo": "Railway Spikes", "weight": 14, "cost": 290, "rarity": 4,
        "description": ""
    },
    "Syringer": {
        "damage": "3", "damageEffects": [], "damageType": "Physical",
        "fireRate": 0, "range": "medium", "qualities": ["Two-Handed"],
        "ammo": "Syringe", "weight": 6, "cost": 132, "rarity": 2,
        "description": ""
    },
    # === ENERGY WEAPONS (page 101-104) ===
    "Institute Laser": {
        "damage": "3", "damageEffects": ["Burst"], "damageType": "Energy",
        "fireRate": 3, "range": "close", "qualities": ["Close Quarters", "Inaccurate"],
        "ammo": "Fusion Cells", "weight": 4, "cost": 50, "rarity": 2,
        "description": "rapid succession of beams"
    },
    "Laser Musket": {
        "damage": "5", "damageEffects": ["Piercing 1"], "damageType": "Energy",
        "fireRate": 0, "range": "medium", "qualities": ["Two-Handed"],
        "ammo": "Fusion Cells", "weight": 13, "cost": 57, "rarity": 1,
        "description": "homemade form of laser rifle"
    },
    "Laser Gun": {
        "damage": "4", "damageEffects": ["Piercing 1"], "damageType": "Energy",
        "fireRate": 2, "range": "close", "qualities": ["Close Quarters"],
        "ammo": "Fusion Cells", "weight": 4, "cost": 69, "rarity": 2,
        "description": ""
    },
    "Plasma Gun": {
        "damage": "6", "damageEffects": [], "damageType": "Physical/Energy",
        "fireRate": 1, "range": "close", "qualities": ["Close Quarters"],
        "ammo": "Plasma Cartridge", "weight": 4, "cost": 123, "rarity": 3,
        "description": ""
    },
    "Gamma Gun": {
        "damage": "3", "damageEffects": ["Piercing 1", "Blast", "Stun"], "damageType": "Radiation",
        "fireRate": 1, "range": "medium", "qualities": ["Inaccurate"],
        "ammo": "Gamma Cartridge", "weight": 3, "cost": 156, "rarity": 5,
        "description": ""
    },
}

# === BIG GUNS (pages 107-109) ===
pdf_data.update({
    "Fat Man": {
        "damage": "21", "damageEffects": ["Breaking", "Blast", "Radioactive", "Vicious"],
        "damageType": "Physical", "fireRate": 0, "range": "medium",
        "qualities": ["Inaccurate", "Two-Handed"], "ammo": "Mini-Nuke",
        "weight": 31, "cost": 512, "rarity": 4,
        "description": "M42 Nuclear Catapult"
    },
    "Flamer": {
        "damage": "3", "damageEffects": ["Burst", "Debilitating", "Persistent", "Spread"],
        "damageType": "Energy", "fireRate": 4, "range": "close",
        "qualities": ["Inaccurate", "Two-Handed"], "ammo": "Flamer Fuel",
        "weight": 16, "cost": 137, "rarity": 3,
        "description": "sprays an ignited fuel mixture"
    },
    "Gatling Laser": {
        "damage": "3", "damageEffects": ["Gatling", "Burst", "Piercing 1"],
        "damageType": "Energy", "fireRate": 6, "range": "medium",
        "qualities": ["Inaccurate", "Two-Handed"], "ammo": "Fusion Cells",
        "weight": 19, "cost": 804, "rarity": 3,
        "description": "several rotating barrels"
    },
    "Heavy Incinerator": {
        "damage": "5", "damageEffects": ["Burst", "Debilitating", "Persistent", "Spread"],
        "damageType": "Energy", "fireRate": 3, "range": "medium",
        "qualities": ["Two-Handed"], "ammo": "Flamer Fuel",
        "weight": 20, "cost": 350, "rarity": 4,
        "description": ""
    },
    "Junk Jet": {
        "damage": "6", "damageEffects": [],
        "damageType": "Physical", "fireRate": 1, "range": "medium",
        "qualities": ["Two-Handed"], "ammo": "Junk",
        "weight": 30, "cost": 285, "rarity": 3,
        "description": ""
    },
    "Minigun": {
        "damage": "3", "damageEffects": ["Gatling", "Burst", "Spread"],
        "damageType": "Physical", "fireRate": 5, "range": "medium",
        "qualities": ["Inaccurate", "Two-Handed"], "ammo": "5.56mm",
        "weight": 27, "cost": 382, "rarity": 2,
        "description": ""
    },
    "Missile Launcher": {
        "damage": "11", "damageEffects": ["Blast"],
        "damageType": "Physical", "fireRate": 0, "range": "long",
        "qualities": ["Two-Handed"], "ammo": "Missile",
        "weight": 21, "cost": 314, "rarity": 4,
        "description": ""
    },
})

# === MELEE WEAPONS (pages 111-114) ===
pdf_data.update({
    "Unarmed Strike": {"damage": "2", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 0, "cost": 0, "rarity": 0, "ammo": None, "description": ""},
    "Handy Rock": {"damage": "2", "damageEffects": ["Vicious"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Thrown (C)"], "weight": 1, "cost": 0, "rarity": 0, "ammo": None, "description": ""},
    "Gun Bash (1H)": {"damage": "2", "damageEffects": ["Stun"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 0, "cost": 0, "rarity": 0, "ammo": None, "description": ""},
    "Gun Bash": {"damage": "3", "damageEffects": ["Stun"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 0, "cost": 0, "rarity": 0, "ammo": None, "description": ""},
    "Sword": {"damage": "4", "damageEffects": ["Piercing 1"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Parry"], "weight": 3, "cost": 50, "rarity": 2, "ammo": None, "description": "status and prestige amongst soldiers"},
    "Combat Knife": {"damage": "3", "damageEffects": ["Piercing 1"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 1, "cost": 25, "rarity": 1, "ammo": None, "description": ""},
    "Machete": {"damage": "3", "damageEffects": ["Piercing 1"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 2, "cost": 25, "rarity": 1, "ammo": None, "description": ""},
    "Ripper": {"damage": "4", "damageEffects": ["Vicious"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 6, "cost": 50, "rarity": 2, "ammo": None, "description": ""},
    "Shishkebab": {"damage": "5", "damageEffects": ["Piercing 1"], "damageType": "Energy", "fireRate": None, "range": None, "qualities": ["Parry"], "weight": 3, "cost": 200, "rarity": 3, "ammo": None, "description": ""},
    "Switchblade": {"damage": "2", "damageEffects": ["Piercing 1"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Concealed"], "weight": 1, "cost": 20, "rarity": 0, "ammo": None, "description": ""},
    "Baseball Bat": {"damage": "4", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Two-Handed"], "weight": 3, "cost": 25, "rarity": 1, "ammo": None, "description": ""},
    "Aluminum Baseball Bat": {"damage": "5", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Two-Handed"], "weight": 2, "cost": 32, "rarity": 2, "ammo": None, "description": ""},
    "Board": {"damage": "4", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Two-Handed"], "weight": 3, "cost": 20, "rarity": 0, "ammo": None, "description": ""},
    "Lead Pipe": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 3, "cost": 15, "rarity": 0, "ammo": None, "description": ""},
    "Pipe Wrench": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 2, "cost": 30, "rarity": 1, "ammo": None, "description": ""},
    "Pool Cue": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Two-Handed"], "weight": 1, "cost": 10, "rarity": 0, "ammo": None, "description": ""},
    "Rolling Pin": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 1, "cost": 10, "rarity": 0, "ammo": None, "description": ""},
    "Baton": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 2, "cost": 15, "rarity": 1, "ammo": None, "description": ""},
    "Sledgehammer": {"damage": "5", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Two-Handed"], "weight": 12, "cost": 40, "rarity": 2, "ammo": None, "description": ""},
    "Super Sledge": {"damage": "6", "damageEffects": ["Breaking"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Two-Handed"], "weight": 20, "cost": 180, "rarity": 3, "ammo": None, "description": ""},
    "Tire Iron": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 2, "cost": 25, "rarity": 1, "ammo": None, "description": ""},
    "Walking Cane": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 2, "cost": 10, "rarity": 0, "ammo": None, "description": ""},
    "Boxing Glove": {"damage": "3", "damageEffects": ["Stun"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 1, "cost": 10, "rarity": 1, "ammo": None, "description": ""},
    "Deathclaw Gauntlet": {"damage": "5", "damageEffects": ["Piercing 1"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 10, "cost": 75, "rarity": 3, "ammo": None, "description": ""},
    "Knuckles": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": None, "qualities": ["Concealed"], "weight": 0, "cost": 10, "rarity": 1, "ammo": None, "description": ""},
    "Power Fist": {"damage": "4", "damageEffects": ["Stun"], "damageType": "Physical", "fireRate": None, "range": None, "qualities": [], "weight": 4, "cost": 100, "rarity": 2, "ammo": None, "description": ""},
})

# === THROWING WEAPONS ===
pdf_data.update({
    "Throwing Knives": {"damage": "2", "damageEffects": ["Piercing 1"], "damageType": "Physical", "fireRate": None, "range": "close", "qualities": ["Thrown"], "weight": 0, "cost": 30, "rarity": 2, "ammo": None, "description": ""},
    "Tomahawk": {"damage": "3", "damageEffects": [], "damageType": "Physical", "fireRate": None, "range": "close", "qualities": ["Thrown"], "weight": 0, "cost": 35, "rarity": 2, "ammo": None, "description": ""},
    "Javelin": {"damage": "5", "damageEffects": ["Piercing 1"], "damageType": "Physical", "fireRate": None, "range": "close", "qualities": ["Thrown", "Two-Handed"], "weight": 2, "cost": 25, "rarity": 2, "ammo": None, "description": ""},
})

# === EXPLOSIVES ===
pdf_data.update({
    "Baseball Grenade": {"damage": "5", "damageEffects": ["Blast"], "damageType": "Physical", "fireRate": None, "range": "close", "qualities": ["Thrown (C)", "Fragmenting", "Blast"], "weight": 1, "cost": 15, "rarity": 1, "ammo": None, "description": ""},
    "Frag Grenade": {"damage": "6", "damageEffects": ["Blast", "Piercing 1"], "damageType": "Physical", "fireRate": None, "range": "close", "qualities": ["Thrown (C)", "Fragmenting", "Blast"], "weight": 0, "cost": 40, "rarity": 1, "ammo": None, "description": ""},
    "Molotov Cocktail": {"damage": "4", "damageEffects": ["Blast", "Persistent", "Spread"], "damageType": "Energy", "fireRate": None, "range": "close", "qualities": ["Thrown (C)", "Blast"], "weight": 1, "cost": 5, "rarity": 0, "ammo": None, "description": ""},
    "Nuka Grenade": {"damage": "12", "damageEffects": ["Blast"], "damageType": "Physical/Energy/Radiation", "fireRate": None, "range": "close", "qualities": ["Thrown (C)", "Blast"], "weight": 2, "cost": 100, "rarity": 4, "ammo": None, "description": ""},
    "Plasma Grenade": {"damage": "8", "damageEffects": ["Blast", "Vicious"], "damageType": "Physical/Energy", "fireRate": None, "range": "close", "qualities": ["Thrown (C)", "Blast"], "weight": 0, "cost": 75, "rarity": 3, "ammo": None, "description": ""},
    "Pulse Grenade": {"damage": "6", "damageEffects": ["Blast", "Stun"], "damageType": "Energy", "fireRate": None, "range": "close", "qualities": ["Thrown (C)", "Blast"], "weight": 0, "cost": 100, "rarity": 3, "ammo": None, "description": ""},
    "Bottlecap Mine": {"damage": "10", "damageEffects": ["Blast", "Breaking", "Piercing 2"], "damageType": "Physical", "fireRate": None, "range": "close", "qualities": ["Mine", "Blast", "Fragmenting"], "weight": 1, "cost": 45, "rarity": 3, "ammo": None, "description": ""},
    "Frag Mine": {"damage": "6", "damageEffects": ["Blast", "Piercing 1"], "damageType": "Physical", "fireRate": None, "range": "close", "qualities": ["Mine", "Blast", "Fragmenting"], "weight": 1, "cost": 50, "rarity": 2, "ammo": None, "description": ""},
    "Nuke Mine": {"damage": "15", "damageEffects": ["Blast", "Breaking"], "damageType": "Physical/Radiation", "fireRate": None, "range": "close", "qualities": ["Mine", "Blast"], "weight": 5, "cost": 112, "rarity": 5, "ammo": None, "description": ""},
    "Plasma Mine": {"damage": "8", "damageEffects": ["Blast", "Vicious"], "damageType": "Physical/Energy", "fireRate": None, "range": "close", "qualities": ["Mine", "Blast"], "weight": 0, "cost": 113, "rarity": 4, "ammo": None, "description": ""},
    "Pulse Mine": {"damage": "6", "damageEffects": ["Blast", "Stun"], "damageType": "Energy", "fireRate": None, "range": "close", "qualities": ["Mine", "Blast"], "weight": 0, "cost": 150, "rarity": 4, "ammo": None, "description": ""},
})

# Compare
fields_to_check = [
    ("damage", "damage"),
    ("damageEffects", "damageEffects"),
    ("damageType", "damageType"),
    ("fireRate", "fireRate"),
    ("range", "range"),
    ("qualities", "qualities"),
    ("weight", "weight"),
    ("cost", "cost"),
    ("rarity", "rarity"),
]

discrepancies = []

for pdf_name, pdf_item in pdf_data.items():
    if pdf_name not in weapons_by_name:
        print(f"\n⚠  FALTA EN JSON: {pdf_name}")
        continue
    
    w = weapons_by_name[pdf_name]
    item_issues = []
    
    for json_field, pdf_field_name in fields_to_check:
        pdf_val = pdf_item[pdf_field_name]
        json_val = w.get(json_field)
        
        # Normalize for comparison
        if isinstance(json_val, list) and isinstance(pdf_val, list):
            # Remove duplicates and sort
            j_set = sorted(set(json_val))
            p_set = sorted(set(pdf_val))
            if j_set != p_set:
                item_issues.append(f"  {json_field}: JSON={j_set} vs PDF={p_set}")
        elif json_val != pdf_val:
            item_issues.append(f"  {json_field}: JSON={json_val} vs PDF={pdf_val}")
    
    if item_issues:
        discrepancies.append(f"\n❌ {pdf_name}:")
        discrepancies.extend(item_issues)

# Check for items in JSON but not in PDF
json_names = set(weapons_by_name.keys())
pdf_names = set(pdf_data.keys())
extra_in_json = json_names - pdf_names
if extra_in_json:
    discrepancies.append(f"\n⚠  EXTRA EN JSON (no en PDF): {sorted(extra_in_json)}")

print("\n" + "="*60)
print("DISCREPANCIAS DE ARMAS vs PDF OFICIAL")
print("="*60)
if discrepancies:
    for d in discrepancies:
        print(d)
    print(f"\nTotal: {len([d for d in discrepancies if d.startswith('❌')])} armas con errores")
else:
    print("✓ TODAS LAS ARMAS COINCIDEN CON EL PDF OFICIAL")
