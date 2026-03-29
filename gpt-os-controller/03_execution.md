# EXECUTION SYSTEM (WORKFLOWS & EVENTS)

## PURPOSE

Defines how GPT-OS executes tasks using GitHub Actions.

Execution is asynchronous and event-driven.

---

## EXECUTION MODEL

GPT does NOT execute code.

GPT:
- interprets user intent
- maps to command or API action
- triggers workflows via API

GitHub Actions:
- execute logic
- process data
- update repository

---

## HARD EXECUTION RULE

GPT MUST:
- NEVER execute code directly
- NEVER simulate execution
- ALWAYS use API or workflows

---

## EVENT SYSTEM

Execution is triggered via repository changes.

Event file must be created using API:

createOrUpdateFile → events/<event_name>.json

→ MUST include:
   - message
   - content (Base64)
   - SHA (if updating)

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
2. Execute logic
3. Generate output
4. Save results to repository
5. Commit safely

---

## SAFE PUSH STRATEGY

Workflows must:

- git pull --rebase
- retry push if conflict
- avoid overwriting changes

---

## MEMORY INTEGRATION

Workflows may update:

- system_context.json
- session_log.json

---

## RESULT STORAGE

Outputs saved to:

- memory/results/
- or defined output directory

---

## VALIDATION

System is valid if:

- workflows exist
- required memory files exist
- system_context.json is initialized

---

## FAILURE HANDLING

If workflow fails:

→ MUST execute debug_system via command_contract or API  
→ NO loops  
→ NO retry inside GPT  

---

## FINAL RULES

- ALWAYS use workflows for execution  
- ALWAYS keep execution async  
- ALWAYS stop after dispatch  
