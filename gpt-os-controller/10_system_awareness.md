# SYSTEM AWARENESS (STATE-AWARE EXECUTION)

## PURPOSE

Defines how GPT-OS understands system state using memory.

System is STATELESS by default.
State is restored via memory.

---

## MEMORY STRUCTURE

memory/
├── debug/          # errors per run
├── session/        # history per event
└── source_of_truth.json  # global state

---

## SOURCE OF TRUTH (SOT)

SOT is the ONLY source of system state.

GPT MUST:
- ALWAYS read memory/source_of_truth.json BEFORE any response
- NEVER assume state
- NEVER ignore debug_runs

---

## GPT MEMORY BOOT PROTOCOL (MBP)

Every request:

1. LOAD SOT (API)
2. PARSE STATE
3. DETECT MODE
4. LOAD CONTEXT
5. RESPOND

---

## MODE DETECTION

if debug_runs > 0:
    mode = "DEBUG"
elif sessions > 0:
    mode = "CONTINUE"
else:
    mode = "INIT"

Priority:
DEBUG > CONTINUE > INIT

---

## CONTEXT LOADING

DEBUG:
→ load memory/debug/run_<latest>.json

CONTINUE:
→ load memory/session/session_<latest>.json

INIT:
→ no memory

---

## INTERNAL STATE

context = {
  "mode": mode,
  "repo_state": ...,
  "last_error": ...,
  "last_action": ...
}

---

## RESPONSE STRATEGY

DEBUG:
"Ostatni run zakończył się błędem. Naprawić?"

CONTINUE:
"Kontynuujemy ostatnie zadanie?"

INIT:
"System gotowy. Co robimy?"

---

## HARD RULES

- ALWAYS read SOT before response
- NEVER guess state
- NEVER ignore debug_runs
- NEVER reset if data exists

---

## FINAL MODEL

GPT = stateless engine
+
memory (SOT) = state
=
STATEFUL SYSTEM
