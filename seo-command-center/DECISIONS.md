# DECISIONS.md — decision & learnings log

A short running note of the real choices you made: what you tried, what failed and why, what
you changed. This is your engineering judgement on the record — it is what separates a builder
from a button-presser, and it is graded (challenge brief section 08).

Append a 1–2 line entry whenever you make a real decision or hit/fix a wall. Add a timestamp.

Format:
`[HH:MM] <decision or problem> → <what you did and why>`

---

## Example (replace with your own)
- `[10:20]` Chose plain-csv parsing over pandas → fewer deps, fast enough for 5k rows, model
  quota saved for the fixer.
- `[11:05]` Title detector over-counted duplicates → realized non-indexable pages were
  included; added an indexable+200 filter (per rulebook).
- `[12:40]` Dashboard wasn't updating live → MCP tool wasn't emitting the SSE event; added
  `_emit("issue", row)` in extract.

---

## My log
- [14:28] Added titles_too_short detector. tested with python run.py command to check if its working.
- [15:08] Added 3 meta detectors (batch 1) → pattern: filter indexable+200, dedupe on key.
- [15:23] Added and tested h1 + thin_content detectors (batch 2).
- [15:26] Added and tested remaining 3 detectors (batch 3).
- [15:50] Found a bug in redirect chain detector. Moving forward to first implement the fix agent. 
- [15:59] Fixer agent isn't implemented by model. it gave a simulator code.
- [16:29] Explained the detailed purpose of fixer agent and told to integrate with MCP pipeline
- [16:41] Integrated and validate the fixer agent code.
- [16:50] Found a bug with fixer agent. still uses simulated data.
- [16:58] Fixed fixer agent. noe using real data
- [] 

