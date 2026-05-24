# Diagnose

**Type:** Debugging | **Use:** Hard bug or performance regression

## Description

A 6-phase debugging protocol. The core principle: you need a fast, deterministic signal before you can find a root cause.

## When to use

- Bug that's hard to reproduce
- Performance regression
- "It works on my machine" issues
- Intermittent failures

## The 6 Phases

### Phase 1: Feedback Loop

Build a tight loop to verify the bug.

**Rules:**
1. **Automate the signal** - script, test, curl
2. **Under 10 seconds** to run
3. **Deterministic** - same result every time
4. **Bisect** - if bug appeared between two known states

**Check:**
- Can I make it faster?
- Can I make the signal clearer?
- Can I make it more deterministic?

### Phase 2: Reproduce

Get the bug happening reliably in the feedback loop.

### Phase 3: Hypothesize

List possible causes. **Each hypothesis must be falsifiable**: state the prediction it makes.

```
H1: The cache isn't invalidated
   → Prediction: Clearing cache fixes it

H2: Race condition in auth
   → Prediction: Adding delay makes it consistent
```

### Phase 4: Instrument

Add probes to test each hypothesis. Each probe maps to a specific Phase 3 prediction.

### Phase 5: Fix

Apply the fix and verify with Phase 1 loop.

### Phase 6: Cleanup

Remove instrumentation. Add a test that catches this bug if it regresses.

## Rule: Ask for human help

**Question: what would have prevented this bug?** If the answer involves architectural change, hand off to `/improve-codebase-architecture`.
