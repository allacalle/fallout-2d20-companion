# 🚀 INIT - Get Started in 2 Minutes

Step-by-step guide to activate AI-SQUAD v7.0 in your project.

---

## Step 1: Copy the Framework

```bash
# 1. Go to your project root
cd /path/to/your-project

# 2. Copy the .ai-squad/ folder (core framework)
cp -r /path/to/ai-squad/.ai-squad/ ./

# 3. Copy root documentation files
cp /path/to/ai-squad/*.md ./

# 4. Copy templates
cp /path/to/ai-squad/templates/ ./

# 5. Verify
ls -la .ai-squad/
```

**Expected result**:
```
.ai-squad/
├── agents/        # 12 agent prompts (10 dev + 2 new)
├── config/        # Configuration files
├── content/       # Brand content
├── docs/          # State files + architecture/ + ux/
├── skills/        # 22 specialized skills
├── templates/     # ADR, VISION, UX_DIRECTION, TASK
└── CONFIG.md      # Project config
```

---

## Step 2: Write Your Vision

Edit `docs/VISION.md` — one paragraph in natural language:

> "I want a URL shortener where users can paste a long URL, get a short code, and track how many clicks it gets. No ads, no accounts required for basic use. Premium users get custom slugs and analytics."

That's it. No tech decisions yet. Just what you want to build.

---

## Step 3: Start the AI

Open your AI assistant and say:

> "Read PROMPT-INICIAL.md and docs/VISION.md. I'm ready to architect this project."

The AI will now guide you through the Definition phases:
1. Research options (Researcher)
2. Architecture decisions (Architect → you choose ADRs)
3. UX decisions (UX Architect → you choose flows)
4. Visual decisions (Designer → you choose direction)

Then automatically move to Execution.

---

## Step 4: What to Expect

**Your job during Definition**:
- Read options presented by agents
- Choose in natural language ("Option A", "SQLite is fine for now", "I prefer mobile-first")
- Spend 5-10 minutes per decision point

**Your job during Execution**:
- Nothing. Agents execute locked tasks.
- Validate at the end (5-minute review)

---

## Step 5: Monitor Progress

```bash
# Check overall status
cat .ai-squad/docs/STATE.md

# See who's doing what
cat .ai-squad/docs/ACTIVE.md

# See completed tasks
cat .ai-squad/docs/DONE.md

# Check architecture decisions
ls docs/architecture/
```

---

## Startup Checklist

- [ ] `.ai-squad/` copied to project
- [ ] Root `.md` files copied
- [ ] `docs/VISION.md` written
- [ ] AI launched with `PROMPT-INICIAL.md`
- [ ] First ADR presented → you decide
- [ ] Proceed through Definition phases
- [ ] When Spec is locked → agents execute
- [ ] **Debug Protocol**: before retrying a failed integration, add RAW logging at the system boundary and compare expected vs actual format

---

## Troubleshooting

### "Agent won't stop asking questions"
That's by design in v7.0. It's called the "Preguntón Principle". Every decision needs your approval. Batch answers — read all options, then respond to all at once.

### "Can I skip some decisions?"
Yes. Say "I trust your recommendation on this one" and the agent uses their default. It'll be documented as "Owner delegated" in the ADR.

### "This is too slow"
Definition takes 10-15 minutes for a simple project, 30-45 for a complex one. Then agents execute everything without you. Total time < traditional development.

---

## Next Steps

👉 **[README.md](./README.md)** — Full framework overview
