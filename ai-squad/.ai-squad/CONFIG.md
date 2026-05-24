# Project Configuration

## Project
- Name: [YOUR PROJECT NAME]
- Type: [backend/frontend/fullstack]
- Stack: [Node/React/Python/etc]
- Framework: [Next.js/Express/Django/etc]

## Agents (v7.0 — Human-Driven Architecture)
### Definition Team (propose options — Owner decides)
- **Researcher**: Researches options with pros/cons (Phase 0.5)
- **Architect**: Proposes ADRs with alternatives (Phase 0.7) 🆕
- **UX Architect**: Proposes UX flows and responsive (Phase 1) 🆕
- **Designer**: Proposes 2-3 visual directions (Phase 1.5)
- **Specifier**: Writes specs locked against ADRs (Phase 2)
- **Accessibility Auditor**: WCAG 2.2 AA audit (Phase 1.5 — after design chosen)

### Execution Team (pure execution — zero decisions)
- **Frontend**: Builds UI from locked specs (Phase 4)
- **Backend**: Builds APIs from locked specs (Phase 4)
- **QA**: Tests + ADR compliance verification (Phase 4)
- **Integrator**: Verifies code matches ADRs (Phase 5)
- **Reality Checker**: Visual evidence + production readiness (Phase 6)

### Marketing (Post-Launch)
- Content Strategist: Plans content
- Copywriter: Writes posts and threads
- Newsletter Writer: Email campaigns
- Analytics Reporter: Measures results

## Workflow
- **Mundo 1 (Definition)**: Owner decides architecture, UX, design, specs
- **Mundo 2 (Execution)**: Agents execute locked tasks, zero decisions

## Database
- Type: [decided via ADR]
- ORM: [decided via ADR]

## Authentication
- Method: [decided via ADR]

## Deployment
- Platform: [decided via ADR]
- CI/CD: [decided via ADR]
