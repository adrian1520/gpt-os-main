# SYSTEM AWARENESS (CONTEXT-AWARE EXECUTION)

## PURPOSE

Enable GPT-OS to make decisions based on current repository state.

System awareness is request-based, not continuous.

---

## CONTEXT PRINCIPLE

GPT does NOT maintain global state.

GPT MUST:

- read required context via API
- use only current data
- avoid assumptions

---

## CONTEXT SOURCES

Use ONLY when relevant:

- system_context.json
- session_log.json
- case_memory.json
- workflow runs
- specific files

DO NOT load all data by default.

---

## STATE EVALUATION

System state is inferred dynamically from:

- latest workflow runs
- memory files
- current task

NO persistent state model required.

---

## DECISION RULE

Before action, GPT MAY:

- read required files
- check latest workflow status
- verify task relevance

ONLY if needed.

---

## PRIORITY ENGINE

Order:

1. CRITICAL (system failure)
2. DEBUG (failures)
3. EXECUTION (user tasks)
4. EVOLUTION (improvements)

---

## CONFLICT AVOIDANCE

Before write:

- verify file via getFileContent
- use latest SHA
- avoid duplicate operations

No implicit conflict detection.

---

## SYSTEM HEALTH (INFERRED)

OK:
- latest workflow success

DEGRADED:
- recent failures

CRITICAL:
- repeated failures

Based on workflow data only.

---

## RESPONSE STRATEGY

IF CRITICAL:
â MUST execute debug_system via command_contract or API  

IF DEGRADED:
â MUST prioritize execution of debug_system  

IF OK:
â proceed with execution  

---

## MEMORY USAGE

- always prefer latest data  
- avoid stale reads  
- reload when required  

---

## FINAL RULE

System awareness = read â decide â act (single cycle)

No loops. No persistent awareness.