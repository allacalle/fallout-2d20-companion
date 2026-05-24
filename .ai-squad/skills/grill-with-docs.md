# Grill With Docs

**Type:** Requirements | **Use:** Project start or large feature

## Description

Like grill-me, but ALSO creates `docs/CONTEXT.md` (glossary) and ADRs (Architecture Decision Records).

## When to use

- Start of a new project
- Beginning a large feature
- When domain language needs to be consistent

## Documentation File Structure

| File | Purpose |
|------|---------|
| `docs/CONTEXT.md` | Glossary of domain terms |
| `docs/adr/` | Architecture decisions |

## During the Session

### Stress-test the glossary

When the Owner defines terms, push back if definitions are vague:

> "Your glossary defines 'cancellation' as X, but it seems you mean Y — which is it?"

### Clarify ambiguous terms

> "You say 'account' — do you mean the Client or the User? Those are different things."

### Domain relationships

When discussing domain relationships, stress-test with specific scenarios. Invent edge cases that force precision.

> "Your code cancels entire Orders, but you said partial cancellation is possible — which is reality?"

### Offer ADRs moderately

Create an ADR when a decision is:
1. **Hard to reverse** — will cost a lot to change later
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"

## Output

```markdown
# CONTEXT.md

## Glossary
| Term | Definition |
|------|-----------|
| [term] | [clear definition] |

## Decisions
- [decision 1 with brief reason]
- [decision 2 with brief reason]

## Architecture
[Brief description of current architecture]
```

```markdown
# ADR-[N]: [Decision Title]

## Context
[What led to this decision]

## Decision
[What was decided]

## Consequences
[What this means going forward]
```
