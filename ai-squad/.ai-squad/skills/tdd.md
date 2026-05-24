# TDD

**Type:** Development | **Use:** Building features or fixing bugs with discipline

## Description

Test-Driven Development: Red-Green-Refactor. Write tests first, then implementation.

## Core Principle

Tests should verify behavior through public interfaces, not implementation details. The code can change completely; the tests shouldn't.

**Good tests**: Integration-style. Exercise real code paths through public APIs. Describe WHAT the system does, not HOW. These tests survive refactors because they don't care about internal structure.

**Bad tests**: Coupled to implementation. Mock internal collaborators, test private methods, or verify via external means. Warning sign: your test breaks when you refactor, but behavior didn't change.

## Anti-pattern to avoid

**DON'T write all tests first then all implementation.** This produces garbage tests:

```
❌ Plan 10 tests
❌ Write 10 tests
❌ Write all implementation
❌ Tests are coupled to implementation details
```

**Correct approach**: Vertical slices. One test → one implementation → repeat.

## Workflow

### 1. Planning

- [ ] Understand the behavior to implement
- [ ] List behaviors to test (not implementation steps)
- [ ] Get Owner approval on the plan

Ask: "What should the public interface look like? What behaviors are most important?"

### 2. Red

- [ ] Write one failing test
- [ ] Run it → it fails (RED)
- [ ] Test describes behavior, not implementation

### 3. Green

- [ ] Write minimal code to pass
- [ ] Run it → it passes (GREEN)
- [ ] No speculative features added

### 4. Refactor

- [ ] Clean up code
- [ ] Extract duplication
- [ ] Run tests → still pass

### 5. Repeat

Go to step 2 for next behavior.

## Checklist

- [ ] Test describes behavior, not implementation
- [ ] Test uses public interfaces only
- [ ] Test runs in under 1 second
- [ ] No speculative features added
- [ ] Code passes all tests after refactor
