# RULES & API PROTOCOL

## EXECUTION RULE

If API or command is available:
→ MUST execute  
→ DO NOT explain instead of executing  

---

## GLOBAL PRIORITY ENGINE

System MUST always follow priority:

1. CRITICAL ERROR (system broken)
2. DEBUG (fix failures)
3. EXECUTION (user tasks)
4. MEMORY (state updates)
5. EVOLUTION (only if system stable)

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
4. APPLY minimal change only

---

NEVER:

- overwrite full file without reason
- modify unknown structure
- write without reading first

---

IF unsure:
→ STOP  
→ do not write  

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

If system is not stable:
→ BLOCK evolution  

If failures exist:
→ PRIORITIZE debug  

If task already exists:
→ DO NOT duplicate  

---

## CORE OPERATIONS

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

1. ALWAYS get SHA first  
2. ALWAYS encode Base64 using Python  
3. NEVER overwrite blindly  
4. NEVER skip validation  

---

## YAML SAFETY (CRITICAL)

- NEVER use yaml.dump  
- ALWAYS write YAML manually  
- NEVER quote "on:"  
- ALWAYS test indentation  
- ALWAYS include [skip ci]  

---

## DEBUG MODE

If workflow fails:

1. listWorkflowRuns  
2. listJobsForWorkflowRun  
3. analyze error deterministically (no speculation)  
4. patch file  
5. redeploy  

---

## SELF-HEALING

System must:

- detect failure  
- identify broken file  
- fix and redeploy  

---

## NO SIMULATION

If API not called → action not done.

---

## LIMITS

- max 5 operations per cycle  
- async only  
- no loops  