# AUTO DEBUG SYSTEM (SOT-AWARE, SELF-HEALING)

## PURPOSE

Enable GPT-OS to detect, analyze, and fix system errors deterministically with full memory awareness.

System does NOT run loops.
Each debug execution is a single cycle.

---

## BOOT REQUIREMENT (MANDATORY)

Before debug:

1. READ memory/source_of_truth.json via API
2. PARSE state
3. DETECT mode

IF SOT read fails:
→ STOP
→ respond: ⚠ BRAK DANYCH

---

## MODE PRIORITY

IF mode == DEBUG:
→ debug_system has PRIORITY

Priority:
DEBUG > CONTINUE > INIT

---

## TRIGGERS

- workflow failure detected
- user: "debug"
- command: debug_system

---

## DEBUG FLOW (STRICT)

### 1. DETECT FAILURE

API:
listWorkflowRuns

→ use per_page=1  
→ extract workflow_runs[0].id as run_id  
→ extract workflow_runs[0].conclusion  

→ if conclusion != "failure":
   → STOP  

---

### 2. GET EXECUTION DATA

API:
listJobsForWorkflowRun

params:
- run_id: ${run_id}

→ extract jobs  
→ select job where conclusion == "failure"  
→ if none:
   → STOP  

→ extract steps from job.steps

---

### 3. ANALYZE ERROR (DETERMINISTIC)

Input: steps  
Output: error_type  

Allowed:
- YAML_ERROR  
- PYTHON_ERROR  
- PATH_ERROR  
- MISSING_FILE  
- SYNTAX_ERROR  
- UNKNOWN_ERROR  

NO free reasoning.

---

### 4. FIX STRATEGY

YAML_ERROR:
- fix indentation
- remove quotes from "on:"
- validate structure

PYTHON_ERROR:
- fix imports
- fix syntax
- fix paths

PATH_ERROR:
- correct paths

MISSING_FILE:
- create required file

SYNTAX_ERROR:
- fix syntax

UNKNOWN_ERROR:
→ STOP

---

### 5. APPLY FIX (INTERPRETER LAYER)

RULES:
- NO direct Base64
- USE Python (prepare_content.py)
- ALWAYS fetch SHA before write
- ALWAYS minimal patch

FLOW:

RAW → Python normalize → encode → API write

---

### 6. MEMORY WRITE-BACK (MANDATORY)

After fix attempt:

- create memory/debug/run_<id>.json
- include:
  - run_id
  - error_type
  - affected_files
  - status

- update memory/source_of_truth.json:
  - increment debug_runs
  - append debug_files

---

### 7. REDEPLOY

API:
rerunWorkflowRun
or repositoryDispatch

---

### 8. VERIFY

API:
listWorkflowRuns

IF success:
→ STOP

IF failure:
→ require new debug execution

---

## SAFETY RULES

- NO loops  
- NO retries inside GPT  
- NO full overwrite unless required  
- PRESERVE structure  
- DO NOT delete critical files  

---

## FINAL RULE

System is self-healing via stateful iterations (memory), not loops.
