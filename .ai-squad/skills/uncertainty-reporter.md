# Uncertainty Reporter

Skill for agents to self-assess confidence and report uncertainty to the Owner BEFORE making assumptions.

## Why This Exists

Experiments B0-B5 proved that when an agent is unsure and assumes anyway, it creates bugs. The solution is NOT to eliminate uncertainty (impossible) but to surface it before it becomes code.

## The Uncertainty Scale

| Level | Label | Meaning | Action |
|-------|-------|---------|--------|
| 90-100% | CERTAIN | Known pattern, clear spec | Execute, optional confirm |
| 70-89% | CONFIDENT | Strong signal, some ambiguity | Execute, mention assumption |
| 50-69% | UNSURE | Multiple valid interpretations | STOP. Report uncertainty. |
| <50% | BLIND | No signal, guessing | STOP. Must ask Owner. |

## When to Report Uncertainty

Report uncertainty when ANY of these are true:

1. **Missing context**: Owner hasn't specified something you need
2. **Multiple valid paths**: 2+ approaches with no clear winner
3. **Ambiguous requirement**: The spec can be read in >1 way
4. **Unknown trade-off**: You don't know which dimension matters more (speed vs memory vs readability)
5. **Unfamiliar domain**: You're outside your training distribution

## DO NOT Report Uncertainty When

- The decision is purely mechanical (what variable name to use)
- The answer is in an ADR or spec you haven't read yet
- The decision has 1 correct answer (use Decision Type Routing → CERRADO)
- The Owner already gave explicit guidance on this exact question

## Uncertainty Report Template

```markdown
## ⚠️ Uncertainty Report: [Agent Name]

### What I'm unsure about
[One sentence — what exactly is uncertain?]

### Why I'm unsure
[Context that's missing / multiple valid interpretations / unknown trade-off]

### My confidence level: [50-69% / <50%]

### What I need from the Owner
[Specific question — yes/no or A/B choice]
```

### Examples

**Good uncertainty report:**
```
⚠️ Uncertainty Report: Backend Agent
What: Should the API return 400 or 422 for validation errors?
Why: The spec says "validation error" but doesn't specify the HTTP status code.
Confidence: 60%
Need: Owner, 400 Bad Request or 422 Unprocessable Entity?
```

**Bad uncertainty report (don't do this):**
```
⚠️ Uncertainty Report: Backend Agent
What: Not sure about the architecture.
Why: Lots of decisions to make.
Confidence: 40%
Need: Owner, what should I do?
```

## Integration with Decision Type Routing

The Uncertainty Reporter skill should be invoked AFTER classifying the decision type:

1. Classify decision type using `decision-type-routing` skill
2. If type is `INCIERTO` → generate uncertainty report
3. If type is `ABANICO AMPLIO` → research + reduce, don't report uncertainty
4. If type is `INSTINTIVO` → ask directly, don't report uncertainty
5. If type is `CERRADO` → execute, don't report uncertainty

## Integration with Process Auditor

The Process Auditor (agents/process-auditor.md) will check:
- Before each phase transition, did any agent have unresolved uncertainty?
- Are there open uncertainty reports in `docs/pending-decisions/`?
- If yes → BLOCK phase transition until resolved
