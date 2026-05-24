# Grill Me

**Type:** Requirements | **Use:** Owner requests something vague or before starting any feature

## Description

The agent interviews you relentlessly, one question at a time, until there's total understanding.

## When to use

- The Owner says "build me this" but the description is vague
- Before starting any significant feature
- When requirements are unclear or incomplete

## Rules

1. **One question at a time** - Don't overwhelm
2. **Push on ambiguity** - If something is vague, dig deeper
3. **Never assume** - Ask, don't guess
4. **Always give your recommendation** alongside the question

## Format

```
❓ Question: [what you need to know]
   Options:
   A) [option 1]
   B) [option 2]
   C) [option 3]

💡 My recommendation: [your suggested answer]
   Agreed? If not, what do you prefer?
```

## Example

```
❓ Question 1: Which auth method do you prefer?
   Options:
   A) Email + password
   B) OAuth (Google, GitHub)
   C) Both

💡 My recommendation: Email+password first (simpler), OAuth later
   Agreed?
```

## Integration with framework

After the interview is complete:
1. Update BACKLOG.md with clear tasks
2. Launch the appropriate agents
3. Reference the interview decisions in task descriptions
