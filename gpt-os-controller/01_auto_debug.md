# AUTO DEBUG SYSTEM (SELF-HEALING)

## PURPOSE

Enable GPT-OS to detect, analyze, and fix system errors deterministically.

System does NOT run loops.

Each debug execution is a single cycle.

---

## TRIGGERS

- workflow failure detected
- user: "debug"
- command: debug_system

---

## DEBUG FLOW (STRICT)

### 1. DETECT FAILURE

API:
listWorkflowRuns

→ use per_page=1  
→ extract workflow_runs[0].id as run_id  
→ extract workflow_runs[0].conclusion  

→ if conclusion != "failure":
   → STOP (no failure) 

---
- 

### 2. GET EXECUTION DATA

API:
listJobsForWorkflowRun

params:
- run_id: ${run_id}

→ extract jobs  
→ select job where conclusion == "failure"  
→ if none:
   → STOP (no failure detected)  

→ extract steps from job.steps

---

### 3. ANALYZE ERROR (DETERMINISTIC)

Use transform:

Input:
steps

Output:
error_type

Allowed types:

- YAML_ERROR  
- PYTHON_ERROR  
- PATH_ERROR  
- MISSING_FILE  
- SYNTAX_ERROR  
- UNKNOWN_ERROR  

NO free reasoning.

---

### 4. FIX STRATEGY (MAPPED)

Error must map to fix:

YAML_ERROR:
- fix indentation
- remove quotes from "on:"
- validate structure

PYTHON_ERROR:
- fix imports
- fix syntax
- fix paths

PATH_ERROR:
- correct file paths

MISSING_FILE:
- create required file

SYNTAX_ERROR:
- fix syntax

UNKNOWN_ERROR:
→ STOP (no unsafe fix)

---

### 5. APPLY FIX

API:
createOrUpdateFile

RULES:
- ALWAYS fetch SHA first  
- ALWAYS encode Base64  
- ALWAYS minimal patch  

---

### 6. REDEPLOY

API:
rerunWorkflowRun  
or  
repositoryDispatch  

---

### 7. VERIFY

API:
listWorkflowRuns

→ check latest conclusion  

IF success:
→ STOP  

IF failure:
→ require new debug execution (no loop)  

---

## SAFETY RULES

- NO loops  
- NO automatic retries  
- NO full file overwrite unless required  
- PRESERVE structure  
- DO NOT delete critical files  

---

## PRIORITY

If failure detected:

→ debug_system has HIGH priority  
→ but does NOT override explicit user commands  

---

## FINAL RULE

System is self-healing via repeated executions, not loops.