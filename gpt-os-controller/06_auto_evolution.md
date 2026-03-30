# AUTO EVOLUTION SYSTEM (SOT-FIRST, INTERPRETER COMPLIANT)

## PURPOSE

Enable GPT-OS to improve and extend system safely via controlled, state-aware changes.

System does NOT evolve automatically.

Evolution is always single-cycle and user-triggered.

---

## BOOT REQUIREMENT (MANDATORY)

Before ANY evolution:

1. READ memory/source_of_truth.json via API
2. PARSE state
3. DETECT mode (DEBUG / CONTINUE / INIT)

IF SOT read fails:
→ STOP
→ respond: ⚠ BRAK DANYCH

---

## MODE PRIORITY

DEBUG > CONTINUE > INIT

IF mode == DEBUG:
→ MUST execute debug_system first
→ evolution blocked until system is stable

---

## TRIGGERS

- user: "ulepsz system"
- user: "rozwiń system"
- explicit system improvement request

---

## EVOLUTION FLOW (STRICT)

### 1. ANALYZE TARGET

Read ONLY required files via API:

- memory/source_of_truth.json
- relevant module(s)
- related workflows (if needed)

NO blind full-repo scan.

---

### 2. DEFINE CHANGE

Improvement MUST be:

- explicit
- minimal
- deterministic

Allowed:

- FIX → bug repair  
- OPTIMIZE → performance improvement  
- EXTEND → new capability  
- REFACTOR → structure cleanup  

---

### 3. PLAN PATCH

Define:

- target file(s)
- exact modification
- expected effect

NO abstract planning.

---

### 4. APPLY CHANGE (INTERPRETER LAYER)

FLOW:

RAW → Python interpreter → API write

RULES:

- NO direct Base64 encoding
- MUST use interpreter (prepare_content.py)
- ALWAYS fetch fresh SHA
- ALWAYS minimal diff

---

### 5. MEMORY UPDATE (MANDATORY)

After change:

Update memory/source_of_truth.json:

- last_update
- last_evolution
- change_summary

OPTIONAL:

- write session log → memory/session/
- write debug info → memory/debug/ (if needed)

RULES:

- append, not overwrite
- preserve structure
- deterministic updates

---

### 6. DEPLOY

API:

- repositoryDispatch  
or  
- workflow trigger  

---

### 7. VERIFY

API:
listWorkflowRuns  

Check:

- workflow success  
- system stability  

IF failure:

→ STOP  
→ MUST execute debug_system  

---

## SAFETY RULES

- MAX 3 files per evolution  
- NEVER modify prompt.md automatically  
- NEVER delete system-critical files  
- ALWAYS preserve bootability  
- ALWAYS follow SAFE WRITE PROTOCOL  

---

## EXECUTION RULE

Evolution MUST:

- use command_contract if available
- otherwise use deterministic API execution

NO manual unsafe operations.

---

## FINAL RULE

Evolution = controlled, state-aware mutation

NOT autonomous behavior.
