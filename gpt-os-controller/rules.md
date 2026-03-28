# AUTO DEBUG YSTEM (SELF-HEALING)

## PURPOSE

Enable GPT-OS to detect, analyze, and fix system errors deterministically.

System does not run loops.

Each debug execution is a single cycle.

## TRIGGERS

- workflow failure detected
- user: debug
- command: debug_system

## DEBUG FLOW (STRICT)

### 1. DETECT FAILURE

API: listWorkflowRuns

use per_page=1
extract run_id
extract conclusion

if not failure stop

### 2. GET EXECUTION DATA

API: listJobsForWorkflowRun
param: run_id

extract jobs
select failed job
extract steps

if no failure stop

### 3. ANALYZE ERROR

extract steps
determine error_type

ALLOWED:
Y-MAL-ERROR
PYTHON-ERROR
PATH-ERROR
MISSING-FILE
SYNTAX-ERROR
UNKNOWN

### 4. FIX STRATEGY

MAP:
 YAML: fix indentation, structure
 PYTHON: fix syntax, imports
 PATH: fix paths
 MISSING: create file
 SYNTAX: fix syntax
 UNKNOWN: stop

### 5. APPLY FIX

API: createOrUpdateFile

RULES:
- fetch SHA
- encode base64
- minimal patch

### 6. REDEPROY

API: rerunWorkflowRun or repositoryDispatch

### 7. VERIFY

API: listWorkflowRuns

check conclusion
if success stop
if failure wait for next cycle

## SAFETY

- no loops
- no retries
- preserve structure
- no deletes

## PRIORITY 

- debug has high priority
- but respects user commands

## FINAL RULE

System is self healing by executions, not loops
