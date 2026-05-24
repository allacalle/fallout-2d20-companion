# Discovery: Fallout RPG Web Companion

| Field | Value |
|-------|-------|
| **Surface** | Web app mobile responsive (SPA con hash routing) |
| **Audience** | Grupo de juego interno (dominio Fallout 2d20) |
| **Tone** | Vault-Tec de lujo — refugio premium (dorados, verde azulado, retro-futurista limpio) |
| **Brand** | Fallout 2d20 de Modiphius (ambientación 2077, sistema en `fallout_rpg.md`) |
| **Scale** | MVP: reglas, skills, perks, equipo con mods, creador de personajes básico |
| **Constraints** | Vanilla HTML+CSS+JS, datos en JSON, GitHub Pages, sin backend, sin auth, mobile-first |

## Implicaciones para el equipo
- **Researcher**: Investigar esquema óptimo de JSON para datos de juego relacionales (armas↔mods, skills↔atributos)
- **Architect**: ADRs sobre estructura de datos, organización del proyecto, routing SPA
- **Data Build**: Crear todos los JSONs a partir del manual (prioridad: equipo > reglas > skills > perks)
- **Designer**: Estética Vault-Tec premium con paleta dorado/verde azulado, tipografía retro-futurista
- **Frontend**: Vanilla JS SPA con hash routing, búsqueda rápida, filtros, mobile-first
