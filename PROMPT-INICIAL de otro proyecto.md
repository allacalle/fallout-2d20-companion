# PROMPT-INICIAL — Experimento B7: Imaginarium (AI Art Gallery)

## Instrucciones para el AI

Lee este archivo completo antes de empezar. Este es el Experimento B7 del framework AI-SQUAD.

---

## Contexto

Este es el experimento 7 del **Diario de Experimentos con Agentes IA** de Alfonso Lacalle García. El objetivo es construir **Imaginarium** — una galería de arte moderna donde cualquier visitante escribe un prompt y Pollinations.ai genera una imagen que se guarda en la galería. Una obra de arte colaborativa alimentada por IA.

**Stack:** React 19 + Vite 6 + TypeScript + Express + SQLite (better-sqlite3) + Pollinations.ai

**Backend:** Express en puerto 3001
**Frontend:** Vite con proxy a 3001 en desarrollo
**BD:** SQLite con better-sqlite3 (sincrónica)

---

## Archivos clave del contexto

- `docs/VISION.md` — Visión completa del proyecto: diseño, API, componentes, esquema BD

---

## Reglas del Framework AI-SQUAD v7.1

1. **Human Core**: El humano decide en cada fase. Tú traduces a tareas.
2. **Decision Type Routing**: Clasifica decisiones en ABANICO_AMPLIO, INSTINTIVO, CERRADO, INCIERTO.
3. **Regla #8**: NUNCA escribas código directamente. Delega a agentes especializados.
4. **Task Handoff Protocol**: Usa el protocolo de handoff para delegar tareas.
5. **Uncertainty Reporter**: Si tu confianza es <70%, PARA y pregunta al humano.
6. **Closure Protocol**: Al cerrar, actualiza docs, Engram, diario y arrancar.sh.
7. **Regla #10 — Debug Protocol**: Cuando el output no es el esperado, inspecciona el dato real en la frontera del sistema antes de reescribir o reintentar. Añade logging RAW. Compara formato esperado vs recibido. Ajusta el parser al dato real. Nunca asumas que tu código es correcto hasta que veas los datos que recibe.

---

## Fases del experimento

```
FASE 0: Discovery    → 6-field form (Surface, Audience, Tone, Brand, Scale, Constraints) — YA HECHO en VISION.md
FASE 0.5: Research   → Investigación técnica: Pollinations.ai API, better-sqlite3, Express + CORS
🚦 HITL #1: Owner aprueba visión y stack
FASE 1: Spec         → Contratos (componentes, data flow, API calls, acceptance criteria)
FASE 2: Plan         → Asignar tareas en BACKLOG.md
FASE 3: Design       → Tokens visuales, layout, WCAG
🚦 HITL #2: Owner aprueba diseño
FASE 4: Build        → Agentes en paralelo (Backend, Frontend, QA)
FASE 5: Verify       → QA + tests + realidad
🚦 HITL #3: Owner valida funcionalidad
FASE 6: Document     → STATE.md, DONE.md, retrospectiva
🚦 HITL #4: Owner cierra sprint
```

---

## Lo que NO hay que hacer

- No implementar autenticación ni login
- No implementar borrado de imágenes
- No implementar edición de prompts
- No implementar paginación (carga todas las imágenes)
- No implementar rate limiting
- No guardar imágenes en disco (solo URL en BD)
- No resolver todo tú mismo — delega a agentes

---

## Lo que SÍ hay que hacer

- Frontend React 19 + Vite 6 + TypeScript
- Backend Express + TypeScript (puerto 3001)
- BD SQLite con better-sqlite3 (tabla `images`)
- API REST con 4 rutas (GET list, POST create, GET by id, PATCH like)
- Conexión a Pollinations.ai desde el backend (POST create → generar imagen)
- Grid masonry responsivo (3/2/1 columnas)
- Input de prompt grande con estado de carga
- Modal de vista ampliada al hacer clic en imagen
- ❤️ like sin auth (cualquiera puede dar like)
- Diseño oscuro con acentos púrpura y cian (museo de arte moderno)
- CSS Modules para todos los estilos
- Proxy de Vite a backend en desarrollo

---

## API de Pollinations.ai

**Endpoint para generar imágenes:**
```
GET https://image.pollinations.ai/prompt/{prompt_encoded}
```

- No requiere API key
- El prompt se codifica en URL
- Devuelve la imagen directamente (binario)
- Ejemplo: `https://image.pollinations.ai/prompt/un%20perro%20espacial%20con%20gafas`

**Endpoint para prompt description (opcional):**
```
GET https://text.pollinations.ai/{prompt}
```

---

## Datos de Alfonso (para el asistente)

- **Nombre:** Alfonso Lacalle García
- **GitHub:** https://github.com/allacalle
- **Portfolio:** https://portfolio-alfonso.vercel.app
- **Web:** alfonsolacalle.dev
- **LinkedIn:** https://linkedin.com/in/alfonso-l-4a23b148
- **Perfil:** Ingeniero de Software (Universidad de Córdoba). Freelance web, Flutter, Godot. Creador de AI-SQUAD.
- **Stack:** JavaScript, TypeScript, Python, React, Astro, Vite, Node.js, Flutter, Godot

---

## API Key

La API de Pollinations.ai es **keyless** — no necesita API key. No hay .env ni configuración extra de API keys.

---

**¡Empieza por la FASE 0: Discovery!**
