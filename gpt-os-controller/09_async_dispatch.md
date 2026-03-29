# ASYNC DISPATCH MODE (FORMERLY PARALLEL EXECUTION)

## PURPOSE

Enable GPT-OS to handle asynchronous task execution via repository-driven workflows.

GPT does NOT manage parallel execution.

Parallelism is handled by GitHub Actions.

---

## CORE PRINCIPLE

GPT:

- creates tasks
- triggers execution

GitHub Actions:

- process tasks
- handle parallel execution
- manage concurrency

---

## TASK DISPATCH

Tasks MAY be written to:

memory/queue/

Using API:
createOrUpdateFile

Example:
memory/queue/task_<id>.json

---

## EXECUTION TRIGGER

API:
repositoryDispatch

event_type:
process_queue

---

## WORKFLOW RESPONSIBILITY

GitHub Actions MUST:

- read queue
- process tasks
- manage parallel execution
- handle locking
- avoid conflicts

GPT is NOT responsible for:

- locking
- concurrency
- worker coordination

---

## RESULT HANDLING

Results stored in:

memory/results/

GPT MAY read results using:
getFileContent

---

## FAILURE HANDLING

If task fails:

→ mark as failed  
→ MUST execute debug_system via command_contract or API  

---

## GOVERNOR CONSTRAINTS

- avoid conflicting writes  
- prefer sequential updates when modifying same files  
- do not dispatch excessive tasks  

---

## ROLE IN SYSTEM

This module defines dispatch strategy, not execution logic.

Execution logic remains in:
- command_contract
- workflows

---

## FINAL RULE

GPT dispatches.  
Workflows execute.