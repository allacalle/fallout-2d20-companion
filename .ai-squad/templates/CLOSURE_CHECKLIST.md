# Closure Checklist — AI-SQUAD v7.1

4-step closure protocol. Run at the end of each sprint/experiment.

## Step 1: Sync Docs

- [ ] `docs/BACKLOG.md` — mark all tasks as DONE or archive
- [ ] `.ai-squad/docs/ACTIVE.md` — clear (empty = no active tasks)
- [ ] `.ai-squad/docs/DONE.md` — add sprint summary
- [ ] `.ai-squad/docs/STATE.md` — update current state
- [ ] `.ai-squad/docs/GAP_APPROVAL.md` — close resolved gaps

## Step 2: Engram Memory

- [ ] Save summary to Engram:
  - What was built
  - Key decisions
  - Bugs found and fixed
  - Lessons learned

## Step 3: Startup Instructions

- [ ] Generate `SERVIDOR.txt` (or update) with:
  - Port used
  - Startup command
  - Recovery command (`lsof -i :PORT`, `kill`)
- [ ] If it exists, generate/update `arrancar.sh`

## Step 4: Cost Tracking

- [ ] Log models used in `.ai-squad/docs/COST_TRACKING.md`
  - Which agent executed each phase
  - Which model was actually used
  - Deviations from agents.json

---

## Post-Closure

- [ ] Commit with message: "closure: [sprint-name] — [summary]"
- [ ] If experiment: copy summary to diario-de-experimentos/
