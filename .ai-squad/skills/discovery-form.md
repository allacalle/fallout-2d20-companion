# Discovery Form — Structured Requirements Gathering

## PURPOSE

Replaces free-form interviews with a **structured 6-field form** that captures everything needed before any work begins. Based on Nexu's finding that 80% of redirects happen because the brief was incomplete.

## THE 6 FIELDS

When the CEO starts a new feature or project, they MUST fill this form:

### 1. SURFACE — What are we building?
- [ ] Web app (desktop)
- [ ] Web app (mobile responsive)
- [ ] Mobile app prototype
- [ ] Landing page
- [ ] Dashboard / Admin panel
- [ ] API only
- [ ] Other: ______

### 2. AUDIENCE — Who will use this?
- [ ] Developers (high tech literacy)
- [ ] Business users (medium tech literacy)
- [ ] General public (varied tech literacy)
- [ ] Children / Seniors (low tech literacy, high accessibility needs)
- [ ] Internal team (specific domain knowledge)

### 3. TONE — What should it feel like?
- [ ] Professional / Corporate
- [ ] Friendly / Casual
- [ ] Playful / Fun
- [ ] Minimal / Serious
- [ ] Bold / Disruptive

### 4. BRAND CONTEXT — What existing brand/assets exist?
- [ ] No brand — start from scratch
- [ ] Basic brand — logo + colors exist
- [ ] Full brand — style guide, fonts, colors, voice all defined
- [ ] Competing with [specific brand] — need to differentiate

### 5. SCALE — How big is this?
- [ ] MVP — core feature only, ship fast
- [ ] V1 — core + nice-to-haves
- [ ] Full product — complete feature set
- [ ] Incremental — adding to existing system

### 6. CONSTRAINTS — What limits us?
- [ ] Budget: [describe]
- [ ] Timeline: [describe]
- [ ] Tech stack: [must use X, cannot use Y]
- [ ] Regulatory: [GDPR, HIPAA, etc.]
- [ ] Accessibility: [WCAG AA, WCAG AAA]
- [ ] Performance: [specific targets]

## HOW TO USE

### Method A: CEO fills directly
CEO reads the form and fills all 6 fields before launching any agents.

### Method B: Agent interviews (replaces /grill-me)
If the owner hasn't filled it, the CEO asks these 6 questions **one at a time** (not all at once). Each answer narrows the scope.

### Method C: Auto-fill from context
If `PRODUCT.md` or `README.md` exists, the CEO pre-fills what's known and asks only about gaps.

## OUTPUT

After filling, the CEO creates `docs/discovery/[feature-name].md`:

```markdown
# Discovery: [Feature Name]

| Field | Value |
|-------|-------|
| Surface | Web app (mobile responsive) |
| Audience | Business users (medium tech literacy) |
| Tone | Professional / Corporate |
| Brand Context | Basic brand — logo + colors exist |
| Scale | V1 — core + nice-to-haves |
| Constraints | Must use Next.js, WCAG AA, GDPR compliant |

## Implications for the team
- **Designer**: Use existing brand tokens, ensure WCAG AA contrast
- **Frontend**: Mobile responsive, Next.js components
- **Backend**: GDPR — data retention policies, consent management
- **QA**: Accessibility tests, GDPR compliance checks
```

## WHY THIS WORKS

Free-form conversations wander. Structured forms lock scope in **2 minutes**.

| Approach | Time | Redirects |
|----------|------|-----------|
| Free-form chat | 15-30 min | 3-5 redirects |
| Structured form | 2-5 min | 0-1 redirect |

The cost of a wrong direction is one form edit, not one finished sprint.

---

*Inspired by nexu-io/open-design discovery protocol (Turn-1 question form)*
