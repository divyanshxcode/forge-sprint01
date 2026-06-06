# Forge Sprint 01 — SEO Command Center | Full Build Context

**Event:** NMG Forge Sprint 01 Hackathon (Sat 6 June 2026, solo 6-hour build)  
**Workspace:** `/Users/divyansh-air/Local Disk/Codes/Github Clones/nmg`  
**Repo:** `seo-command-center/` (Claude Code plugin)

---

## 🎯 THE MISSION

Build an autonomous SEO audit agent (Claude Code plugin) that:
1. Ingests a Screaming Frog export (`internal_all.csv` + issue CSVs)
2. Detects 17 types of SEO issues using deterministic rules
3. Prioritizes them by severity
4. Writes fixes (title/meta rewrites, redirect map)
5. Outputs: live dashboard (localhost:7700) + report.json + report.html (client deliverable)

**Why:** Real technical SEO analysts do this by hand. You're automating it.

---

## 📋 THE 17 SEO RULES (from rulebook.md)

**Pre-filters:** Only `text/html` content. For duplicates, compare only indexable 200 pages.

| Issue Type | Rule | Severity |
|---|---|---|
| `missing_title` | Title 1 empty, indexable 200 page | High |
| `duplicate_title` | same Title 1 on 2+ indexable URLs | High |
| `title_too_long` | Title 1 Pixel Width > 561 OR Title 1 Length > 60 | Medium |
| `title_too_short` | Title 1 Length < 30 (and not empty) | Low |
| `missing_meta_description` | Meta Description 1 empty, indexable 200 page | Medium |
| `duplicate_meta_description` | same Meta Description 1 on 2+ indexable URLs | Medium |
| `meta_description_too_long` | Meta Description 1 Length > 155 | Low |
| `missing_h1` | H1-1 empty on a 200 page | Medium |
| `duplicate_h1` | same H1-1 on 2+ indexable URLs | Low |
| `broken_link` | Status Code 400–499 | High |
| `server_error` | Status Code 500–599 | High |
| `redirect` | Status Code 300–399 | Medium |
| `redirect_chain` | redirect whose Redirect URL is itself a redirecting URL | High |
| `thin_content` | Word Count < 200 on an indexable page | Low |
| `orphan_page` | Inlinks = 0 on an indexable 200 page | Medium |
| `non_indexable_but_linked` | Indexability = Non-Indexable AND Inlinks > 0 | Medium |
| `slow_page` | Response Time > 1.0 second | Low |

---

## 📊 SCORING BREAKDOWN (100 points)

### Auto-scored by harness (55 points)
- **Issue detection accuracy** (20 pts) — F1 score vs ground truth (biggest lever)
- Plugin installs, MCP boots, runs end-to-end (14 pts)
- report.json schema valid (5 pts)
- Prioritization correct, fix artifacts valid, efficiency (9 pts)

### Process-scored from logs (25 points)
- ≥10 incremental commits, spread over time (6 pts)
- Real agentic architecture in audit log (sub-agents + tools) (7 pts)
- Debugging discipline (caught + fixed failures) (7 pts)
- Verification / self-tests before done (5 pts)

### Human demo (20 points)
- Live dashboard quality (7 pts)
- Report quality / actionability (7 pts)
- Code explanation + surprise export demo (6 pts)

### Gate (caps score at 40 if violated)
- Missing/faked audit.jsonl or single giant commit → 40
- Hard-coded for sample export → 0 accuracy
- Cannot explain your code → capped

---

## 🏗️ ARCHITECTURE (Already Built)

```
seo-command-center/
├── .claude-plugin/plugin.json         # Plugin manifest
├── .claude/
│   ├── settings.json                  # Hooks config (KEEP, already fixed)
│   ├── hooks/audit.sh                 # Records every tool call → audit.jsonl
│   └── audit.jsonl                    # Process log (auto-written, graded)
├── skills/seo-audit/SKILL.md          # Orchestrator (pipeline steps)
├── agents/
│   ├── ingest.md                      # Load export, report URLs
│   ├── auditor.md                     # Run detectors, check coverage
│   ├── fixer.md                       # Model: rewrite titles/meta, build redirects (TODO)
│   └── reporter.md                    # Render report + export HTML
├── mcp/server.py                      # MCP tools + live dashboard host (localhost:7700)
├── seo/detector.py                    # **YOUR MAIN WORK** — deterministic detectors
├── dashboard/
│   ├── index.html                     # Cockpit UI
│   └── app.js                         # Real-time SSE updates
├── outputs/
│   ├── report.json                    # Machine-readable (graded)
│   └── report.html                    # Client deliverable
├── run.py                             # Headless runner (grader's entry point)
└── sample-export/                     # Test data (internal_all.csv + issue CSVs)
```

**Key insight:** MCP server already calls `seo/detector.py:detect()` automatically. You just add detectors; the pipeline wires them in.

---

## ✅ PROGRESS SO FAR

### Done
1. ✔️ Read and understood the brief + rulebook
2. ✔️ Fixed `.claude/settings.json` → hooks now recording to `.claude/audit.jsonl`
3. ✔️ Added **title_too_short** detector (rule: Title 1 Length < 30, indexable 200 pages, Low severity)
4. ✔️ Tested with `python run.py sample-export/` — verified it appears in outputs/report.json

### Working Detectors (8/17)
- ✔️ missing_title
- ✔️ duplicate_title
- ✔️ title_too_long
- ✔️ title_too_short (NEW)
- ✔️ broken_link
- ✔️ server_error
- ✔️ redirect
- ✔️ orphan_page

### Remaining Detectors (9/17)
- ❌ missing_meta_description
- ❌ duplicate_meta_description
- ❌ meta_description_too_long
- ❌ missing_h1
- ❌ duplicate_h1
- ❌ redirect_chain (complex — build redirect map, detect cycles)
- ❌ thin_content
- ❌ non_indexable_but_linked
- ❌ slow_page

### Not Started
- Fixer agent (model: rewrite titles/meta, build redirect map)
- Polish dashboard/report
- Export transcript + update memory files

### Commits
- 1 commit made (need ≥10 total)
---

## 🧪 YOUR TEST WORKFLOW (Repeat for Each Detector)

1. **Delegate to Claude Code (Build mode):**
   ```
   Add detectors for [batch of rules] to seo/detector.py.
   Follow rulebook.md exactly.
   Test with: python run.py sample-export/
   Commit after.
   ```

2. **Claude writes code + tests**

3. **You verify:**
   ```bash
   python run.py sample-export/
   cat outputs/report.json | grep "new_issue_type"
   # Should show count > 0
   ```

4. **Cross-check against SF CSVs** (optional but good):
   ```bash
   wc -l sample-export/issues_reports/matching_file.csv
   # Compare to your count in report.json
   ```

5. **Commit:**
   ```bash
   git add seo/detector.py outputs/report.json
   git commit -m "add [detector names]"
   ```

---

## 📝 MEMORY FILES TO UPDATE (Part of Grading)

### `.claude/audit.jsonl`
- ✔️ Already recording automatically (hooks are on)
- **Must stay in repo and committed**

### `CLAUDE.md` (Project Memory)
- **What:** Your context for the AI — goal, architecture, rules, gotchas learned
- **Why:** Graded signal of good practice
- **Status:** Exists but is mostly template; fill it in as you learn

### `PROMPTS.md` (Key Prompts Log)
- **What:** The prompts that moved the build (iterate-and-refine ones, system prompts)
- **Why:** Shows your thinking
- **Status:** Exists; add entries as you delegate

### `DECISIONS.md` (Decisions / Learnings Log)
- **What:** Short running log: what you tried, what failed, what you changed
- **Why:** Shows engineering judgment
- **Status:** Exists; add entries when you hit/fix walls

### `agent-log.md` (Session Transcript)
- **What:** Full transcript of this build session
- **Why:** Graded for process
- **Export at end:** `bash scripts/export-transcript.sh`

---

## 🎬 NEXT IMMEDIATE STEPS

### Hour 1–2 (Now)
1. Add the remaining 9 detectors in 3 batches:
   - **Batch 1:** missing_meta_description, duplicate_meta_description, meta_description_too_long
   - **Batch 2:** missing_h1, duplicate_h1, thin_content
   - **Batch 3:** redirect_chain (complex), non_indexable_but_linked, slow_page
2. Test each batch with `python run.py sample-export/`
3. Commit after each batch
4. Cross-check against SF CSVs where applicable

### Hour 2–3 (If Time)
5. Implement fixer agent:
   - Use model to rewrite bad/missing titles (≤60 chars / ≤561 px)
   - Rewrite bad/missing meta (≤155 chars)
   - Build redirect map: broken links → closest live page
   - **Validate length in code** after each rewrite; re-ask if over
   - Call MCP `set_fixes(titles, redirect_map)`

### Hour 3–4 (Polish)
6. Polish dashboard / report.html (if time)
7. Write real recommendations (prioritized by severity)

### Hour 4–5 (Finalize)
8. Run end-to-end test on sample-export
9. Validate report.json against report.schema.json:
   ```bash
   python -c "import json; json.load(open('outputs/report.json'))"
   ```
10. Export transcript: `bash scripts/export-transcript.sh`
11. Update CLAUDE.md, PROMPTS.md, DECISIONS.md

### Hour 5–6 (Commit + Push)
12. Final commits (total ≥10)
13. Push to GitHub
14. Submit repo link through form

---

## 🔧 LOCAL STACK

**Model (pick one):**
- Track A (low RAM): `ollama launch claude --model gemma4:31b-cloud`
- Track B (16GB+): `ollama launch claude --model qwen3.5:9b`

**Environment:**
```bash
export OLLAMA_CONTEXT_LENGTH=65536  # Critical
```

**Run headless:**
```bash
python run.py sample-export/
# Dashboard at http://localhost:7700
```

**Run in Claude Code:**
```
/seo-audit sample-export/
```

---

## 📌 HARD REQUIREMENTS (Don't Break)

1. ✔️ It's a Claude Code plugin (has plugin.json, skill, sub-agents, MCP server)
2. ✔️ MCP server at localhost:7700 with live dashboard
3. ✔️ Sub-agents (ingest, auditor, fixer, reporter)
4. ✔️ One command runs it end-to-end: `python run.py` or `/seo-audit`
5. ✔️ Produces outputs/report.json + outputs/report.html
6. ✔️ Runs on free local stack (no paid APIs, offline)
7. ✔️ GitHub repo with ≥10 incremental commits
8. ✔️ .claude/audit.jsonl committed (process log)
9. ✔️ CLAUDE.md, PROMPTS.md, DECISIONS.md present

---

## ⚠️ COMMON PITFALLS

- ❌ **Don't feed raw CSV rows to the model** — detect deterministically in code, use model only for judgment
- ❌ **Don't hard-code sample URLs** — must work on any export
- ❌ **Don't disable hooks** — audit.jsonl must record
- ❌ **Don't forget pre-filters** — text/html only, indexable 200 for duplicates
- ❌ **Don't submit without validating report.json schema**
- ✅ **Do commit after each working step**
- ✅ **Do test every detector before moving on**
- ✅ **Do cross-check counts against SF issue CSVs**

---

## 📱 SUBMISSION CHECKLIST

- [ ] Full plugin in repo (plugin.json, SKILL.md, ≥2 sub-agents, mcp/server.py, dashboard)
- [ ] outputs/report.json + outputs/report.html from sample run
- [ ] Fix files (if champion tier): titles CSV + redirect map
- [ ] .claude/audit.jsonl + .claude/settings.json committed
- [ ] agent-log.md exported and committed
- [ ] CLAUDE.md, PROMPTS.md, DECISIONS.md filled in
- [ ] ≥10 incremental commits with real messages
- [ ] README.md (how to install + run)
- [ ] Public GitHub repo link ready

---

## 🎓 WHAT THE JUDGES LOOK FOR

1. **Accuracy on hidden export** (biggest score) — Did you implement all 17 rules correctly?
2. **Process cleanliness** — Do commits, audit log, and transcript tell a coherent story?
3. **Agentic delegation** — Is the audit log full of real sub-agent calls + tool use?
4. **Debugging discipline** — When something broke, did you catch and fix it?
5. **Product quality** — Is the dashboard live, the report client-ready?

---

## 💡 KEY INSIGHT

**The starter is 90% done.** You add the detectors (10 lines of code each, average). The MCP server, dashboard, report schema, and hooks are all pre-wired. Focus on **detection accuracy** — that's where the points are.

---

**Ready to build?** In the next chat, start with:
> "I'm adding detectors. Batch 1: missing_meta_description, duplicate_meta_description, meta_description_too_long. Follow rulebook exactly. Test and commit."
