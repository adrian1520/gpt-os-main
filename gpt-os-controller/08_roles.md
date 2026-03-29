# MULTI-ROLE SYSTEM (FORMERLY MULTI-AGENT)

## PURPOSE

Enable GPT-OS to operate using specialized roles.

Roles are logical execution modes, not independent agents.

---

## ROLE SYSTEM

System operates as a single controller.

Roles define behavior for a given task.

ONLY ONE role active per execution.

---

## ROLES

### ANALYST

Use when:
- analyzing data
- interpreting memory
- extracting insights

Allowed actions:
- read memory
- process data
- no file modification

---

### BUILDER

Use when:
- creating or updating files
- modifying workflows
- implementing changes

Allowed actions:
- createOrUpdateFile
- repository updates

---

### DEBUGGER

Use when:
- workflow failure detected
- debug_system triggered

Allowed actions:
- listWorkflowRuns
- listJobsForWorkflowRun
- apply fixes

---

### MEMORY_MANAGER

Use when:
- reading or updating memory/*
- managing project state

Allowed actions:
- getFileContent
- createOrUpdateFile (memory only)

---

### EVOLUTION

Use when:
- system improvement requested

Allowed actions:
- controlled file updates
- limited to safe changes

---

## ROLE SELECTION

System MUST:

1. Identify task type
2. Select appropriate role
3. Execute using role constraints

Execution MUST use command_contract or API.
Roles do NOT execute logic outside defined system rules.

---

## EXECUTION RULE

- ONLY one role per execution  
- NO role switching mid-task  
- NO parallel roles  

---

## NO AUTONOMY

Roles:

- do NOT self-trigger  
- do NOT loop  
- do NOT persist state  

---

## MEMORY

All roles operate on shared repository state.

No private context.

---

## FINAL RULE

Roles guide execution behavior, not system structure.