# EXECUTION SYSTEM (SOT-FIRST, INTERPRETER COMPLIANT)

## PURPOSE

Defines how GPT-OS executes tasks using GitHub Actions with full SOT and interpreter layer compliance.

Execution is asynchronous and event-driven.

---

## BOOT DEPENDENCY (MANDATORY)

Execution MUST rely on system bootstrap:

1. READ memory/source_of_truth.json via API
2. DETECT mode (DEBUG / CONTINUE / INIT)

Execution MUST NOT proceed without SOT.

IF SOT read fails:
→ STOP
→ respond: ⚠ BRAK DANYCH

---

## EXECUTION MODEL

GPT does NOT execute code.

GPT:
- interprets user intent
- maps to command or API action
- generates RAW payload only
- triggers workflows via API

GitHub Actions:
- execute logic
- process data
- update repository
- update memory (SOT, debug, session)

---

## HARD EXECUTION RULE

GPT MUST:
- NEVER execute code directly
- NEVER simulate execution
- NEVER perform final writes
- ALWAYS use API or workflows

---

## EVENT SYSTEM (INTERPRETER COMPLIANT)

Execution is triggered via repository changes.

Event file MUST be created via API:

createOrUpdateFile → events/<event_name>.json

Event payload MUST contain RAW content only:

{
  "target": "...",
  "content": "...",
  "meta": {...}
}

RULES:
- NO Base64 in GPT layer
- NO JSON construction in shell
- payload MUST be clean and minimal

---

## WORKFLOW TRIGGER

Workflows listen to:

on:
  push:
    paths:
      - 'events/**'

---

## DISPATCH

Alternative trigger:

repositoryDispatch

Example:
event_type: run_analysis

---

## WORKFLOW FLOW

1. Read event payload
2. Pass content to Python interpreter
3. Normalize + validate + encode
4. Execute logic
5. Save results to repository
6. Update memory (SOT / debug / session)
7. Commit safely

---

## INTERPRETER LAYER (ENFORCED)

ALL writes MUST go through Python layer:

Python (tools/prepare_content.py):
- normalize content
- validate formatting
- encode Base64

API:
- receives ONLY validated content

---

## WRITE PIPELINE (MANDATORY)

GPT → RAW  
↓  
Python (normalize + validate + encode)  
↓  
API write  

---

## MEMORY INTEGRATION (SOT-FIRST)

Workflows MUST update:

- memory/source_of_truth.json (primary state)
- memory/debug/ (on failure)
- memory/session/ (on execution)

RULES:
- ALWAYS follow SAFE WRITE PROTOCOL
- NEVER overwrite full structure unless required
- ALWAYS append state changes

---

## SAFE PUSH STRATEGY

Workflows MUST:

- git pull --rebase
- retry push if conflict
- avoid overwriting changes

---

## VALIDATION

System is valid if:

- workflows exist
- memory/source_of_truth.json exists
- memory/debug and memory/session exist

---

## FAILURE HANDLING

If workflow fails:

→ MUST trigger debug_system  
→ NO loops  
→ NO retry inside GPT  

---

## FINAL RULES

- ALWAYS use workflows for execution  
- ALWAYS keep execution async  
- ALWAYS stop after dispatch  

---

## CRITICAL RULE

NO direct write from GPT.

System execution = workflows + interpreter + memory (SOT)
