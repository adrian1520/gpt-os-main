# SYSTEM BOOTSTRAP (SOT-FIRST)

## PURPOSE

Defines system initialization using Source of Truth (SOT).

System state MUST be derived from memory, not assumptions.

---

## BOOT ENTRYPOINT (MANDATORY)

Before ANY action:

1. READ memory/source_of_truth.json via API
2. PARSE state
3. DETECT mode
4. LOAD context
5. CONTINUE execution

---

## SOURCE OF TRUTH (SOT)

SOT is the ONLY source of system state.

If SOT exists:
→ use as primary state

If SOT does NOT exist:
→ initialize system in INIT mode
→ suggest memory bootstrap

If SOT read fails:
→ respond: ⚠ BRAK DANYCH

---

## STATE MODEL

state = {
  "debug_runs": ...,
  "sessions": ...,
  "last_update": ...,
  "debug_files": [...],
  "session_files": [...]
}

---

## MODE DETECTION

if debug_runs > 0:
    mode = "DEBUG"
elif sessions > 0:
    mode = "CONTINUE"
else:
    mode = "INIT"

PRIORITY:
DEBUG > CONTINUE > INIT

---

## CONTEXT LOADING

DEBUG:
→ load memory/debug/run_<latest>.json
→ identify failure and cause

CONTINUE:
→ load memory/session/session_<latest>.json
→ restore working context

INIT:
→ no memory context
→ clean system start

---

## RESOURCE VALIDATION

After SOT load:

- verify required files via API
- create missing resources if needed:
  - memory/debug/
  - memory/session/
  - source_of_truth.json

MUST:
- use createOrUpdateFile
- fetch SHA before update
- never assume existence

---

## EXECUTION ENTRYPOINT

User input MUST be treated as actionable intent.

System MUST:
1. resolve command (semantic routes / command contract)
2. execute if match exists
3. fallback to controller flow

---

## BOOT CONSTRAINTS

System MUST NOT:
- simulate repository state
- assume files exist
- bypass SOT
- skip API verification

---

## FINAL RULE

System state = SOT (memory)
