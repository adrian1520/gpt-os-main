# COMMAND MAPPING (SOT-FIRST, INTERPRETER COMPLIANT)

## PURPOSE

Defines deterministic routing between user intent, command_contract, and API execution with full SOT awareness.

---

## BOOT REQUIREMENT (MANDATORY)

Before ANY command resolution:

1. READ memory/source_of_truth.json via API
2. PARSE state
3. DETECT mode (DEBUG / CONTINUE / INIT)

IF SOT read fails:
→ STOP
→ respond: ⚠ BRAK DANYCH

---

## EXECUTION RULE

All commands MUST map to:
- command_contract (preferred)
- or direct API call (only if safe and deterministic)

DO NOT interpret commands manually.

---

## MODE-AWARE ROUTING

System MUST respect mode:

DEBUG:
→ prioritize debug_system

CONTINUE:
→ resume last session context

INIT:
→ normal routing

Priority:
DEBUG > CONTINUE > INIT

---

## MEMORY OPERATIONS (SOT-FIRST)

### READ SOT

Command:
read_sot

API:
getFileContent

Path:
memory/source_of_truth.json

---

### READ DEBUG

Command:
read_debug

API:
getFileContent

Path:
memory/debug/run_<latest>.json

---

### READ SESSION

Command:
read_session

API:
getFileContent

Path:
memory/session/session_<latest>.json

---

### UPDATE MEMORY

Command:
update_memory

FLOW:
RAW → Python interpreter → API write

Paths:
- memory/source_of_truth.json
- memory/debug/*
- memory/session/*

RULES:
- MUST follow SAFE WRITE PROTOCOL
- MUST append, not overwrite (unless required)

---

## PROJECT MANAGEMENT

### SAVE PROJECT

Command:
save_project

FLOW:
- read SOT + memory
- construct deterministic snapshot
- write via interpreter layer

Path:
memory/projects/<name>.json

---

### LOAD PROJECT

Command:
load_project

FLOW:
- read project file
- update memory via interpreter

---

### LIST PROJECTS

Command:
list_projects

API:
listRepositoryContents

Path:
memory/projects/

---

## WORKFLOW OPERATIONS

### RUN ANALYSIS

Command:
run_analysis

API:
repositoryDispatch

event_type:
run_analysis

---

## DEBUG SYSTEM

Command:
debug_system

FLOW:
- delegate to command_contract (debug_system)
- execution handled via interpreter + memory write-back

NO manual debug logic in mapping layer.

---

## FILE OPERATIONS (INTERPRETER ONLY)

### READ FILE

Command:
read_file

API:
getFileContent

---

### WRITE FILE

Command:
write_file

FLOW:
RAW → Python interpreter → API write

RULES:
- NO direct createOrUpdateFile from GPT
- MUST use interpreter layer

---

### DELETE FILE

Command:
delete_file

API:
deleteFile

---

## SYSTEM STATUS

Command:
check_status

FLOW:
- read SOT
- optionally verify via listWorkflowRuns

RETURN:
- system state
- last execution status

---

## RULES

- ALWAYS use exact path
- ALWAYS use API
- ALWAYS validate before write
- ALWAYS use interpreter for writes
- NEVER simulate
- ALWAYS follow command_contract
- STOP after execution

---

## FINAL RULE

Routing MUST be deterministic, state-aware, and interpreter-compliant.
