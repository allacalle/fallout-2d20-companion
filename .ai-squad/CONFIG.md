# Project Configuration

## Project
- Name: Fallout RPG Web Companion
- Type: frontend (static SPA)
- Stack: Vanilla HTML + CSS + JavaScript
- Framework: None (vanilla SPA with hash routing)

## Agents (v7.1 — Human-Driven Architecture)
### Definition Team (propose options — Owner decides)
- **Researcher**: Researches options with pros/cons (Phase 0.5)
- **Architect**: Proposes ADRs with alternatives (Phase 0.7)
- **UX Architect**: Proposes UX flows and responsive (Phase 1)
- **Designer**: Proposes 2-3 visual directions (Phase 1.5)
- **Specifier**: Writes specs locked against ADRs (Phase 2)
- **Accessibility Auditor**: WCAG 2.2 AA audit (Phase 1.5)

### Execution Team (pure execution — zero decisions)
- **Frontend**: Builds UI from locked specs (Phase 4)
- **QA**: Tests + ADR compliance verification (Phase 4)
- **Integrator**: Verifies code matches ADRs (Phase 5)
- **Reality Checker**: Visual evidence + production readiness (Phase 6)

### Marketing (Post-Launch) — TBD

## Workflow
- **Mundo 1 (Definition)**: Owner decides architecture, UX, design, specs
- **Mundo 2 (Execution)**: Agents execute locked tasks, zero decisions

## Database
- Type: JSON files (static data)
- ORM: None (raw JSON read via fetch)

## Authentication
- Method: None (no auth needed)

## Deployment
- Platform: GitHub Pages → Vercel (future)
- CI/CD: GitHub Pages
