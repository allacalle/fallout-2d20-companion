# Integration Contracts — Cross-Agent Verification Protocol

## PURPOSE

Prevents the #1 failure mode of multi-agent development: agents produce correct artifacts in isolation that don't fit together. This skill enforces structured verification of every interface between agents.

Based on experimental findings: **integration is the bottleneck**. Agents build islands. This skill builds bridges.

---

## THE 5 INTEGRATION DIMENSIONS

Every feature must pass all 5 before marking "Done":

### 1. API CONTRACT MATCH
- Frontend HTTP calls ⇄ Backend registered endpoints
- Request method (GET/POST/PUT/DELETE) matches
- URL paths match exactly (no `/task` vs `/tasks`)
- Request body shape matches backend validation schema
- Response body shape matches frontend type expectations

### 2. DATA SHAPE MATCH
- Component props ⇄ API response types
- Backend service interfaces ⇄ Database schema columns
- No field name mismatches (`id` vs `_id`, `createdAt` vs `created_at`)
- No type mismatches (`string` vs `number`, `string[]` vs `Array<string>`)

### 3. ROUTER/CONFIG WIRING
- Every route file is imported in the main router
- Every middleware is applied to the correct routes
- Environment variables used in code exist in `.env.example`
- Database connection is configured and accessible

### 4. IMPORT/EXPORT CHAIN
- Every component is rendered by a parent (no orphans)
- Every service is imported and called somewhere
- Every utility function has at least one caller
- CSS files are imported by their components

### 5. END-TO-END FLOW
- User action → API call → Backend processing → DB write → Response → UI update
- Error path: Invalid input → Validation error → Error response → Error UI
- Loading path: Request sent → Loading state → Response received → Data rendered
- Empty state: No data → Empty UI message (not a crash or blank screen)

---

## VERIFICATION COMMANDS

### Quick Integration Health Check
```bash
# Are all routes registered?
grep -r "import.*routes\|app\.use\|router\.use" src/ --include="*.ts"

# Are components actually rendered?
grep -r "import.*[A-Z]" src/App.tsx src/pages/ --include="*.tsx"

# Are API calls consistent?
grep -r "fetch\|axios" src/components/ src/hooks/ --include="*.tsx"
grep -r "router\.\(get\|post\|put\|delete\)" src/routes/ --include="*.ts"

# Compare: every frontend call has a backend match?
# Use: comm <(extract-frontend-calls) <(extract-backend-endpoints)
```

### Placebo Coding Detection (Integration Edition)
```bash
# Find orphan files (exist but never imported/called)
for file in $(find src/ -name "*.ts" -o -name "*.tsx"); do
  basename=$(basename "$file" .ts)
  basename=$(basename "$basename" .tsx)
  if ! grep -rq "$basename" src/ --include="*.ts" --include="*.tsx" | grep -v "$file"; then
    echo "⚠️ ORPHAN: $file — never imported anywhere outside itself"
  fi
done
```

---

## INTEGRATION BLOCK RULES

Block the sprint (cannot proceed to Verify phase) if:

1. **Any API contract mismatch** — Frontend calls an endpoint that doesn't exist
2. **Any data shape mismatch** — Same field has different names across agents
3. **Orphan routes** — Route file exists but isn't registered in the router
4. **Orphan components** — Component exists but isn't rendered anywhere
5. **Integration tests fail** — End-to-end flow broken
6. **GAP_APPROVAL items unresolved** — Bugs detected but not assigned/fixed

### Block format:
```markdown
## 🚨 INTEGRATION BLOCKED

**Type**: [API / Data Shape / Router / Import / E2E / GAP]
**Agent A**: [FRONTEND] → expects [X]
**Agent B**: [BACKEND] → provides [Y]
**Mismatch**: [exact difference]
**Fix**: [which agent must change what]
**Evidence**: [grep output / test failure / diff]
```

---

## INTEGRATION APPROVAL CHECKLIST

Before marking integration complete:

- [ ] API contract audit: All frontend calls have matching backend endpoints
- [ ] Data shape audit: All types consistent across agent boundaries
- [ ] Router audit: All route files registered, no orphans
- [ ] Import audit: All components rendered, all services called
- [ ] E2E test: Happy path works from user action to UI update
- [ ] Error test: Invalid input shows proper error, doesn't crash
- [ ] Empty state: No-data scenario handled gracefully
- [ ] Build: `npm run build` succeeds
- [ ] Full test suite: `npm test` passes (including integration tests)
- [ ] GAP closure: All GAP_APPROVAL items for this feature are resolved

---

## WHY THIS PREVENTS THE #1 FAILURE

| Without Integration Contracts | With Integration Contracts |
|---|---|
| Frontend calls `/api/todos` | Verified backend registers `/api/todos` ✅ |
| Backend returns `{_id, name}` | Verified frontend expects `{id, title}` → MISMATCH caught |
| Route file exists but not wired | Orphan detection catches it |
| Component built, not rendered | Import audit catches it |
| "Tests pass" (unit only, mocked) | Integration test proves real connection |
| Bugs in GAP_APPROVAL.md, unfixed | Loop-closer tracks to resolution |

---

## LOOP-CLOSER INTEGRATION

This skill connects to the Loop-Closer protocol:

1. GAP_APPROVAL items found during integration audit
2. Each gap assigned to responsible agent
3. After agent claims fix, integrator re-verifies
4. Gap closed only when: (a) fix exists, (b) integration test passes, (c) cross-agent audit confirms

**No gap stays open. No feature ships with known bugs.**

---

*Based on experimental findings from 5 multi-agent development experiments — integration was the bottleneck in 4 out of 5.*
