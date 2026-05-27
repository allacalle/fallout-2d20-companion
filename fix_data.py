#!/usr/bin/env python3
"""Fix all game data discrepancies found against PDF manual."""

import json, os, pdfplumber

DATA_DIR = "data"
PDF_FILE = "Fallout - The Role Playing Game.pdf"

def load_json(name):
    with open(os.path.join(DATA_DIR, name)) as f:
        return json.load(f)

def save_json(name, data):
    with open(os.path.join(DATA_DIR, name), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Helper to normalize name for matching
def norm(n):
    return n.strip().lower().replace("'", "").replace("’", "").replace('"', "").replace("‘", "")

# ═══════════════════════════════════════════════════════════
# 1. FIX CONSUMABLES (food from PDF pages 151-153)
# ═══════════════════════════════════════════════════════════

print("="*60)
print("FIXING: Food consumables from PDF pages 151-153")
print("="*60)

# Extract food data from PDF
with pdfplumber.open(PDF_FILE) as pdf:
    pdf_consumables = {}
    for pn in [151, 152, 153, 155, 156, 157, 158, 162, 163, 166, 167, 169, 170]:
        page = pdf.pages[pn - 1]
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if len(row) < 4:
                    continue
                item_name = (row[0] or '').strip()
                if not item_name or item_name == 'ITEM' or item_name == 'AMMUNITION':
                    continue
                # Store raw row data
                pdf_consumables[item_name] = row

# Food: pages 151-153 have format: ITEM | HP HEALED | OTHER EFFECTS | IRRADIATED? | WEIGHT | COST | RARITY
food_corrections = {
    # Page 151
    'Baked Bloatfly': {'weight': '<1', 'cost': 15, 'rarity': 1, 'effects': 'Heals 6 HP, +2 Radiation DR'},
    'BlamCo Brand Mac and Cheese': {'weight': '<1', 'cost': 10, 'rarity': 1, 'effects': 'Heals 4 HP'},
    'Bloatfly Meat': {'weight': '<1', 'cost': 8, 'rarity': 0, 'effects': 'Heals 2 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Bloodbug Meat': {'weight': '<1', 'cost': 8, 'rarity': 1, 'effects': 'Heals 7 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Bloodbug Steak': {'weight': '<1', 'cost': 18, 'rarity': 2, 'effects': 'Heals 10 HP, Max HP +3 until end of following scene'},
    'Brahmin Meat': {'weight': 1, 'cost': 28, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Brain Fungus': {'weight': '<1', 'cost': 6, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Carrot': {'weight': '<1', 'cost': 3, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Cooked Softshell Meat': {'weight': '<1', 'cost': 40, 'rarity': 3, 'effects': 'Heals 9 HP, Gain +1 AP at start of next scene'},
    'Corn': {'weight': '<1', 'cost': 6, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Cram': {'weight': '<1', 'cost': 25, 'rarity': 1, 'effects': 'Heals 5 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Crispy Squirrel Bits': {'weight': '<1', 'cost': 6, 'rarity': 2, 'effects': 'Heals 6 HP'},
    'Dandy Boy Apples': {'weight': '<1', 'cost': 7, 'rarity': 0, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Deathclaw Egg': {'weight': '<1', 'cost': 69, 'rarity': 3, 'effects': 'Heals 7 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Deathclaw Meat': {'weight': 1, 'cost': 110, 'rarity': 3, 'effects': 'Heals 9 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    # Page 152
    'Deathclaw Omelette': {'weight': '<1', 'cost': 80, 'rarity': 4, 'effects': 'Heals 11 HP. If next scene is combat, regain 1 HP at start of each turn'},
    'Deathclaw Steak': {'weight': 1, 'cost': 130, 'rarity': 4, 'effects': 'Heals 14 HP. May re-roll 1d20 on all STR tests until end of next scene'},
    'Fancy Lads Snack Cakes': {'weight': '<1', 'cost': 18, 'rarity': 0, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Food Paste': {'weight': '<1', 'cost': 0, 'rarity': 2, 'effects': 'Heals 7 HP. May re-roll 1d20 on all END tests until end of next scene'},
    'Gourd': {'weight': 1, 'cost': 6, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Grilled Radroach': {'weight': '<1', 'cost': 7, 'rarity': 1, 'effects': 'Heals 5 HP'},
    'Grilled Radstag': {'weight': 1, 'cost': 60, 'rarity': 2, 'effects': 'Heals 11 HP. Carry weight increases by +25 until end of next scene'},
    'Gum Drops': {'weight': '<1', 'cost': 5, 'rarity': 0, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Iguana Bits': {'weight': '<1', 'cost': 8, 'rarity': 1, 'effects': 'Heals 4 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Iguana on a Stick': {'weight': '<1', 'cost': 33, 'rarity': 2, 'effects': 'Heals 6 HP'},
    'Iguana Soup': {'weight': 1, 'cost': 21, 'rarity': 3, 'effects': 'Heals 10 HP'},
    'InstaMash': {'weight': '<1', 'cost': 20, 'rarity': 0, 'effects': 'Heals 4 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Institute Food Packet': {'weight': '<1', 'cost': 10, 'rarity': 2, 'effects': 'Heals 5 HP'},
    'Melon': {'weight': 1, 'cost': 6, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Mirelurk Cake': {'weight': '<1', 'cost': 35, 'rarity': 3, 'effects': 'Heals 12 HP. Can breathe underwater until end of next scene'},
    'Mirelurk Egg': {'weight': 1, 'cost': 0, 'rarity': 2, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Mirelurk Egg Omelette': {'weight': '<1', 'cost': 30, 'rarity': 3, 'effects': 'Heals 7 HP. Immediately add 2 AP to the group pool'},
    'Mirelurk Meat': {'weight': '<1', 'cost': 18, 'rarity': 1, 'effects': 'Heals 6 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Mirelurk Queen Steak': {'weight': 1, 'cost': 130, 'rarity': 5, 'effects': 'Heals 14 HP. Reduce difficulty of all END tests by 1 until end of next scene'},
    'Mole Rat Chunks': {'weight': '<1', 'cost': 8, 'rarity': 1, 'effects': 'Heals 7 HP. +1 Max AP in group pool until end of current scene'},
    'Mole Rat Meat': {'weight': '<1', 'cost': 5, 'rarity': 0, 'effects': 'Heals 5 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Mongrel Dog Meat': {'weight': '<1', 'cost': 8, 'rarity': 0, 'effects': 'Heals 4 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Mutant Hound Chops': {'weight': '<1', 'cost': 12, 'rarity': 3, 'effects': 'Heals 8 HP. Heals 2 Radiation damage'},
    'Mutant Hound Meat': {'weight': '<1', 'cost': 8, 'rarity': 2, 'effects': 'Heals 5 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Mutfruit': {'weight': '<1', 'cost': 8, 'rarity': 0, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Mutt Chops': {'weight': '<1', 'cost': 12, 'rarity': 1, 'effects': 'Heals 6 HP'},
    'Noodle Cup': {'weight': '<1', 'cost': 20, 'rarity': 2, 'effects': 'Heals 6 HP'},
    'Perfectly Preserved Pie': {'weight': '<1', 'cost': 20, 'rarity': 3, 'effects': 'Heals 5 HP'},
    "Pork 'n' Beans": {'weight': '<1', 'cost': 10, 'rarity': 0, 'effects': 'Heals 4 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Potato Crisps': {'weight': '<1', 'cost': 7, 'rarity': 0, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    # Page 153
    'Potted Meat': {'weight': 1, 'cost': 25, 'rarity': 0, 'effects': 'Heals 6 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Queen Mirelurk Meat': {'weight': '<1', 'cost': 22, 'rarity': 4, 'effects': 'Heals 10 HP. May re-roll 1d20 on all END tests until end of next scene'},
    'Radroach Meat': {'weight': '<1', 'cost': 3, 'rarity': 0, 'effects': 'Heals 4 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Radscorpion Egg': {'weight': '<1', 'cost': 48, 'rarity': 3, 'effects': 'Heals 6 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Radscorpion Egg Omelette': {'weight': '<1', 'cost': 65, 'rarity': 4, 'effects': 'Heals 9 HP. Cure all addictions'},
    'Radscorpion Meat': {'weight': 1, 'cost': 55, 'rarity': 2, 'effects': 'Heals 9 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Radscorpion Steak': {'weight': 1, 'cost': 65, 'rarity': 3, 'effects': 'Heals 12 HP. +2 Energy DR until end of next scene'},
    'Radstag Meat': {'weight': 1, 'cost': 50, 'rarity': 1, 'effects': 'Heals 8 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Radstag Stew': {'weight': 1, 'cost': 60, 'rarity': 3, 'effects': 'Heals 12 HP. +3 Energy DR until end of next scene'},
    'Razorgrain': {'weight': '<1', 'cost': 5, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Ribeye Steak': {'weight': 1, 'cost': 40, 'rarity': 2, 'effects': 'Heals 10 HP'},
    'Roasted Mirelurk Meat': {'weight': '<1', 'cost': 40, 'rarity': 2, 'effects': 'Heals 8 HP. Gain +1 AP at start of next scene'},
    'Salisbury Steak': {'weight': '<1', 'cost': 20, 'rarity': 0, 'effects': 'Heals 5 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Silt Bean': {'weight': '<1', 'cost': 6, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Softshell Mirelurk Meat': {'weight': '<1', 'cost': 22, 'rarity': 2, 'effects': 'Heals 6 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Squirrel Bits': {'weight': '<1', 'cost': 4, 'rarity': 1, 'effects': 'Heals 4 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Squirrel on a Stick': {'weight': '<1', 'cost': 15, 'rarity': 2, 'effects': 'Heals 7 HP'},
    'Squirrel Stew': {'weight': 1, 'cost': 24, 'rarity': 2, 'effects': 'Heals 10 HP'},
    'Stingwing Filet': {'weight': '<1', 'cost': 35, 'rarity': 2, 'effects': 'Heals 11 HP. May re-roll 1d20 on all PER tests until end of next scene'},
    'Stingwing Meat': {'weight': '<1', 'cost': 30, 'rarity': 1, 'effects': 'Heals 8 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Sugar Bombs': {'weight': '<1', 'cost': 11, 'rarity': 0, 'effects': 'Heals 4 HP. Gain +1 AP at start of next scene. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Sweet Roll': {'weight': '<1', 'cost': 9, 'rarity': 1, 'effects': 'Heals 4 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Tarberry': {'weight': '<1', 'cost': 5, 'rarity': 3, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Tato': {'weight': '<1', 'cost': 7, 'rarity': 1, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Vegetable Soup': {'weight': 1, 'cost': 13, 'rarity': 2, 'effects': 'Heals 7 HP. +2 Radiation DR until end of next scene'},
}

consumables = load_json("consumables.json")
fix_count = 0
add_count = 0

for name, fix in food_corrections.items():
    # Find existing item
    found = None
    for c in consumables:
        if norm(c['name']) == norm(name):
            found = c
            break
    
    # Try partial match
    if not found:
        for c in consumables:
            if c['type'] == 'food' and (norm(name) in norm(c['name']) or norm(c['name']) in norm(name)):
                found = c
                break
    
    if found:
        changed = False
        for field in ['weight', 'cost', 'rarity', 'effects']:
            if field in fix and str(found.get(field)) != str(fix[field]):
                found[field] = fix[field]
                changed = True
        if changed:
            fix_count += 1
    else:
        # Add new item
        consumables.append({
            'id': 'food_' + name.lower().replace(" ", "_").replace("'", "").replace("/", "_"),
            'name': name,
            'type': 'food',
            'effects': fix['effects'],
            'duration': 'Instant',
            'addictive': False,
            'weight': fix['weight'],
            'cost': fix['cost'],
            'rarity': fix['rarity'],
        })
        add_count += 1

print(f"  Fixed {fix_count} existing food items, added {add_count} new items")

# ═══════════════════════════════════════════════════════════
# 2. FIX BEVERAGES (PDF page 162-163)
# ═══════════════════════════════════════════════════════════

print("\n" + "="*60)
print("FIXING: Beverages from PDF pages 162-163")
print("="*60)

beverage_corrections = {
    'Beer': {'weight': 1, 'cost': 5, 'rarity': 1, 'effects': 'Heals 0 HP. Alcoholic'},
    'Blood Pack': {'weight': '<1', 'cost': 10, 'rarity': 2, 'effects': 'Heals 3 HP'},
    'Bourbon': {'weight': 1, 'cost': 7, 'rarity': 2, 'effects': 'Heals 0 HP. Alcoholic. Re-roll 1d20 on END tests'},
    'Brahmin Milk': {'weight': '<1', 'cost': 15, 'rarity': 2, 'effects': 'Heals 1 HP. Heals 2 Radiation damage'},
    'Dirty Wastelander': {'weight': 1, 'cost': 10, 'rarity': 3, 'effects': 'Heals 0 HP. Alcoholic. Reduce difficulty of all STR tests by 1 and increase difficulty of all INT tests by 2 (in total)'},
    'Dirty Water': {'weight': '<1', 'cost': 5, 'rarity': 0, 'effects': 'Heals 2 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Glowing Blood Pack': {'weight': '<1', 'cost': 30, 'rarity': 3, 'effects': 'Heals 4 HP. +5 to Radiation DR'},
    'Irradiated Blood': {'weight': '<1', 'cost': 50, 'rarity': 2, 'effects': 'Heals 3 HP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Melon Juice': {'weight': '<1', 'cost': 6, 'rarity': 2, 'effects': 'Heals 3 HP. Heal 1 HP at start of each turn'},
    'Moonshine': {'weight': '<1', 'cost': 30, 'rarity': 3, 'effects': 'Heals 0 HP. Alcoholic. +2 Max HP'},
    'Mutfruit Juice': {'weight': '<1', 'cost': 8, 'rarity': 2, 'effects': 'Heals 3 HP. Re-roll 1d20 on all AGI tests'},
    'Nuka-Cherry': {'weight': 1, 'cost': 40, 'rarity': 3, 'effects': 'Heals 3 HP. Immediately gain +2 AP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Nuka-Cola': {'weight': 1, 'cost': 20, 'rarity': 2, 'effects': 'Heals 2 HP. Immediately gain +1 AP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Nuka-Cola Quantum': {'weight': 1, 'cost': 50, 'rarity': 5, 'effects': 'Heals 10 HP. Immediately gain +5 AP. Roll 2 CD rather than 1 for determining Radiation damage when consumed'},
    'Purified Water': {'weight': '<1', 'cost': 20, 'rarity': 1, 'effects': 'Heals 3 HP'},
    'Refreshing Beverage': {'weight': 1, 'cost': 110, 'rarity': 5, 'effects': 'Heals 11 HP. Heals 10 Radiation damage. Cures all addictions'},
    'Rum': {'weight': 1, 'cost': 8, 'rarity': 2, 'effects': 'Heals 0 HP. Alcoholic. Re-roll 1d20 on AGI tests'},
    'Vodka': {'weight': 1, 'cost': 5, 'rarity': 3, 'effects': 'Heals 2 HP. Alcoholic'},
    'Whiskey': {'weight': 1, 'cost': 5, 'rarity': 3, 'effects': 'Heals 0 HP. Alcoholic. Re-roll up to two d20 on STR tests (in total)'},
    'Wine': {'weight': 1, 'cost': 5, 'rarity': 3, 'effects': 'Heals 0 HP. Alcoholic. Immediately gain +1 AP'},
}

for name, fix in beverage_corrections.items():
    found = None
    for c in consumables:
        if norm(c['name']) == norm(name):
            found = c
            break
    
    if found:
        changed = False
        for field in ['weight', 'cost', 'rarity', 'effects']:
            if field in fix and str(found.get(field)) != str(fix[field]):
                found[field] = fix[field]
                changed = True
        if changed:
            fix_count += 1

print(f"  Beverages corrected")

# ═══════════════════════════════════════════════════════════
# 3. FIX CHEMS (PDF page 166-167)
# ═══════════════════════════════════════════════════════════

print("\n" + "="*60)
print("VERIFYING: Chems from PDF pages 166-167")
print("="*60)

# Chems were already verified as correct in the check
# But let's check/add a few that might need fixing
chem_verify = {
    'Ultra Jet': {'cost': 67, 'rarity': 2, 'addictive': True},
    'Stimpak Diffuser': {'cost': 200, 'rarity': 5},
    'Healing Salve': {'weight': '<1', 'cost': 20, 'rarity': 1},
    'Skeeto Spit': {'weight': '<1', 'cost': 40, 'rarity': 2},
    'RadAway (Diluted)': {'weight': '<1', 'cost': 50, 'rarity': 1},
    'Stimpak (Diluted)': {'weight': '<1', 'cost': 30, 'rarity': 1},
    'Jet Fuel': {'weight': '<1', 'cost': 60, 'rarity': 3, 'addictive': True},
    'Overdrive': {'weight': '<1', 'cost': 55, 'rarity': 3, 'addictive': True},
}

for name, fix in chem_verify.items():
    found = None
    for c in consumables:
        if norm(c['name']) == norm(name):
            found = c
            break
    if found:
        for field, val in fix.items():
            if str(found.get(field)) != str(val):
                print(f"  Fixing {name}: {field}={found[field]} -> {val}")
                found[field] = val
                fix_count += 1

print(f"  Chems verified")

# ═══════════════════════════════════════════════════════════
# SAVE UPDATED CONSUMABLES
# ═══════════════════════════════════════════════════════════

# Clean up: remove duplicate items
seen = {}
clean_consumables = []
for c in consumables:
    key = norm(c['name'])
    if key in seen:
        print(f"  Removing duplicate: {c['name']}")
        continue
    seen[key] = True
    clean_consumables.append(c)

save_json("consumables.json", clean_consumables)
dup_count = len(consumables) - len(clean_consumables)
print(f"\nSaved consumables.json with {len(clean_consumables)} items ({dup_count} duplicates removed)")

# ═══════════════════════════════════════════════════════════
# 4. ADD MISSING HEADGEAR
# ═══════════════════════════════════════════════════════════

print("\n" + "="*60)
print("FIXING: Adding missing headgear")
print("="*60)

headgear = load_json("headgear.json")
hg_names = {norm(h['name']) for h in headgear}

new_headgear = [
    {'id': 'army_helmet', 'name': 'Army Helmet', 'covers': ['head'], 'physicalDR': 2, 'energyDR': 0, 'radiationDR': 0, 'weight': 3, 'cost': 20, 'rarity': 1},
    {'id': 'brotherhood_of_steel_hood', 'name': 'Brotherhood of Steel Hood', 'covers': ['head'], 'physicalDR': 0, 'energyDR': 1, 'radiationDR': 0, 'weight': '<1', 'cost': 12, 'rarity': 2},
    {"id": "brotherhood_scribes_hat", "name": "Brotherhood Scribe's Hat", 'covers': ['head'], 'physicalDR': 0, 'energyDR': 2, 'radiationDR': 0, 'weight': '<1', 'cost': 8, 'rarity': 2},
    {'id': 'casual_hat', 'name': 'Casual Hat', 'covers': ['head'], 'physicalDR': 0, 'energyDR': 0, 'radiationDR': 0, 'weight': '<1', 'cost': 15, 'rarity': 1},
]

added = 0
for h in new_headgear:
    if norm(h['name']) not in hg_names:
        headgear.append(h)
        added += 1
        print(f"  Added: {h['name']}")

if added:
    save_json("headgear.json", headgear)
    print(f"  Saved headgear.json with {len(headgear)} items (+{added})")
else:
    print("  No new items needed")

# ═══════════════════════════════════════════════════════════
# 5. FIX CALIBERS NAMING
# ═══════════════════════════════════════════════════════════

print("\n" + "="*60)
print("FIXING: Calibers naming")
print("="*60)

calibers = load_json("calibers.json")
# Rename/alias: PDF uses "Shotgun Shell" not "Shotgun Shells"
for c in calibers:
    if c['name'] == 'Shotgun Shells':
        c['name'] = 'Shotgun Shell'
        print("  Renamed 'Shotgun Shells' -> 'Shotgun Shell'")
    if c['name'] == 'Railway Spike':
        c['name'] = 'Railway Spikes'
        print("  Renamed 'Railway Spike' -> 'Railway Spikes'")
    if c['name'] == 'Syringe Ammo':
        c['name'] = 'Syringe'
        print("  Renamed 'Syringe Ammo' -> 'Syringe'")
    if c['name'] == '.44 Magnum':
        c['name'] = '.44 Rounds'
        print("  Renamed '.44 Magnum' -> '.44 Rounds'")

save_json("calibers.json", calibers)
print("  Saved calibers.json")

# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════

print("\n" + "="*60)
print("CORRECCIONES COMPLETADAS")
print("="*60)
print(f"""
✅ Consumibles: {fix_count} items corregidos, {add_count} anadidos, duplicados limpiados
✅ Headgear: {added} items anadidos (Army Helmet, BoS Hood, BoS Scribe's Hat, Casual Hat)
✅ Calibers: nombres normalizados (Shotgun Shell, Railway Spikes, Syringe, .44 Rounds)
""")
