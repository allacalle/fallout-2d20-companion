#!/usr/bin/env python3
"""Precise verification of JSON against PDF extracted tables."""

import json, re, os

DATA_DIR = "data"

def load_json(name):
    with open(os.path.join(DATA_DIR, name)) as f:
        return json.load(f)

def read_pdf(filename):
    with open(os.path.join("/tmp", filename)) as f:
        return f.read()

def normalize_name(n):
    return n.lower().strip().replace("'", "").replace("’", "")

# ─── WEAPONS ──────────────────────────────────────

# Extract table data DIRECTLY from PDF text
# Lines 509-565: Small Guns
# Lines 894-912: Energy Weapons  
# Lines 1146-1179: Big Guns
# Lines 1381-1411: Melee Weapons
# Lines 1720-1727: Throwing
# Lines 1757-1774: Explosives

pdf_tables = read_pdf("fallout_weapons.txt")

def find_weapon_in_table(name, text):
    """Find weapon data by parsing table lines near the weapon name."""
    name_lower = normalize_name(name)
    lines = text.split('\n')
    
    # Find lines containing the weapon name
    for i, line in enumerate(lines):
        if normalize_name(line.split('  ')[0].strip()) == name_lower:
            # Get context: this line and next few lines
            chunk = '\n'.join(lines[max(0,i-1):min(len(lines),i+5)])
            return chunk
    return None

# Parse weight/cost/rarity from table lines
def parse_weapon_stats(chunk):
    """Try to extract weight, cost, rarity from table chunk."""
    # Pattern: table lines often end with "weight cost rarity"
    # or have qualifiers followed by those numbers
    lines = chunk.split('\n')
    results = {}
    
    for line in lines:
        line = line.strip()
        # Skip empty lines, headers, page markers
        if not line or line.startswith('===') or 'PAGE' in line or 'FALLOUT' in line:
            continue
        
        # Find numbers at end of line
        parts = line.split()
        numbers = []
        for p in parts:
            try:
                # Handle <1
                if p == '<1':
                    numbers.append(0.5)
                else:
                    numbers.append(float(p))
            except ValueError:
                pass
        
        if len(numbers) >= 3:
            # Last numbers should be weight, cost, rarity
            results['weight'] = numbers[-3]
            results['cost'] = int(numbers[-2])
            results['rarity'] = int(numbers[-1])
            break
    
    return results

# Now compare all weapons
weapons = load_json("weapons.json")
weapons_by_name = {w["name"]: w for w in weapons}

print("="*70)
print("VERIFICACION PRECISA: WEAPONS")
print("="*70)

# Build reference from PDF tables
pdf_ref = {}
current_section = None

lines = pdf_tables.split('\n')
for i, line in enumerate(lines):
    s = line.strip()
    if not s:
        continue
    
    # Try to parse weapon entries from table rows
    # A table row typically has: name number CD effects type number range qualifiers number number number
    # Look for lines matching: "<name> <number> CD"
    m = re.match(r'^([A-Za-z][A-Za-z\s\-]+?)\s+(\d+)\s+CD', s)
    if m:
        wname = m.group(1).strip()
        # Skip headers
        if wname in ('WEAPON', 'SMALL', 'ENERGY', 'BIG', 'MELEE', 'THROWING', 'EXPLOSIVE'):
            continue
        
        # Get context
        chunk_lines = [s]
        for j in range(1, 5):
            if i+j < len(lines):
                nl = lines[i+j].strip()
                if nl and not nl.startswith('===') and 'FALLOUT' not in nl and 'PAGE' not in nl:
                    chunk_lines.append(nl)
                else:
                    break
        
        chunk = ' '.join(chunk_lines)
        
        # Extract numbers
        nums = [float(x) for x in re.findall(r'(?:<1|\d+(?:\.\d+)?)', chunk)]
        
        # For ranged weapons: damage rating, fire rate, weight, cost, rarity
        # For melee: damage rating, weight, cost, rarity
        # For throwing: damage rating, weight, cost, rarity
        
        if len(nums) >= 2:
            pdf_ref[wname] = {'raw': chunk, 'numbers': nums}

# Compare
discrepancies = []
missing_in_json = []
missing_in_pdf = []

for pdf_name, pdf_data in pdf_ref.items():
    # Find matching JSON item
    matched = None
    for jname in weapons_by_name:
        if normalize_name(pdf_name) == normalize_name(jname):
            matched = jname
            break
    
    if not matched:
        # Try partial match
        for jname in weapons_by_name:
            pn = normalize_name(pdf_name)
            jn = normalize_name(jname)
            if pn in jn or jn in pn:
                matched = jname
                break
    
    if not matched:
        missing_in_json.append(pdf_name)
        continue
    
    w = weapons_by_name[matched]
    nums = pdf_data['numbers']
    
    # Check weight
    json_weight = w['weight']
    if json_weight == '<1':
        json_weight = 0.5
    pdf_weight = nums[-3] if len(nums) >= 3 else None
    
    # Check cost  
    json_cost = w['cost']
    pdf_cost = int(nums[-2]) if len(nums) >= 2 else None
    
    # Check rarity
    json_rarity = w['rarity']
    pdf_rarity = int(nums[-1]) if len(nums) >= 1 else None
    
    issues = []
    
    if pdf_weight is not None and abs(float(json_weight) - pdf_weight) > 0.1:
        # Check if the PDF parsed incorrectly
        issues.append(f"weight: JSON={json_weight} vs PDF≈{pdf_weight}")
    
    if pdf_cost is not None and json_cost != pdf_cost:
        issues.append(f"cost: JSON={json_cost} vs PDF≈{pdf_cost}")
    
    if pdf_rarity is not None and json_rarity != pdf_rarity:
        issues.append(f"rarity: JSON={json_rarity} vs PDF≈{pdf_rarity}")
    
    if issues:
        discrepancies.append((matched, issues))

# Check for JSON items not found in PDF
for jname, w in weapons_by_name.items():
    found = False
    for pdf_name in pdf_ref:
        if normalize_name(pdf_name) == normalize_name(jname):
            found = True
            break
    if not found:
        missing_in_pdf.append(jname)

if discrepancies:
    for name, issues in discrepancies:
        print(f"\n❌ {name}:")
        for i in issues:
            print(f"   {i}")
else:
    print("✓ No discrepancies found")

if missing_in_json:
    print(f"\n⚠  Missing from JSON: {missing_in_json}")
if missing_in_pdf:
    print(f"\n⚠  Missing from PDF ref: {missing_in_pdf}")
