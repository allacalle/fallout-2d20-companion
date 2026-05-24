# Task Handoffs — AI-SQUAD v7.1

Ready-to-use handoff templates for copy-paste-launch to each agent. The orchestrator MUST NOT write code — it must use these handoffs to delegate.

**v7.1**: All handoffs include `decision_type` and `model_required`.

---

## Template: Frontend Task

```
=== HANDOFF: {FE-NNN} ===
AGENTE: Frontend
ARCHIVO: src/{path/to/file}.ts
CONTRATO:
  - Input: {props o parámetros}
  - Output: {return value}
  - Behavior: {descripción exacta}
TESTS: {N} casos
  - {descripción test 1}
  - {descripción test 2}
ADRs: {ADR-NNN}, {ADR-NNN}
DECISION TYPE: CERRADO
MODEL REQUIRED: MiniMax M2.7
FORBIDDEN: {NO hacer X, NO usar Y, NO añadir Z}
CONTEXTO:
  - Colores definidos en types.ts (COLORS object)
  - Tamaño tile: 48px
  - Grid: 8x12

SPECS: docs/specs/{SPEC-NNN}.md
ADRS: docs/architecture/{ADR-NNN}.md
TIPO: UI Component / Game Logic / Utility
```

---

## Template: Backend Task

```
=== HANDOFF: {BE-NNN} ===
AGENTE: Backend
ARCHIVO: {internal/routes/model}.go (o equivalente)
CONTRATO:
  - Endpoint: {method} /api/{path}
  - Request: {type, fields}
  - Success: {status, response shape}
  - Error: {status, error shape}
TESTS: {N} casos
  - {descripción test 1}
  - {descripción test 2}
ADRs: {ADR-NNN}, {ADR-NNN}
DECISION TYPE: CERRADO
MODEL REQUIRED: MiniMax M2.7
FORBIDDEN: {NO cambiar schema, NO añadir dependencias}

SPECS: docs/specs/{SPEC-NNN}.md
ADRS: docs/architecture/{ADR-NNN}.md
```

---

## Template: QA Task

```
=== HANDOFF: {QA-NNN} ===
AGENTE: QA
ARCHIVO: tests/{path/to/test}.ts
CONTRATO:
  - Verificar que {component/función} cumple specs
  - Verificar ADR compliance de {archivo}
TESTS: {N} casos
  - {descripción test 1}
  - {descripción test 2}
ADRs a verificar: {ADR-NNN}, {ADR-NNN}
DECISION TYPE: CERRADO
MODEL REQUIRED: DeepSeek V4 Flash
FORBIDDEN: {NO modificar código fuente, NO añadir mock data}

SPECS: docs/specs/{SPEC-NNN}.md
ADRS: docs/architecture/{ADR-NNN}.md
```

---

## Template: Integrator Task 🆕

```
=== HANDOFF: INT-{NNN} ===
AGENTE: Integrator
ARCHIVO: docs/integration/{feature}.md
CONTRATO:
  - Verificar cada ADR vs código
  - Verificar contratos cross-agent
  - Verificar que FE y BE conectan
  - Post-merge audit: dead code, orphans, test/prod divergence
DECISION TYPE: CERRADO
MODEL REQUIRED: Qwen3.5 Plus
FORBIDDEN: NO modificar código fuente

ADRS a verificar: todos en docs/architecture/
SPECS: todos en docs/specs/
```

---

## Usage

1. Orchestrator reads BACKLOG.md
2. Copies the corresponding template
3. Fills in the fields with task info + spec + ADR
4. Launches the agent with the complete handoff
5. Marks in ACTIVE.md: `{TASK-ID} → {Agent} → IN_PROGRESS`

**The orchestrator does NOT touch the file until the agent reports DONE.**

---

## Debug Protocol (v7.1.1)

When integrating with an external API, include a **raw debug step** in the handoff:
- Log the raw response before parsing
- Compare expected format vs actual format
- If they don't match: fix the parser, don't assume the API will change

**Why:** In B6, the SSE parser expected `"data: "` (with space) but Google sent `"data:{...}"` (without space). The orchestrator retried 3 times assuming API failure instead of inspecting the raw data. Add `DECISION TYPE: DEBUG` to the handoff.

---

*AI-SQUAD v7.1 — Decision Type Routing Edition. Handoff Protocol enforced.*
