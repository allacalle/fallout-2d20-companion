# Vitest Testing

**Type:** Testing | **Use:** Writing unit and integration tests with Vitest

## Description

How to write unit and integration tests using Vitest with TypeScript.

## Workflow

1. **Understand the code** to test
2. **Write the test** following AAA pattern:
   1. Arrange (setup)
   2. Act (call the function)
   3. Assert (verify result)
3. **Run test** → verify it passes
4. **Check coverage**

## Test Structure

```ts
import { describe, it, expect, beforeEach } from 'vitest';

describe('ComponentName', () => {
  let instance: ComponentName;

  beforeEach(() => {
    instance = new ComponentName();
  });

  describe('methodName', () => {
    it('should do X when Y', () => {
      const result = instance.methodName(input);
      expect(result).toBe(expected);
    });

    it('should throw when invalid input', async () => {
      await expect(instance.methodName(invalidInput)).rejects.toThrow();
    });
  });
});
```

## Simple Function Test

```ts
// math.ts
export function add(a: number, b: number): number {
  return a + b;
}

// math.test.ts
import { describe, it, expect } from 'vitest';
import { add } from './math';

describe('add', () => {
  it('returns sum of two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('handles negative numbers', () => {
    expect(add(-1, -1)).toBe(-2);
  });
});
```

## Rules

- Test behavior, not implementation
- One assertion per test (when possible)
- Descriptive test names: "should X when Y"
- Use `beforeEach` for shared setup
- Mock external dependencies
