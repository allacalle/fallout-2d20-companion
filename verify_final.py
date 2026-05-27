#!/usr/bin/env python3
"""Final comprehensive verification of all game data against PDF manual."""

import json, re, os

DATA_DIR = "data"

def load_json(name):
    with open(os.path.join(DATA_DIR, name)) as f:
        return json.load(f)

def read_pdf(filename):
    with open(os.path.join("/tmp", filename)) as f:
        return f.read()

def normalize(n):
    if n is None: return ""
    return str(n).strip().lower().replace("'", "").replace("’", "").replace("-", " ").replace("_", " ").replace("(", "").replace(")", "").replace("  ", " ")

# ─── WEAPONS ──────────────────────────────────────

print("=" * 70)
print("FASE 1: VERIFICACION DE ARMAS (weapons.json)")
print("=" * 70)

weapons = load_json("weapons.json")
pdf_text = read_pdf("fallout_weapons.txt")
lines = pdf_text.split('\n')

# Build lookup of PDF weapon data by scanning table lines
# Format: each weapon table row has: NAME <dmg> CD [effects] [type] [fire rate] [range] [qualifiers...] <weight> <cost> <rarity>

weapon_ref = {}
current_weapon = None
current_data = []

for i, line in enumerate(lines):
    s = line.strip()
    if not s or s.startswith('===') or 'FALLOUT' in s or 'PAGE' in s:
        continue
    
    # Check if line starts a weapon table entry
    # Pattern: weapon name followed by a number and "CD"
    m = re.match(r'^([A-Za-z].*?)\s+(\d+)\s+CD\s', s)
    if m:
        name = m.group(1).strip()
        # Skip headers
        if name in ('WEAPON', 'SMALL GUN', 'ENERGY WEAPON', 'BIG GUN', 'MELEE WEAPON', 'THROWING WEAPON', 'EXPLOSIVE'):
            continue
        # Skip complication headers
        if 'Complication' in name:
            continue
        
        # Collect all data lines for this weapon until next weapon or section break
        weapon_ref[name] = {'line': i, 'text': s}
        
        # Collect subsequent lines that belong to this entry
        extra = []
        for j in range(i+1, min(i+4, len(lines))):
            nl = lines[j].strip()
            if not nl or nl.startswith('===') or 'FALLOUT' in nl or 'PAGE' in nl:
                break
            # If next line starts a new weapon, stop
            if re.match(r'^[A-Za-z].*?\d+\s+CD', nl):
                break
            extra.append(nl)
        
        weapon_ref[name]['extra'] = extra
        weapon_ref[name]['full'] = s + ' | ' + ' '.join(extra)

# Now compare
discrepancies = []
unmatched_json = []

for pdf_name, pdf_data in weapon_ref.items():
    # Find in JSON
    matched = None
    for w in weapons:
        if normalize(w['name']) == normalize(pdf_name):
            matched = w
            break
    
    if not matched:
        # Fuzzy match
        pn = normalize(pdf_name)
        for w in weapons:
            wn = normalize(w['name'])
            if pn in wn or wn in pn:
                matched = w
                break
    
    if not matched:
        continue
    
    full = pdf_data['full']
    
    # Extract all numbers from the full text
    nums = []
    for token in full.split():
        token = token.replace(',', '')
        try:
            if token == '<1' or token == '<1,':
                nums.append(0.5)
            else:
                f = float(token)
                nums.append(f)
        except ValueError:
            pass
    
    if len(nums) < 3:
        continue
    
    # Last 3 numbers should be weight, cost, rarity
    pdf_weight = nums[-3]
    pdf_cost = int(nums[-2])
    pdf_rarity = int(nums[-1])
    
    json_weight = matched['weight']
    if json_weight == '<1':
        json_weight = 0.5
    
    issues = []
    
    if abs(float(json_weight) - pdf_weight) > 0.1:
        issues.append(f"weight: JSON={matched['weight']} vs PDF≈{pdf_weight}")
    
    if matched['cost'] != pdf_cost:
        issues.append(f"cost: JSON={matched['cost']} vs PDF≈{pdf_cost}")
    
    if matched['rarity'] != pdf_rarity:
        issues.append(f"rarity: JSON={matched['rarity']} vs PDF≈{pdf_rarity}")
    
    if issues:
        discrepancies.append((matched['name'], issues))

# Check for JSON items not in PDF
for w in weapons:
    found = False
    for pdf_name in weapon_ref:
        if normalize(pdf_name) == normalize(w['name']):
            found = True
            break
    if not found:
        unmatched_json.append(w['name'])

if discrepancies:
    print(f"\n⚠  DISCREPANCIAS ENCONTRADAS ({len(discrepancies)} armas):")
    for name, issues in discrepancies:
        print(f"\n  [{name}]")
        for i in issues:
            print(f"    {i}")
else:
    print("\n✓ Todas las armas verificadas — weight/cost/rarity OK")

if unmatched_json:
    print(f"\n⚠  Armas en JSON no encontradas en tabla PDF: {unmatched_json}")

# ═══════════════════════════════════════════════════
# Check THROWING WEAPONS separately
# ═══════════════════════════════════════════════════

print("\n" + "=" * 70)
print("VERIFICACION: Throwing Weapons + Explosives")
print("=" * 70)

# Throwing table lines 1720-1727
# Explosives table lines 1757-1774

throwing_ref = {
    'Throwing Knives': {'weight': 0.5, 'cost': 10, 'rarity': 1, 'damage': '3', 'damageEffects': ['Piercing 1'], 'qualities': ['Concealed', 'Suppressed', 'Thrown (C)']},
    'Tomahawk': {'weight': 0.5, 'cost': 15, 'rarity': 2, 'damage': '4', 'damageEffects': ['Piercing 1'], 'qualities': ['Suppressed', 'Thrown (C)']},
    'Javelin': {'weight': 4, 'cost': 10, 'rarity': 1, 'damage': '4', 'damageEffects': ['Piercing 1'], 'qualities': ['Suppressed', 'Thrown (M)']},
}

explosives_ref = {
    'Baseball Grenade': {'weight': 1, 'cost': 40, 'rarity': 1, 'damage': '5', 'damageEffects': [], 'damageType': 'Physical', 'qualities': ['Blast', 'Thrown (M)'], 'range': 'medium'},
    'Frag Grenade': {'weight': 0.5, 'cost': 50, 'rarity': 2, 'damage': '6', 'damageEffects': [], 'damageType': 'Physical', 'qualities': ['Blast', 'Thrown (M)'], 'range': 'medium'},
    'Molotov Cocktail': {'weight': 1, 'cost': 20, 'rarity': 1, 'damage': '4', 'damageEffects': ['Persistent'], 'damageType': 'Energy', 'qualities': ['Blast', 'Thrown (M)'], 'range': 'medium'},
    'Nuka Grenade': {'weight': 1, 'cost': 100, 'rarity': 4, 'damage': '9', 'damageEffects': ['Radioactive', 'Breaking', 'Vicious'], 'damageType': 'Energy', 'qualities': ['Blast', 'Thrown (M)']},
    'Plasma Grenade': {'weight': 0.5, 'cost': 135, 'rarity': 3, 'damage': '9', 'damageEffects': [], 'damageType': 'Energy', 'qualities': ['Blast', 'Thrown (M)']},
    'Pulse Grenade': {'weight': 0.5, 'cost': 100, 'rarity': 3, 'damage': '6', 'damageEffects': ['Stun'], 'damageType': 'Energy', 'qualities': ['Blast', 'Thrown (M)']},
    'Bottlecap Mine': {'weight': 1, 'cost': 75, 'rarity': 2, 'damage': '6', 'damageEffects': [], 'damageType': 'Physical', 'qualities': ['Blast', 'Mine']},
    'Frag Mine': {'weight': 1, 'cost': 50, 'rarity': 2, 'damage': '6', 'damageEffects': [], 'damageType': 'Physical', 'qualities': ['Blast', 'Mine']},
    'Nuke Mine': {'weight': 1, 'cost': 100, 'rarity': 4, 'damage': '9', 'damageEffects': ['Radioactive', 'Breaking', 'Vicious'], 'damageType': 'Energy', 'qualities': ['Blast', 'Mine']},
    'Plasma Mine': {'weight': 0.5, 'cost': 135, 'rarity': 3, 'damage': '9', 'damageEffects': [], 'damageType': 'Energy', 'qualities': ['Blast', 'Mine']},
    'Pulse Mine': {'weight': 0.5, 'cost': 100, 'rarity': 3, 'damage': '6', 'damageEffects': ['Stun'], 'damageType': 'Energy', 'qualities': ['Blast', 'Mine']},
}

weapons_by_name = {w['name']: w for w in weapons}

def check_weapon_ref(ref_dict, label):
    errs = []
    for name, ref in ref_dict.items():
        w = weapons_by_name.get(name)
        if not w:
            errs.append(f"\n  ❌ {name}: NO ENCONTRADO EN JSON")
            continue
        issues = []
        for field, ref_val in ref.items():
            json_val = w.get(field)
            if isinstance(json_val, str) and isinstance(ref_val, str):
                if normalize(json_val) != normalize(ref_val):
                    issues.append(f"  {field}: JSON='{json_val}' vs PDF='{ref_val}'")
            elif isinstance(json_val, list) and isinstance(ref_val, list):
                if sorted(normalize(x) for x in json_val) != sorted(normalize(x) for x in ref_val):
                    issues.append(f"  {field}: JSON={json_val} vs PDF={ref_val}")
            elif json_val != ref_val:
                issues.append(f"  {field}: JSON={json_val} vs PDF={ref_val}")
        if issues:
            errs.append(f"\n  ❌ {name}:")
            errs.extend(issues)
    return errs

throw_issues = check_weapon_ref(throwing_ref, "Throwing")
exp_issues = check_weapon_ref(explosives_ref, "Explosives")

for e in throw_issues + exp_issues:
    if not e.startswith("  ❌"):
        print(e)
    else:
        print(e)

if not throw_issues and not exp_issues:
    print("✓ Todas las throwing/explosives correctas")

# ═══════════════════════════════════════════════════
# Check damageEffects vs qualities mixup
# ═══════════════════════════════════════════════════

print("\n" + "=" * 70)
print("VERIFICACION: damageEffects vs qualities (posible mixup)")
print("=" * 70)

# These qualities should be DAMAGE EFFECTS, not qualities:
damage_effect_qualities = {'Blast', 'Burst', 'Breaking', 'Gatling', 'Debilitating', 'Persistent', 'Spread'}

mixup_found = False
for w in weapons:
    quals = set(normalize(q) for q in w.get('qualities', []))
    deffects = set(normalize(e) for e in w.get('damageEffects', []))
    
    # Check if any damage effect is listed as a quality
    for q in list(quals):
        if q in damage_effect_qualities:
            # Check if it's also (or should be) in damageEffects
            if q not in deffects:
                print(f"  ⚠  {w['name']}: '{q}' esta en qualities pero deberia ser damageEffect")
                mixup_found = True
    
    # Check if any quality is listed as a damage effect
    for d in list(deffects):
        if d in damage_effect_qualities:
            pass  # Correct - these belong in damageEffects

if not mixup_found:
    print("✓ No se detecto mixup damageEffects vs qualities")

# ═══════════════════════════════════════════════════
# Check descriptions
# ═══════════════════════════════════════════════════

print("\n" + "=" * 70)
print("VERIFICACION: Descripciones de armas")
print("=" * 70)

no_desc = []
for w in weapons:
    if not w.get('description') or w['description'].strip() == '':
        no_desc.append(w['name'])

if no_desc:
    print(f"  ⚠  {len(no_desc)} armas sin descripcion:")
    for n in no_desc[:10]:
        print(f"    - {n}")
    if len(no_desc) > 10:
        print(f"    ... y {len(no_desc)-10} mas")
else:
    print("✓ Todas las armas tienen descripcion")

# ═══════════════════════════════════════════════════
# ARMOR
# ═══════════════════════════════════════════════════

print("\n" + "=" * 70)
print("FASE 2: VERIFICACION DE ARMADURAS (armor.json)")
print("=" * 70)

armor = load_json("armor.json")
armor_pdf = read_pdf("fallout_armor.txt")

# Raider, Leather, Metal, Combat, Synth, Vault-Tec Security armor tables
# Format: Name PDR EDR RDR Location Weight Cost Rarity

armor_ref = {
    # Raider (lines 113-121)
    'Raider Chest Piece': {'physicalDR': 1, 'energyDR': 1, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 7, 'cost': 18, 'rarity': 0},
    'Raider Leg': {'physicalDR': 1, 'energyDR': 1, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 3, 'cost': 8, 'rarity': 0},
    'Raider Arm': {'physicalDR': 1, 'energyDR': 1, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 3, 'cost': 6, 'rarity': 0},
    'Sturdy Raider Chest Piece': {'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 12, 'cost': 33, 'rarity': 1},
    'Sturdy Raider Leg': {'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 7, 'cost': 13, 'rarity': 1},
    'Sturdy Raider Arm': {'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 7, 'cost': 8, 'rarity': 1},
    'Heavy Raider Chest Piece': {'physicalDR': 3, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 17, 'cost': 48, 'rarity': 2},
    'Heavy Raider Leg': {'physicalDR': 3, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 10, 'cost': 18, 'rarity': 2},
    'Heavy Raider Arm': {'physicalDR': 3, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 10, 'cost': 15, 'rarity': 2},
    
    # Leather (lines 126-134)
    'Leather Chest Piece': {'physicalDR': 1, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 5, 'cost': 25, 'rarity': 1},
    'Leather Leg': {'physicalDR': 1, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 2, 'cost': 10, 'rarity': 1},
    'Leather Arm': {'physicalDR': 1, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 2, 'cost': 8, 'rarity': 1},
    'Sturdy Leather Chest Piece': {'physicalDR': 2, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 10, 'cost': 50, 'rarity': 2},
    'Sturdy Leather Leg': {'physicalDR': 2, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 5, 'cost': 20, 'rarity': 2},
    'Sturdy Leather Arm': {'physicalDR': 2, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 5, 'cost': 18, 'rarity': 2},
    'Heavy Leather Chest Piece': {'physicalDR': 3, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 15, 'cost': 75, 'rarity': 3},
    'Heavy Leather Leg': {'physicalDR': 3, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 7, 'cost': 30, 'rarity': 3},
    'Heavy Leather Arm': {'physicalDR': 3, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 7, 'cost': 28, 'rarity': 3},
    
    # Metal (lines 144-155)
    'Metal Helmet': {'physicalDR': 2, 'energyDR': 1, 'radiationDR': 0, 'covers': ['Head'], 'weight': 3, 'cost': 15, 'rarity': 1},
    'Metal Chest Piece': {'physicalDR': 2, 'energyDR': 1, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 6, 'cost': 40, 'rarity': 1},
    'Metal Leg': {'physicalDR': 2, 'energyDR': 1, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 3, 'cost': 15, 'rarity': 1},
    'Metal Arm': {'physicalDR': 2, 'energyDR': 1, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 3, 'cost': 15, 'rarity': 1},
    'Sturdy Metal Helmet': {'physicalDR': 3, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Head'], 'weight': 8, 'cost': 65, 'rarity': 2},
    'Sturdy Metal Chest Piece': {'physicalDR': 3, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 16, 'cost': 115, 'rarity': 2},
    'Sturdy Metal Leg': {'physicalDR': 3, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 8, 'cost': 65, 'rarity': 2},
    'Sturdy Metal Arm': {'physicalDR': 3, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 8, 'cost': 65, 'rarity': 2},
    'Heavy Metal Helmet': {'physicalDR': 4, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Head'], 'weight': 12, 'cost': 115, 'rarity': 3},
    'Heavy Metal Chest Piece': {'physicalDR': 4, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 23, 'cost': 190, 'rarity': 3},
    'Heavy Metal Leg': {'physicalDR': 4, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 12, 'cost': 115, 'rarity': 3},
    'Heavy Metal Arm': {'physicalDR': 4, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 12, 'cost': 115, 'rarity': 3},
    
    # Combat (lines 160-171)
    'Combat Helmet': {'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Head'], 'weight': 4, 'cost': 25, 'rarity': 2},
    'Combat Chest Piece': {'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 8, 'cost': 60, 'rarity': 2},
    'Combat Leg': {'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 2, 'cost': 25, 'rarity': 2},
    'Combat Arm': {'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 2, 'cost': 25, 'rarity': 2},
    'Sturdy Combat Helmet': {'physicalDR': 3, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Head'], 'weight': 5, 'cost': 105, 'rarity': 3},
    'Sturdy Combat Chest Piece': {'physicalDR': 3, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 12, 'cost': 140, 'rarity': 3},
    'Sturdy Combat Leg': {'physicalDR': 3, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 5, 'cost': 105, 'rarity': 3},
    'Sturdy Combat Arm': {'physicalDR': 3, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 5, 'cost': 105, 'rarity': 3},
    'Heavy Combat Helmet': {'physicalDR': 4, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Head'], 'weight': 7, 'cost': 185, 'rarity': 4},
    'Heavy Combat Chest Piece': {'physicalDR': 4, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 16, 'cost': 220, 'rarity': 4},
    'Heavy Combat Leg': {'physicalDR': 4, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 7, 'cost': 185, 'rarity': 4},
    'Heavy Combat Arm': {'physicalDR': 4, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 7, 'cost': 145, 'rarity': 4},
    
    # Synth (lines 181-192)
    'Synth Helmet': {'physicalDR': 2, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Head'], 'weight': 3, 'cost': 33, 'rarity': 3},
    'Synth Chest Piece': {'physicalDR': 2, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 7, 'cost': 75, 'rarity': 3},
    'Synth Leg': {'physicalDR': 2, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 3, 'cost': 30, 'rarity': 3},
    'Synth Arm': {'physicalDR': 2, 'energyDR': 3, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 3, 'cost': 30, 'rarity': 4},
    'Sturdy Synth Helmet': {'physicalDR': 3, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Head'], 'weight': 7, 'cost': 70, 'rarity': 4},
    'Sturdy Synth Chest Piece': {'physicalDR': 3, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 12, 'cost': 125, 'rarity': 4},
    'Sturdy Synth Leg': {'physicalDR': 3, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 7, 'cost': 80, 'rarity': 4},
    'Sturdy Synth Arm': {'physicalDR': 3, 'energyDR': 4, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 7, 'cost': 70, 'rarity': 4},
    'Heavy Synth Helmet': {'physicalDR': 4, 'energyDR': 5, 'radiationDR': 0, 'covers': ['Head'], 'weight': 10, 'cost': 110, 'rarity': 5},
    'Heavy Synth Chest Piece': {'physicalDR': 4, 'energyDR': 5, 'radiationDR': 0, 'covers': ['Torso'], 'weight': 17, 'cost': 175, 'rarity': 5},
    'Heavy Synth Leg': {'physicalDR': 4, 'energyDR': 5, 'radiationDR': 0, 'covers': ['Leg'], 'weight': 10, 'cost': 130, 'rarity': 5},
    'Heavy Synth Arm': {'physicalDR': 4, 'energyDR': 5, 'radiationDR': 0, 'covers': ['Arm'], 'weight': 10, 'cost': 110, 'rarity': 5},
    
    # Vault-Tec Security (lines 197-198)
    'Vault-Tec Security Helmet': {'physicalDR': 2, 'energyDR': 0, 'radiationDR': 0, 'covers': ['Head'], 'weight': 2, 'cost': 20, 'rarity': 1},
    'Vault-Tec Security Armor': {'physicalDR': 2, 'energyDR': 0, 'radiationDR': 0, 'covers': ['Arms', 'Legs', 'Torso'], 'weight': 8, 'cost': 16, 'rarity': 1},
}

armor_by_name = {a['name']: a for a in armor}

armor_discrepancies = []
for ref_name, ref_data in armor_ref.items():
    a = armor_by_name.get(ref_name)
    if not a:
        armor_discrepancies.append(f"\n  ❌ {ref_name}: NO ENCONTRADO EN JSON")
        continue
    issues = []
    for field, ref_val in ref_data.items():
        json_val = a.get(field)
        if isinstance(json_val, list) and isinstance(ref_val, list):
            if sorted(json_val) != sorted(ref_val):
                issues.append(f"  {field}: JSON={json_val} vs PDF={ref_val}")
        elif json_val != ref_val:
            issues.append(f"  {field}: JSON={json_val} vs PDF={ref_val}")
    if issues:
        armor_discrepancies.append(f"\n  ❌ {ref_name}:")
        armor_discrepancies.extend(issues)

if armor_discrepancies:
    for d in armor_discrepancies:
        print(d)
else:
    print("✓ Todas las armaduras verificadas (Raider, Leather, Metal, Combat, Synth, Vault-Tec Security)")

print("\n" + "=" * 70)
print("VERIFICACION: headgear, clothing, outfits vs PDF")
print("=" * 70)

# Headgear from PDF pages 128-130
# The PDF lists: Army Helmet, BoS Hood, BoS Scribe's Hat, Casual Hat, Formal Hat, 
# Gas Mask, Hard Hat, Hood/Cowl, Sack Hood, Welder's Visor

hg_ref = {
    'Army Helmet': {'covers': ['Head'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 12, 'rarity': 1},
    'BoS Hood': {'covers': ['Head'], 'physicalDR': 1, 'energyDR': 1, 'radiationDR': 0, 'weight': 1, 'cost': 8, 'rarity': 1},
    "BoS Scribe's Hat": {'covers': ['Head'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 1, 'cost': 8, 'rarity': 1},
    'Casual Hat': {'covers': ['Head'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 1, 'cost': 3, 'rarity': 0},
    'Formal Hat': {'covers': ['Head'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 1, 'cost': 10, 'rarity': 0},
    'Gas Mask': {'covers': ['Head'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 1, 'weight': 3, 'cost': 15, 'rarity': 1},
    'Hard Hat': {'covers': ['Head'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 8, 'rarity': 0},
    'Hood or Cowl': {'covers': ['Head'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 1, 'cost': 5, 'rarity': 0},
    'Sack Hood': {'covers': ['Head'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 1, 'cost': 3, 'rarity': 0},
    "Welder's Visor": {'covers': ['Head'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 15, 'rarity': 1},
}

headgear = load_json("headgear.json")
hg_by_name = {h['name']: h for h in headgear}

# Also clothing and outfits
clothing_ref = {
    'Brotherhood of Steel Uniform': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 1, 'radiationDR': 1, 'weight': 3, 'cost': 10, 'rarity': 1, 'underArmor': True},
    'Casual Clothing': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 1, 'cost': 5, 'rarity': 0, 'underArmor': True},
    'Harness': {'covers': ['Torso'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 8, 'rarity': 0, 'underArmor': True},
    'Military Fatigues': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 3, 'cost': 8, 'rarity': 1, 'underArmor': True},
    'Road Leathers': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 5, 'cost': 10, 'rarity': 0, 'underArmor': True},
    'Tough Clothing': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 3, 'rarity': 0, 'underArmor': True},
}

# Actually clothing.json and outfits.json - we need to find the table in the PDF
# The clothing table is on page 128 of the PDF
# The PDF text extraction of the clothing table may not be clean

# Let me check the clothing from the JSON first
clothing = load_json("clothing.json")
outfits = load_json("outfits.json")

print(f"  Clothing en JSON: {[c['name'] for c in clothing]}")
print(f"  Outfits en JSON: {[o['name'] for o in outfits]}")

# Find clothing table in PDF
clothing_section = armor_pdf[armor_pdf.find('CLOTHING'):armor_pdf.find('CLOTHING')+1500] if 'CLOTHING' in armor_pdf else "Not found"
print(f"\n  Clothing PDF section found: {'Yes' if 'CLOTHING' in armor_pdf else 'No'}")

# Read headgear section  
headgear_section_start = armor_pdf.find('HEADGEAR')
if headgear_section_start >= 0:
    headgear_section = armor_pdf[headgear_section_start:headgear_section_start+2000]
else:
    # Try alternative names
    for term in ['Formal Hat', 'Army Helmet', 'Gas Mask', 'Hard Hat']:
        idx = armor_pdf.find(term)
        if idx >= 0:
            headgear_section = armor_pdf[max(0,idx-100):idx+1000]
            print(f"\n  Found headgear section near '{term}' at offset {idx}")
            # Show first 500 chars
            print(f"  First 500: {headgear_section[:500]}")
            break

print("\n" + "=" * 70)
print("VERIFICACION: clothing stats vs PDF page 128")
print("=" * 70)

# Verify clothing against PDF data
# From PDF text at page 128:
clothing_pdf = {
    'Brotherhood of Steel Uniform': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 1, 'radiationDR': 1, 'weight': 3, 'cost': 10, 'rarity': 1},
    'Casual Clothing': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 1, 'cost': 5, 'rarity': 0},
    'Harness': {'covers': ['Torso'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 8, 'rarity': 0},
    'Military Fatigues': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 3, 'cost': 8, 'rarity': 1},
    'Road Leathers': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 5, 'cost': 10, 'rarity': 0},
    'Tough Clothing': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 3, 'rarity': 0},
}

clothing_errs = []
for cl in clothing:
    ref = clothing_pdf.get(cl['name'])
    if not ref:
        clothing_errs.append(f"  ⚠  {cl['name']}: no en referencia PDF")
        continue
    issues = []
    for field, ref_val in ref.items():
        if cl.get(field) != ref_val:
            issues.append(f"  {field}: JSON={cl.get(field)} vs PDF={ref_val}")
    if issues:
        clothing_errs.append(f"\n  ❌ {cl['name']}:")
        clothing_errs.extend(issues)

for e in clothing_errs:
    print(e)
if not clothing_errs:
    print("✓ Todas las clothing verificadas correctamente")

# Outfits reference from PDF page 128-130
outfits_pdf = {
    'Brotherhood of Steel Fatigues': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 3, 'energyDR': 2, 'radiationDR': 0, 'weight': 6, 'cost': 18, 'rarity': 2},
    "Brotherhood Scribe's Armor": {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 2, 'energyDR': 2, 'radiationDR': 0, 'weight': 3, 'cost': 30, 'rarity': 2},
    'Cage Armor': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 2, 'energyDR': 0, 'radiationDR': 0, 'weight': 12, 'cost': 10, 'rarity': 1},
    'Drifter Outfit': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 3, 'cost': 5, 'rarity': 0},
    "Engineer's Armor": {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 1, 'radiationDR': 0, 'weight': 5, 'cost': 45, 'rarity': 1},
    'Formal Clothing': {},
    'Hazmat Suit': {'covers': ['Arms', 'Legs', 'Torso', 'Head'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 10, 'weight': 8, 'cost': 100, 'rarity': 3},
    'Heavy Coat': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 5, 'cost': 15, 'rarity': 0},
    'Hides': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 2, 'energyDR': 0, 'radiationDR': 0, 'weight': 8, 'cost': 10, 'rarity': 0},
    'Lab Coat': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': 2, 'cost': 20, 'rarity': 1},
    'Spike Armor': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 3, 'energyDR': 0, 'radiationDR': 0, 'weight': 15, 'cost': 15, 'rarity': 2},
    'Utility Coveralls': {'covers': ['Arms', 'Legs', 'Torso'], 'physicalDR': 1, 'energyDR': 0, 'radiationDR': 0, 'weight': 3, 'cost': 12, 'rarity': 0},
}

# Looking at the PDF page 128-130 more carefully, I see the table layout is:
# For Outfits on page 128: ITEM, LOCATIONS, PHYSICAL, ENERGY, RADIATION, WEIGHT, COST, RARITY
# Let me get the exact data from the PDF text
