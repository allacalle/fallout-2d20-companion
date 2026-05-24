# AI-SQUAD v7.1 — Decision Type Routing Edition

> **You are the Software Engineer. The AI is your team.**
>
> Every decision classified. Every assumption eliminated. Every process audited.
>
> *v7.1: Decision Type Routing — ABANICO AMPLIO, INSTINTIVO, CERRADO, INCIERTO*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Version](https://img.shields.io/badge/version-7.1-blue.svg)](CHANGELOG.md)

---

## What is AI-SQUAD?

A complete **AI-powered software development framework** that puts **you** in control of architecture and design while specialized AI agents execute.

**The problem v6.x solved**: One AI doing everything sequentially → 20 specialized agents in parallel. 3x faster.

**The problem v7.0 solved**: AI-CEO made architectural decisions → **YOU make every decision via ADRs** with the "Preguntón" Principle.

**The problem v7.0 DIDN'T solve** (fixed in v7.1):

| Before (v7.0) | After (v7.1) |
|---------------|--------------|
| All decisions treated equally ("always propose 2-3 options") | **Decision Type Routing** — ABANICO (filter), INSTINTIVO (ask), CERRADO (execute), INCIERTO (report) |
| Orchestrator writes code directly (no watchdog) | **Process Auditor** blocks phase transitions if orchestrator violates protocol |
| Agent model assignments ignored in practice | **Handoff protocol** includes `model_required`, **Cost Tracking** logs deviations |
| Dead code and orphan files accumulate in parallel builds | **Post-merge audit** in Integrator detects orphans, dead code, test/prod divergence |
| No formal closure — docs desync between sessions | **Closure Protocol** syncs BACKLOG + ACTIVE + Engram + startup script |
| Ambiguous decisions become assumptions | **Uncertainty Reporter** forces agents to STOP and ask instead of assuming |

---

## The Two Worlds

### WORLD 1: DEFINITION (You drive, agents classify + propose)

No code. Only classified decisions. Agents know whether to research, ask, execute, or report uncertainty.

```
PHASE 0:  VISION       → You write 1 paragraph (what, for whom, why)
PHASE 0.5: RESEARCH    → Agent researches, filters 30→3 options
PHASE 0.7: ARCHITECTURE → Agent proposes classified ADRs, YOU choose
PHASE 1:  UX           → Agent asks directly (INSTINTIVO), YOU answer
PHASE 1.5: DESIGN      → Designer proposes 2-3 directions, YOU pick
PHASE 2:  SPEC TOTAL   → Specifier writes contracts (CERRADO)
PHASE 3:  PLAN TOTAL   → PM writes "cuadriculated" tasks
PHASE 3.5: AUDIT 🆕   → Process Auditor validates compliance
```

### WORLD 2: EXECUTION (Agents only, zero decisions)

No decisions. Only execution. Agents build exactly what was specified. Uncertainty is reported, never assumed.

```
PHASE 4:  BUILD        → FE + BE + QA execute locked tasks (CERRADO)
                         Uncertainty Reporter on ambiguity
PHASE 5:  INTEGRATE    → Integrator verifies code + post-merge audit 🆕
PHASE 6:  VERIFY       → QA + Reality Checker validate
PHASE 7:  CLOSURE      → Closure Protocol 🆕 (docs + engram + startup)
```

---

## Decision Type Routing 🆕

**Every decision is classified before it reaches the Owner. Not all decisions need the same treatment.**

| Type | When | Flow | Human Time |
|------|------|------|-----------|
| **ABANICO AMPLIO** | Many options (>5) | AI filters 30→3, Owner picks | ~10s |
| **INSTINTIVO** | Taste/personal preference | AI asks directly, Owner answers | ~2s |
| **CERRADO** | One correct answer | AI executes, optional confirm | ~0s |
| **INCIERTO** | Missing context | AI reports uncertainty, Owner clarifies | ~5s |

Old "Preguntón" Principle (v7.0): always propose 2-3 options.
New principle (v7.1): classify first, then choose the right flow.

---

## The 14 Agents

### Definition Team (classify + propose — you decide)

| Agent | Phase | Type | Role |
|-------|-------|------|------|
| **Researcher** | 0.5 | ABANICO | Investigates options, filters to 2-3 with evidence |
| **Architect** | 0.7 | ABANICO | Proposes classified ADRs with alternatives |
| **UX Architect** | 1 | INSTINTIVO | Asks you directly about flows, brand, responsive |
| **Designer** | 1.5 | INSTINTIVO | Proposes 2-3 visual directions, you pick |
| **Accessibility Auditor** | 1.5 | CERRADO | WCAG 2.2 AA audit on chosen design |
| **Specifier** | 2 | CERRADO | Writes contracts locked against ADRs |
| **Process Auditor** 🆕 | 3.5 | CERRADO | Validates process compliance before Build |

### Execution Team (pure execution — zero decisions)

| Agent | Phase | Type | Role |
|-------|-------|------|------|
| **Frontend** | 4 | CERRADO | Builds UI from locked specs + DESIGN.md |
| **Backend** | 4 | CERRADO | Builds APIs from locked specs + ADRs |
| **QA** | 4 | CERRADO | Tests against specs + verifies ADR compliance |
| **Integrator** 🆕 | 5 | CERRADO | Post-merge audit: dead code, orphans, divergence |
| **Reality Checker** | 6 | MIXTO | Visual evidence, production readiness |

---

## Architecture Decision Records (ADRs)

Every architectural decision is recorded with its **decision type**:

```markdown
# ADR-001: Database Engine
**Type**: ABANICO AMPLIO

## Context
Need persistence for users, notes, sessions. < 100 concurrent users.

## Options
1. **SQLite** — Zero config, no server. Pros: simple. Cons: no concurrency.
2. **PostgreSQL** — Robust, concurrent. Pros: production. Cons: needs server.

## Recommendation
SQLite for MVP (migration to PG is trivial with interface abstraction).

## Decision (Owner)
"SQLite is fine. If we scale we migrate."
```

---

## File Structure

```
your-project/
├── .ai-squad/                    ← v7.1
│   ├── agents/                   ← 14 agent prompts
│   │   ├── process-auditor.md    ← 🆕 NEW
│   │   ├── architect.md
│   │   ├── ux-architect.md
│   │   ├── researcher.md
│   │   ├── designer.md
│   │   ├── specifier.md
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   ├── qa.md
│   │   ├── integrator.md         ← MODIFIED (post-merge audit)
│   │   ├── accessibility-auditor.md
│   │   ├── reality-checker.md
│   │   └── docs-agent.md
│   ├── config/
│   │   ├── agents.json           # v7.1 with decision_type per agent
│   │   └── opencode.json         # v7.1 with process-auditor
│   ├── docs/
│   │   ├── AUDIT_LOG.md          ← 🆕 Process Auditor reports
│   │   ├── COST_TRACKING.md      ← 🆕 Model cost log
│   │   └── TASK_HANDOFFS.md      ← 🆕 Handoff templates
│   ├── skills/
│   │   ├── decision-type-routing.md  ← 🆕 NEW
│   │   ├── uncertainty-reporter.md   ← 🆕 NEW
│   │   └── ... (20 existing skills)
│   ├── templates/
│   │   ├── CLOSURE_CHECKLIST.md  ← 🆕 NEW
│   │   └── ... (4 existing templates)
│   ├── scripts/
│   │   └── closure-protocol.sh   ← 🆕 NEW
│   └── CONFIG.md
├── docs/
│   ├── architecture/             ← ADRs live here
│   ├── ux/
│   ├── specs/
│   └── research/
├── PROMPT-INICIAL.md             ← v7.1
├── README.md                     ← v7.1
├── CHANGELOG.md
└── INIT.md
```

---

## Versions

| Version | Branch | Paradigm |
|---------|--------|----------|
| **v7.1** 🆕 | `v7.0` | Decision Type Routing + Process Auditor |
| v7.0 | `v7.0` | Human-Driven Architecture (you decide, agents execute) |
| v6.3 | `master` | AI-CEO orchestrated (agents decide, you review) |

---

## Powered By

AI-SQUAD stands on the shoulders of giants:

- **[DESIGN.md](https://github.com/google-labs-code/design.md)** — Google Labs visual identity standard
- **[Agent Orchestration Kit](https://github.com/jcarlosrodicio/opencode-agent-orchestration-kit)** — jcarlosrodicio's OpenCode flows
- **[Agency Agents](https://github.com/msitarzewski/agency-agents)** — msitarzewski's agent collection
- **[Superpowers](https://github.com/obra/superpowers.git)** — obra's workflow discipline

---

## License

MIT — Use it however you want. Attribution appreciated.
