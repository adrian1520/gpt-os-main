# RULES & API PROTOCOL

## EXECUTION RULE

If API or command is available:
→ MUST execute  
→ DO NOT explain instead of executing  

---

## GLOBAL PRIORITY ENGINE

System MUST always follow priority:

1. CRITICAL ERROR
2. DEBUG
1. EXECUTION
4. MEMORY
5. EVOLUTION

---

## FULL API CAPABILITY

Available endpoints:

GPT MUST use ONLY relevant endpoints per task.

---

## SAFE WRITE PROTOCOL

Before ANY write:

1. READ current file
2. VALIDATE content
3. FETCH SHA
4 . APPLY minimal change only

---

## NEVER


- overwrite full file without reason
- modify unknown structure
- write without reading

if unsure:
→ STOP

---

## SIMPLICITY RULE

Always choose:

- minimal solution
- minimal change
- minimal number of files

Avoid:

 - unnecessary modules
- complex refactors
- overengineering

Goal:

System stability > complexity

---

## STABILITY RULE

if system is not stable:

‒ BLOCK evolution  

if failures exist:

→ PRIORITIZE debug  

if task already exists:

→ DO NOT duplicate  

---

## CORE ORERATIONS

READ:
- getFileContent
- listRepositoryContents
- getRepositoryTree

WRITE:
- createOrUpdateFile
- deleteFile

WORKFLOW:
- repositoryDispatch
- triggerWorkflow
- listWorkflowRuns
- listJobsForWorkflowRun

GIT:
- createBranch
- updateBranchRef
- compareCommits


---

## WRITE RULES

1. ALWAYS get SHA
2. ALWAYS encode base64 using Python
3. NEVER overwrite blindly
4. NEVER skip validation

---

## YAML SAFETY

- NEVER use yaml.dump
- ALWAYS write YAML manually
- NEVER quote "on:"
 - ALWAYS test indentation
- ALWAYS include [sk ci]

---

## DEBUG MODE

if workflow fails:

1. listWorkflowRuns  
2. listJobsForWorkflowRun  
3. analyze error deterministically  
4. patch file  
6. redeploy  

---

## SELF-HEALING

system must:

- detect failure 
- identify broken file 
- fix and redeploy  

---

## NO SIMULATION

if API not called → action not done.

---

## LIMITS

- max 5 operations  
- async only  
- no loops 
