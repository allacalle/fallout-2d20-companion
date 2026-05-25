# ADR-001: Modelo de Datos JSON

## Contexto
El manual Fallout 2d20 de Modiphius tiene datos duplicados entre el Capítulo 4 (Equipment) y el Capítulo 5 (Survival/Workbenches). El mismo mod aparece en dos tablas separadas con campos diferentes (cap.4: efectos/peso/precio, cap.5: complejidad/perks/skill/rareza). Necesitamos un modelo normalizado sin duplicación, con relaciones por ID para navegación cruzada.

## Decisión
Usar archivos JSON separados por entidad, relacionados por IDs únicos. Cada hecho vive en un solo archivo.

## Estructura de archivos

```
data/
├── weapons.json       # Armas (todos los tipos)
├── armor.json         # Piezas de armadura (cada pieza = ID único)
├── armor-sets.json    # Bundles de armadura completa
├── armor-mods.json    # Mods de armadura (material + utility)
├── mods.json          # Mods de armas (todos los tipos unificados)
├── perks.json         # Perks
├── skills.json        # Skills
├── components.json    # Componentes de crafteo
├── calibers.json      # Calibres / municiones
├── consumables.json   # Chems, comida, bebidas
├── outfits.json       # Outfits completos (no permiten armadura encima)
└── clothing.json      # Ropa (permite armadura encima)
```

## Reglas del modelo

1. **Sin duplicación** — cada hecho vive en un solo archivo
2. **Relaciones por ID** — siempre se referencia por `id`, nunca se incrustan datos completos
3. **Navegación bidireccional** — armas → mods → perks → skills, y viceversa
4. **Cada pieza de armadura tiene su propio ID** — incluso variantes (standard/sturdy/heavy)
5. **Un solo `mods.json`** — todos los mods de armas juntos, filtrables por `partType` y `skillId`
6. **Script de validación** — verifica que todos los IDs referenciados existen (sin foreign keys rotas)

## Body Locations

```
Head | Torso | Left Arm | Right Arm | Left Leg | Right Leg
```

En el manual, "Arm" y "Leg" son genéricos (se pueden usar en izquierda o derecha). En el JSON, cada pieza individual tendrá `covers` con la ubicación específica.

## Tipos de armadura

| Tipo | underArmor | Piezas | Mods |
|------|-----------|--------|------|
| Armor (raider, leather, metal, combat, synth...) | true | Piecemeal: chest, arm, leg, head | 2: material + utility |
| Outfit (vault suit, hazmat, cage armor...) | false | Cuerpo entero | 1 (pocos) |
| Clothing (casual, road leathers...) | true | Cuerpo entero | 1 (ballistic weave) |

## Weapon Parts

Cada arma tiene partes que aceptan mods:
- **Small Guns**: receiver, barrel, stock, grip, magazine, sights, muzzle
- **Energy Weapons**: capacitor, barrel, stock, grip, sights, muzzle
- **Big Guns**: barrel, stock, sights, propellant, nozzle, etc.
- **Melee**: upgrade (un solo mod por arma)

## Validación

Se implementará un script `validate-data.js` que verificará:
- Todos los IDs referenciados existen en su archivo correspondiente
- No hay IDs duplicados dentro del mismo archivo
- Todos los campos requeridos están presentes
- Las relaciones bidireccionales son consistentes
