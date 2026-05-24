# Zoom Out

**Type:** Architecture | **Use:** When I don't know a code area well

## Description

Tell the agent to go up one level of abstraction. Get a map of all relevant modules and their callers, using the project's domain vocabulary.

## Workflow

1. **Identify the area** I'm unsure about
2. **Run zoom-out** on that area
3. **Read the module map** and understand relationships
4. **Proceed with understanding** of the full context

## Output Format

```
## [Module Name]
- Responsibility: [what it does]
- Callers: [who calls it]
- Dependencies: [what it depends on]
- Abstraction: [what it hides]
```

## Example

Owner: "How does the auth system work here?"

```
## Auth System
- auth.service.ts
  - Responsibility: JWT creation, validation, refresh
  - Callers: auth.routes.ts, middleware/auth.ts
  - Dependencies: db/users.ts, config/jwt.ts
  - Abstraction: Token generation and validation

## middleware/auth.ts
- Responsibility: Verify JWT on protected routes
- Callers: Express router
- Dependencies: auth.service.ts
- Abstraction: Token verification for routes
```

## When to use

- Before modifying unfamiliar code
- When debugging across multiple files
- When explaining system architecture
- Before making architectural decisions
