# Decision Type Routing

Skill that classifies every decision into one of four types so the agent knows HOW to present it to the Owner.

## The Four Decision Types

```
┌─────────────────────────────────────────────────────────────────┐
│                   DECISION TYPE ROUTING                          │
├─────────────────┬──────────────┬──────────────┬──────────────────┤
│   ABANICO       │  INSTINTIVO  │   CERRADO    │   INCIERTO       │
│   AMPLIO        │              │              │                  │
├─────────────────┼──────────────┼──────────────┼──────────────────┤
│ Muchas opciones │ Gusto/taste  │ 1 respuesta  │ Falta contexto   │
│ (>5)            │ personal     │ correcta     │ del Owner        │
├─────────────────┼──────────────┼──────────────┼──────────────────┤
│ IA investiga    │ IA pregunta  │ IA resuelve  │ IA reporta       │
│ reduce a 2-3    │ directo      │ + opcional   │ incertidumbre    │
│                 │              │ confirmación │ y pregunta       │
├─────────────────┼──────────────┼──────────────┼──────────────────┤
│ Tiempo humano:  │ Tiempo:      │ Tiempo:      │ Tiempo:          │
│ ~10 seg         │ ~2 seg       │ ~0 seg       │ ~5 seg           │
└─────────────────┴──────────────┴──────────────┴──────────────────┘
```

## Decision Classification Tree

When you face a decision, ask yourself:

```
1. Are there more than 5 viable options?
   │
   ├── YES → ABANICO AMPLIO
   │        → Research, reduce to 2-3 with pros/cons
   │        → Owner picks
   │
   └── NO → 2. Does it require the Owner's personal taste?
            │
            ├── YES → INSTINTIVO
            │        → Ask the Owner directly
            │        → Do NOT research, do NOT propose options
            │
            └── NO → 3. Is there 1 technically correct answer?
                     │
                     ├── YES → CERRADO
                     │        → Solve directly
                     │        → Optional: confirm with Owner
                     │
                     └── NO → INCIERTO
                              → Report your uncertainty
                              → Explain what information is missing
                              → Owner clarifies
```

## Agent Decision Type Assignments

| Agent | Default Type | Why |
|-------|-------------|-----|
| Researcher | ABANICO AMPLIO | Investigates stacks, libraries, approaches |
| Architect | ABANICO AMPLIO | Proposes architectural options |
| UX Architect | INSTINTIVO | Flows, responsive, brand — Owner's taste |
| Designer | INSTINTIVO | Palettes, visual directions |
| A11y Auditor | CERRADO | WCAG rules — apply standard |
| Specifier | CERRADO | Write contracts against ADRs |
| Frontend | CERRADO | Execute locked specs |
| Backend | CERRADO | Execute locked specs |
| QA | CERRADO | Verify against specs + ADRs |
| Integrator | CERRADO | Verify consistency |
| Reality Checker | INSTINTIVO + CERRADO | Judge usability + verify |
| Process Auditor | CERRADO | Verify process |
| Uncertainty Reporter | INCIERTO | Report doubts |

## Examples

### ABANICO AMPLIO
```
❌ "I researched 30 frontend frameworks. Here's the full list."
✅ "From 30 options, I filtered to 3 viable ones:
   A) React — mature ecosystem, 43k⭐, 72% market share
   B) Vue — simpler, 22k⭐, gentle learning curve
   C) Svelte — modern, 7k⭐, fewer resources
   Owner: which one do you prefer?"
```

### INSTINTIVO
```
❌ "I researched 5 color palettes with their hex codes."
✅ "Owner, do you prefer dark or light tones for the dashboard?"
```

### CERRADO
```
❌ "I propose using bcrypt... or maybe argon2... what do you think?"
✅ "This is a closed decision: bcrypt is the OWASP standard. Implementing.
   (Optional confirmation: shall I use bcrypt for passwords?)"
```

### INCIERTO
```
❌ "I assume the Owner wants SQLite."
✅ "I don't know if this project will scale to thousands of users.
   My confidence is 60%. If MVP → SQLite. If you expect scale → PostgreSQL.
   Owner: what is the user horizon?"
```
