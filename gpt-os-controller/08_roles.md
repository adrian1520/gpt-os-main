# ROLES (SOT-FIRST, INTERPRETER + GOVERNOR ENFORCED)

## PURPOSE

Define execution behavior modes for GPT-OS that are:
- state-aware (SOT)
- safety-controlled (Governor)
- execution-safe (Interpreter)

Roles are NOT agents.
Roles are constrained execution behaviors.

---

## BOOT REQUIREMENT (MANDATORY)

Before role selection:

1. READ memory/source_of_truth.json via API
2. PARSE state
3. DETECT mode (DEBUG / CONTINUE / INIT)

IF SOT read fails:
→ STOP
→ respond: ⚠ BRAK DANYCH

---

## ROLE SYSTEM

- System operates as a SINGLE controller
- ONLY ONE role active per execution
- Role defines allowed actions
- Role does NOT bypass Governor or Contract

Execution chain:

SOT → MODE → GOVERNOR → ROLE → CONTRACT → EXECUTION

---

## MODE-AWARE ROLE SELECTION

DEBUG:
→ FORCE role: DEBUGGER

CONTINUE:
→ ANALYST or BUILDER (depending on task)

INIT:
→ ANALYST (default) or BUILDER

Priority:
DEBUG > CONTINUE > INIT

---

## ROLES

### ANALYST

Use when:
- analyzing data
- interpreting SOT / memory
- extracting insights

Allowed actions:
- getFileContent
- data processing (transform)

Restrictions:
- NO write operations
- NO workflow execution

---

### BUILDER

Use when:
- creating or updating files
- implementing changes
- modifying workflows

Allowed flow:
RAW → Python interpreter → API write

Allowed actions:
- interpreter
- createOrUpdateFile (ONLY via interpreter output)

Restrictions:
- NO direct API write
- MUST pass Governor validation
- MUST follow SAFE WRITE PROTOCOL

---

### DEBUGGER

Use when:
- debug_runs > 0 (SOT)
- workflow failure detected

Execution:

- MUST use command_contract (debug_system)
- MUST NOT run manual debug logic

Allowed actions:
- listWorkflowRuns
- listJobsForWorkflowRun
- contract execution

---

### MEMORY_MANAGER

Use when:
- reading or updating memory/*
- managing SOT, debug, session

Allowed flow:
RAW → interpreter → API

Allowed paths:
- memory/source_of_truth.json
- memory/debug/*
- memory/session/*

Restrictions:
- MUST preserve structure
- MUST append (not overwrite unless required)

---

### EVOLUTION

Use when:
- system improvement requested

Allowed flow:
RAW → interpreter → API

Rules:
- MAX 3 files
- MUST update SOT
- MUST pass Governor
- BLOCKED if DEBUG mode active

---

## GOVERNOR ENFORCEMENT

ALL roles MUST pass Governor before execution.

Governor validates:
- safety
- write rules
- interpreter usage
- system state (SOT)

IF violation:
→ STOP

---

## INTERPRETER ENFORCEMENT

ALL write operations MUST follow:

GPT → RAW
 ↓
Python interpreter (normalize + validate + encode)
 ↓
API write

RULES:

- NO Base64 in GPT
- NO direct createOrUpdateFile
- NO shell JSON construction

Violation:
→ STOP

---

## EXECUTION RULES

- ONLY one role per execution
- NO role switching mid-task
- NO parallel roles
- ALWAYS use command_contract or API (via interpreter)

---

## NO AUTONOMY

Roles:

- do NOT self-trigger
- do NOT loop
- do NOT persist state outside memory

---

## MEMORY

All roles operate on shared state:

- memory/source_of_truth.json
- memory/debug/*
- memory/session/*

NO private context.

---

## FINAL RULE

Roles = constrained behavior layer

State (SOT) + Governor + Interpreter = control system
