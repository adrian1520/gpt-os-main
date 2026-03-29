## API ACCESS

System has access to ALL endpoints defined in OpenAPI schema.

GPT MAY use any endpoint when required,
even if not explicitly listed in this mapping.

# COMMAND + API MAPPING

## EXECUTION RULE

All commands MUST map to:
- command_contract
- or direct API call

DO NOT interpret commands manually.

---

## MEMORY OPERATIONS

### READ MEMORY

Command:
read_memory

API:
getFileContent

Paths:
- memory/system_context.json
- memory/session_log.json

---

### LOAD CONTEXT

Command:
load_context

API:
getFileContent

Path:
memory/context_bundle.json

---

### UPDATE MEMORY

Command:
update_memory

API:
createOrUpdateFile

Path:
memory/*

---

## PROJECT MANAGEMENT

### SAVE PROJECT

Command:
save_project

Required steps:
- read memory files
- construct snapshot (deterministic)
- write to memory/projects/<name>.json

API:
- getFileContent
- createOrUpdateFile

---

### LOAD PROJECT

Command:
load_project

Required steps:
- read project file
- overwrite memory files

API:
- getFileContent
- createOrUpdateFile

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

### DEBUG SYSTEM

Command:
debug_system

Flow:
1. listWorkflowRuns
2. listJobsForWorkflowRun
3. delegate to command_contract (debug_system)
4. apply fix via contract execution
5. createOrUpdateFile

---

## FILE OPERATIONS

### READ FILE

Command:
read_file

API:
getFileContent

---

### WRITE FILE

Command:
write_file

API:
createOrUpdateFile

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

Flow:
- listWorkflowRuns
- extract latest run
- return status

---

## RULES

- ALWAYS use exact path
- ALWAYS use API
- ALWAYS validate before write
- NEVER simulate
- ALWAYS follow command_contract
- STOP after execution