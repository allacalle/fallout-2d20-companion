# Superpowers Discipline — Phase Enforcement

## PURPOSE

Prevents the CEO and agents from skipping phases. Enforces strict step-by-step execution. **The order matters**: experiments proved that Designer → Auditor → Devs → QA → Integrator produces dramatically better results than the old Build-everything-at-once approach.

## THE PHASES (v6.3 — corrected order)

Every feature MUST go through these phases IN ORDER. Skipping is FORBIDDEN.

```
Phase 0: DISCOVERY      → CEO fills 6-field Discovery Form
Phase 0.5: RESEARCH     → Researcher investigates tech, competitors, users
Phase 1: SPEC           → Specifier writes contracts (informed by research)
Phase 2: PLAN           → CEO assigns tasks to agents
Phase 3: DESIGN         → Designer creates DESIGN.md (Direction Picker + tokens)
Phase 3.5: A11Y AUDIT   → Accessibility Auditor runs WCAG 2.2 AA on DESIGN.md
Phase 4: BUILD          → Frontend + Backend + QA code in parallel
Phase 5: INTEGRATE      → Integrator verifies cross-agent contracts and connections
Phase 6: VERIFY         → Reality Checker validates visual evidence + production readiness
Phase 7: CEO INTEGRATE  → CEO verifies integration (npm test, npm run build, manual)
Phase 8: DOCUMENT       → Update STATE.md, BACKLOG.md, DONE.md
```

## CRITICAL ORDER RULES (learned from experiments)

- **Designer MUST go FIRST** (before devs). Skipping this caused quality failures in Exp1-4.
- **A11y Auditor MUST go SECOND** (before devs). Exp5 proved this produces WCAG AA products.
- **Integrator MUST run AFTER build** (before Verify). Without this, agents ship disconnected pieces.
- **Reality Checker MUST run AFTER Integration** (after connections are proven).

## ENFORCEMENT RULES

### For the CEO:

- **You CANNOT launch dev agents** before Phase 3.5 (A11y Audit) passes
- **You CANNOT skip Designer + A11y** — this was the winning formula
- **You CANNOT approve work** before Phase 5 (Integrator) verifies connections
- **You CANNOT mark done** before Phase 7 (CEO Integrate) succeeds
- **You CANNOT start next feature** before Phase 8 (Document) is complete

### For Agents:

- **Designer CANNOT code** — design tokens only
- **A11y Auditor CANNOT change designs** — audit only
- **Devs CANNOT start** until A11y Auditor approves Designer's work
- **Agents CANNOT report done** without running `npm test && npm run build`
- **Integrator CANNOT approve** without cross-agent contract verification
- **Reality Checker CANNOT approve** without visual evidence

### For Integrator (new in v6.3):

- **CANNOT approve** if any cross-agent contract mismatches
- **CANNOT approve** if integration tests fail
- **CANNOT approve** if GAP_APPROVAL items are unresolved
- **MUST block** with exact diff evidence when contracts don't match

## VIOLATION HANDLING

If anyone tries to skip a phase:

```
🚨 DISCIPLINE VIOLATION

Phase attempted: [X]
Required previous phase: [Y] — NOT COMPLETE

You must complete Phase [Y] before proceeding to Phase [X].
This is not optional. This is the discipline.

Experiments proved this order matters:
- Designer → A11y → Devs → Integrator → Verify = 137/137 tests, WCAG AA (Exp5)
- Build-everything-at-once = disconnected pieces, silent failures (Exp2-3)
```

## SLASH COMMANDS

These commands enforce phase transitions:

| Command | Phase | What it does |
|---------|-------|-------------|
| `/discovery [feature]` | Phase 0 | Fills 6-field structured brief |
| `/research [feature]` | Phase 0.5 | Launches Researcher |
| `/spec [feature]` | Phase 1 | Launches Specifier to write contracts |
| `/sprint-start` | Phase 2 | CEO reviews specs, assigns tasks |
| `/build` | Phase 4 | CEO launches Frontend + Backend + QA (Designer + A11y must be done) |
| `/integrate-check` | Phase 5 | CEO launches Integrator for cross-agent contract audit |
| `/review` | Phase 6 | Reality Checker validates visual evidence |
| `/integrate` | Phase 7 | CEO verifies end-to-end integration |
| `/done` | Phase 8 | CEO updates all docs, marks complete |

## WHEN TO USE STRICT MODE

**Strict mode ON** (enforce all phases):
- New feature from scratch
- Major refactor
- After a bug caused by skipped steps
- Multi-agent projects with > 2 agents

**Strict mode OFF** (allow skipping):
- Tiny typo fix
- Documentation update only
- Single-agent task
- Owner explicitly says "skip the process, just do it"

## CEO REMINDER

At the start of every session, announce:

```
📋 Current Phase: [X/8]
✅ Completed: [list of completed phases]
⏳ In Progress: [current phase]
🔒 Next: [next phase] — requires [prerequisite]

⚠️ Remember: Designer → A11y → Devs → Integrator → Verify
   This order was proven in 5 experiments. Don't skip.
```

---

*Inspired by obra/superpowers workflow discipline plugin*
*Phase order corrected based on experimental findings (Exp1-5, May 2026)*
