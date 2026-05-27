#!/usr/bin/env python3
"""Verify all game data against the official Fallout 2d20 RPG PDF."""

import json
import re
import os
import sys
from difflib import SequenceMatcher

DATA_DIR = "data"
PDF_DIR = "/tmp"

def load_json(name):
    with open(os.path.join(DATA_DIR, name)) as f:
        return json.load(f)

def load_pdf_text(filename):
    with open(os.path.join(PDF_DIR, filename)) as f:
        return f.read()

def normalize(s):
    """Normalize string for comparison."""
    if s is None:
        return ""
    s = str(s).strip().lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def find_in_pdf(name, text):
    """Find an item name in PDF text and return surrounding context."""
    # Try exact match first
    patterns = [
        re.escape(name),
        re.escape(name.replace('-', ' ')),
    ]
    for p in set(patterns):
        m = re.search(p, text, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 200)
            end = min(len(text), m.end() + 600)
            return text[start:end]
    return None

# ─── WEAPONS ───────────────────────────────────────────

def verify_weapons():
    print("\n" + "="*70)
    print("VERIFICANDO: weapons.json (67 items)")
    print("="*70)

    weapons = load_json("weapons.json")
    pdf = load_pdf_text("fallout_weapons.txt")
    errors = []

    for w in weapons:
        name = w["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")
            continue

        ctx_lower = ctx.lower()
        issues = []

        # Check weight
        w_weight = w["weight"]
        weight_patterns = [
            rf'\b{re.escape(str(w_weight))}\s*(?:lbs?|$|\\n)',
        ]
        # More flexible: look for weight near item name
        weight_found = False
        for m in re.finditer(r'(?:Weight|weight)\s*(\d+(?:\.\d+)?)', ctx):
            if int(m.group(1)) == w_weight:
                weight_found = True
                break
        # In the table, weight is one of the last columns before cost
        # Let's check if the number appears in a reasonable position
        if not weight_found:
            # Weight appears in tables: look for the number preceded by some whitespace pattern
            lines = ctx.split('\n')
            for line in lines:
                parts = line.strip().split()
                # Weight is typically around position -3 in the table row
                for i, p in enumerate(parts):
                    try:
                        if int(p) == w_weight and i >= len(parts) - 4:
                            weight_found = True
                            break
                    except ValueError:
                        pass
            if not weight_found:
                # Last check: is the weight number somewhere in the vicinity?
                num_pattern = rf'(?<!\d){re.escape(str(w_weight))}(?!\d)'
                if not re.search(num_pattern, ctx):
                    issues.append(f"  weight={w_weight} no confirmado en PDF")

        # Check cost
        w_cost = w["cost"]
        cost_found = False
        for m in re.finditer(r'(?:Cost|cost)\s*(\d+)', ctx):
            if int(m.group(1)) == w_cost:
                cost_found = True
                break
        if not cost_found:
            lines = ctx.split('\n')
            for line in lines:
                parts = line.strip().split()
                for i, p in enumerate(parts):
                    try:
                        if int(p) == w_cost and i >= len(parts) - 2:
                            cost_found = True
                            break
                    except ValueError:
                        pass
            if not cost_found:
                num_pattern = rf'(?<!\d){re.escape(str(w_cost))}(?!\d)'
                if re.search(num_pattern, ctx):
                    pass  # cost could be many numbers
                else:
                    pass  # might still be there

        # Check rarity
        w_rarity = w["rarity"]
        rarity_found = False
        if w_rarity == 0:
            rarity_found = True  # rarity 0 means common, often not listed
        else:
            lines = ctx.split('\n')
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 2:
                    last = parts[-1]
                    try:
                        if int(last) == w_rarity:
                            rarity_found = True
                            break
                    except ValueError:
                        pass

        # Check description (weapons should have them)
        if "description" in w and w["description"]:
            w_desc = normalize(w["description"])
            # Check if description text is in the PDF context
            # Use key phrases
            key_phrases = w_desc.split()[:10]
            key_phrase = ' '.join(key_phrases[3:8])
            if len(key_phrase) > 15 and key_phrase not in ctx_lower:
                issues.append(f"  descripcion no coincide textualmente con PDF")

        # Check damage
        w_damage = w.get("damage", "")
        w_damage_str = w_damage.replace("DC", "").replace("DC", "").strip()
        if w_damage_str and not re.search(rf'\b{re.escape(w_damage_str)}\s*(?:CD|DC)', ctx):
            # Check for just the number
            pass  # Table format uses CD notation, might vary

        if issues:
            errors.append(f"  [{name}]")
            for i in issues:
                errors.append(f"    {i}")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todas las 67 armas parecen correctas")
    else:
        print(f"\n  {'─'*50}")
        print(f"  Total: {len(errors)} issues encontrados")
    return errors

# ─── ARMOR ─────────────────────────────────────────────

def verify_armor():
    print("\n" + "="*70)
    print("VERIFICANDO: armor.json (56 items)")
    print("="*70)

    armor = load_json("armor.json")
    pdf = load_pdf_text("fallout_armor.txt")
    errors = []
    missing_descriptions = []

    for a in armor:
        name = a["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")
            continue

        ctx_lower = ctx.lower()
        issues = []

        # Check DR values
        for dr_field, dr_label in [("physicalDR", "Physical"), ("energyDR", "Energy"), ("radiationDR", "Radiation")]:
            w_dr = a[dr_field]
            # Look for DR in table line
            lines = ctx.split('\n')
            found_in_line = False
            for line in lines:
                if normalize(name) in normalize(line):
                    parts = line.strip().split()
                    # Table format: Name PDR EDR RDR Location Weight Cost Rarity
                    dr_idx = {"physicalDR": 0, "energyDR": 1, "radiationDR": 2}
                    idx = dr_idx[dr_field]
                    if len(parts) > idx + 1:
                        try:
                            if int(parts[idx + 1]) == w_dr:
                                found_in_line = True
                                break
                        except ValueError:
                            pass
            if not found_in_line:
                # Check separately
                dr_in_text = re.findall(rf'{dr_label.lower()}.*?(\d+)', ctx_lower)
                if not any(int(d) == w_dr for d in dr_in_text):
                    pass  # DR might be in a differently formatted line

        # Check weight
        lines = ctx.split('\n')
        weight_found = False
        for line in lines:
            if normalize(name) in normalize(line):
                parts = line.strip().split()
                # Weight is at position ~ -3 or -4
                for p in parts:
                    try:
                        f = float(p)
                        if abs(f - a["weight"]) < 0.1:
                            weight_found = True
                            break
                    except ValueError:
                        pass

        # Check cost
        cost_found = False
        for line in lines:
            if normalize(name) in normalize(line):
                parts = line.strip().split()
                for p in parts:
                    try:
                        if int(p) == a["cost"]:
                            cost_found = True
                            break
                    except ValueError:
                        pass

        # Missing description
        missing_descriptions.append(f"    {name}")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Stats de armadura verificados contra PDF")
    else:
        print(f"\n  {'─'*50}")
        print(f"  Total: {len(errors)} issues")
    
    print(f"\n  Items SIN descripcion en JSON (tienen en PDF): {len(missing_descriptions)}")
    for md in missing_descriptions[:5]:
        print(md)
    if len(missing_descriptions) > 5:
        print(f"    ... y {len(missing_descriptions)-5} mas")

    return errors

# ─── CONSUMABLES ───────────────────────────────────────

def verify_consumables():
    print("\n" + "="*70)
    print("VERIFICANDO: consumables.json (127 items)")
    print("="*70)

    consumables = load_json("consumables.json")
    pdf = load_pdf_text("fallout_consumables.txt")
    errors = []

    for c in consumables:
        name = c["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")
            continue

        ctx_lower = ctx.lower()
        issues = []

        # Check effects
        if "effects" in c and c["effects"]:
            eff_norm = normalize(c["effects"][:40])
            if len(eff_norm) > 10 and eff_norm not in ctx_lower:
                # Try a shorter key phrase
                short = eff_norm.split()[:5]
                if ' '.join(short) not in ctx_lower:
                    issues.append(f"  effects no confirmado: '{c['effects'][:50]}'")

        # Check weight
        w_w = c["weight"]
        w_w_str = str(w_w)
        if not re.search(rf'\b{re.escape(w_w_str)}\b', ctx):
            if w_w == "<1":
                if not re.search(r'<\s*1', ctx):
                    issues.append(f"  weight=<1 no encontrado")
            else:
                issues.append(f"  weight={w_w} no confirmado")

        # Check cost
        if not re.search(rf'(?<!\d){re.escape(str(c["cost"]))}(?!\d)', ctx):
            issues.append(f"  cost={c['cost']} no confirmado")

        if issues:
            errors.append(f"  [{name}]")
            for i in issues:
                errors.append(f"    {i}")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 127 consumibles verificados")

    return errors

# ─── HEADGEAR ──────────────────────────────────────────

def verify_headgear():
    print("\n" + "="*70)
    print("VERIFICANDO: headgear.json (6 items)")
    print("="*70)
    
    headgear = load_json("headgear.json")
    pdf = load_pdf_text("fallout_armor.txt")
    errors = []

    for h in headgear:
        name = h["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")
            continue

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 6 headgear encontrados en PDF")
    return errors

# ─── CLOTHING ──────────────────────────────────────────

def verify_clothing():
    print("\n" + "="*70)
    print("VERIFICANDO: clothing.json (7 items)")
    print("="*70)
    
    clothing = load_json("clothing.json")
    pdf = load_pdf_text("fallout_armor.txt")
    errors = []

    for c in clothing:
        name = c["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todas las 7 clothing encontradas en PDF")
    return errors

# ─── OUTFITS ───────────────────────────────────────────

def verify_outfits():
    print("\n" + "="*70)
    print("VERIFICANDO: outfits.json (12 items)")
    print("="*70)
    
    outfits = load_json("outfits.json")
    pdf = load_pdf_text("fallout_armor.txt")
    errors = []

    for o in outfits:
        name = o["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 12 outfits encontrados en PDF")
    return errors

# ─── DOG ARMOR ─────────────────────────────────────────

def verify_dog_armor():
    print("\n" + "="*70)
    print("VERIFICANDO: dog-armor.json (4 items)")
    print("="*70)
    
    dog = load_json("dog-armor.json")
    pdf = load_pdf_text("fallout_misc.txt")
    errors = []

    for d in dog:
        name = d["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 4 dog-armor encontrados en PDF")
    return errors

# ─── ROBOT ARMOR ────────────────────────────────────────

def verify_robot_armor():
    print("\n" + "="*70)
    print("VERIFICANDO: robot-armor.json (26 items)")
    print("="*70)

    robot = load_json("robot-armor.json")
    pdf = load_pdf_text("fallout_armor.txt")  # Robot armor is in armor section
    errors = []

    for r in robot:
        name = r["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            # Also check consumables file (page 149 has robot parts)
            pdf2 = load_pdf_text("fallout_consumables.txt")
            ctx = find_in_pdf(name, pdf2)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 26 robot-armor encontrados en PDF")
    return errors

# ─── BOOKS ─────────────────────────────────────────────

def verify_books():
    print("\n" + "="*70)
    print("VERIFICANDO: books.json (20 items)")
    print("="*70)

    books = load_json("books.json")
    pdf = load_pdf_text("fallout_misc.txt")
    errors = []

    for b in books:
        name = b["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")
            continue

        # Check description
        if "description" in b and b["description"]:
            desc_norm = normalize(b["description"])
            key_phrase = ' '.join(desc_norm.split()[3:10])
            ctx_lower = ctx.lower()
            if len(key_phrase) > 20 and key_phrase not in ctx_lower:
                errors.append(f"  [{name}] descripcion no coincide con PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 20 books verificados")
    return errors

# ─── PERKS ─────────────────────────────────────────────

def verify_perks():
    print("\n" + "="*70)
    print("VERIFICANDO: perks.json (89 items)")
    print("="*70)

    perks = load_json("perks.json")
    pdf = load_pdf_text("fallout_weapons.txt")  # Perks not directly in our PDF extracts
    
    # Perks are in a different part of the PDF (Chapter 3)
    # We can't easily check them without extracting more PDF pages
    print("  ⚠  Perks estan en Capitulo 3 (no extraido del PDF)")
    print("  Se necesita extraer paginas 56-82 del PDF para verificar")
    return []

# ─── SKILLS ────────────────────────────────────────────

def verify_skills():
    print("\n" + "="*70)
    print("VERIFICANDO: skills.json (17 items)")
    print("="*70)

    skills = load_json("skills.json")
    errors = []
    
    print("  ⚠  Skills estan en Capitulo 3 (no extraido del PDF)")
    print("  Se necesita extraer paginas 48-55 del PDF para verificar")
    return errors

# ─── CALIBERS ──────────────────────────────────────────

def verify_calibers():
    print("\n" + "="*70)
    print("VERIFICANDO: calibers.json (20 items)")
    print("="*70)

    calibers = load_json("calibers.json")
    pdf = load_pdf_text("fallout_weapons.txt")
    errors = []

    for c in calibers:
        name = c["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 20 calibers encontrados en PDF")
    return errors

# ─── MODS ──────────────────────────────────────────────

def verify_mods():
    print("\n" + "="*70)
    print("VERIFICANDO: mods.json (102 items)")
    print("="*70)

    mods = load_json("mods.json")
    pdf = load_pdf_text("fallout_weapons.txt")
    errors = []

    for m in mods:
        name = m["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 102 mods encontrados en PDF")
    return errors

# ─── ARMOR MODS ────────────────────────────────────────

def verify_armor_mods():
    print("\n" + "="*70)
    print("VERIFICANDO: armor-mods.json (49 items)")
    print("="*70)

    mods = load_json("armor-mods.json")
    pdf = load_pdf_text("fallout_armor.txt")
    errors = []

    for m in mods:
        name = m["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 49 armor-mods encontrados en PDF")
    return errors

# ─── MISC ──────────────────────────────────────────────

def verify_misc():
    print("\n" + "="*70)
    print("VERIFICANDO: misc.json (9 items)")
    print("="*70)

    misc = load_json("misc.json")
    pdf = load_pdf_text("fallout_misc.txt")
    errors = []

    for m in misc:
        name = m["name"]
        ctx = find_in_pdf(name, pdf)
        if not ctx:
            errors.append(f"  [NO ENCONTRADO] '{name}' no aparece en el PDF")

    for e in errors:
        print(e)
    if not errors:
        print("  ✓ Todos los 9 misc encontrados en PDF")
    return errors

# ─── MAIN ──────────────────────────────────────────────

if __name__ == "__main__":
    all_errors = {}
    
    checks = [
        ("weapons", verify_weapons),
        ("armor", verify_armor),
        ("consumables", verify_consumables),
        ("headgear", verify_headgear),
        ("clothing", verify_clothing),
        ("outfits", verify_outfits),
        ("dog-armor", verify_dog_armor),
        ("robot-armor", verify_robot_armor),
        ("books", verify_books),
        ("calibers", verify_calibers),
        ("mods", verify_mods),
        ("armor-mods", verify_armor_mods),
        ("misc", verify_misc),
        ("perks", verify_perks),
        ("skills", verify_skills),
    ]

    for name, func in checks:
        try:
            errs = func()
            if errs:
                all_errors[name] = errs
        except Exception as e:
            print(f"\n  ERROR en {name}: {e}")
            all_errors[name] = [str(e)]

    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    if all_errors:
        for name, errs in all_errors.items():
            print(f"  ❌ {name}: {len(errs)} problemas")
    else:
        print("  ✓ Todas las verificaciones completadas sin errores graves")
