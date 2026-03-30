# ASYNC DISPATCH MODE (SOT + GOVERNOR + INTERPRETER ENFORCED)

## PURPOSE

Enable GPT-OS to handle asynchronous task execution via repository-driven workflows.

GPT DOES NOT execute tasks.
GitHub Actions execute tasks.

---

## SOT INTEGRATION (MANDATORY)

Before dispatch:

- MUST read SOT
- MUST detect mode

RULE:

IF mode == DEBUG:
→ DO NOT dispatch new tasks
→ PRIORITIZE debug_system

---

## GOVERNOR ENFORCEMENT

ALL dispatch operations MUST pass through governor.

Governor may:
- block dispatch
- delay dispatch
- limit task count

IF blocked:
→ STOP

---

## CORE PRINCIPLE

GPT:
- creates tasks (RAW only)
- triggers execution

GitHub Actions:
- process tasks
- handle parallel execution
- manage concurrency

---

## TASK DISPATCH

Tasks MUST be written to:

memory/queue/

Using API:
createOrUpdateFile

---

## TASK FORMAT (CRITICAL)

Tasks MUST contain RAW content only.

FORBIDDEN:
- base64 encoding by GPT
- formatted payloads

Encoding:
→ handled by interpreter layer in workflow

---

## TASK ID

task_id MUST include:
- timestamp
- session_id
- operation type

Example:
task_20260330_write_config.json

---

## EXECUTION TRIGGER

API:
repositoryDispatch

event_type:
- process_queue

---

## WORKFLOW RESPONSIBILITY

GitHub Actions MUST:
- read queue
- process tasks
- manage parallel execution
- handle locking
- avoid conflicts
- use interpreter layer for writes

GPT is NOT responsible for:
- locking
- concurrency
- worker coordination

---

## LIMITS (ENFORCED)

MAX:
- tasks per cycle: 5

---

## RESULT HANDLING

Results stored in:

memory/results/

GPT MAY read using:
getFileContent

---

## FAILURE HANDLING

If task fails:

→ mark as failed
→ MUST execute debug_system

---

## FINAL RULE

GPT dispatches.
Workflows execute.
