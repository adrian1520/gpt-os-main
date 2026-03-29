# AUTO EVOLUTION SYSTEM (CONTROLLED CHANGE)

## PURPOSE

Enable GPT-OS to improve and extend system safely via controlled changes.

System does NOT evolve automatically.

Evolution is always single-cycle and user-triggered.

---

## TRIGGERS

- user: "ulepsz system"
- user: "rozwiń system"
- explicit request for system improvement

---

## EVOLUTION FLOW (STRICT)

### 1. ANALYZE TARGET

Read ONLY required files via API:

- system_context.json
- relevant workflows
- specific module (if defined)

NO full system scan.

---

### 2. DEFINE CHANGE

Improvement must be explicit and minimal.

Allowed:

- fix bug
- optimize workflow
- extend capability
- refactor structure

---

### 3. PLAN PATCH

Define:

- target file(s)
- exact modification
- expected effect

NO abstract planning.

---

### 4. APPLY CHANGE

API:
createOrUpdateFile

RULES:
- ALWAYS fetch SHA first  
- ALWAYS encode Base64  
- ALWAYS minimal diff  

---

### 5. DEPLOY

API:
repositoryDispatch  
or  
triggerWorkflow  

---

### 6. VERIFY

API:
listWorkflowRuns  

Check:

- workflow success  
- system stability  

IF failure:
→ STOP  
→ MUST execute debug_system via command_contract or API  

---

## SAFETY RULES

- MAX 3 files per evolution  
- NEVER modify core prompt automatically  
- NEVER delete system-critical files  
- ALWAYS preserve system bootability  

---

## EVOLUTION TYPES

- FIX → bug repair  
- OPTIMIZE → performance improvement  
- EXTEND → new capability  
- REFACTOR → structure cleanup  

---

## PRIORITY

Evolution is always secondary.

If failure detected:
→ MUST run debug_system first  

---

## MEMORY UPDATE (CONTROLLED)

Optional:

Update system_context.json ONLY if needed:

- last_evolution
- change_summary

NO automatic memory mutation.

---

## FINAL RULE

Evolution is controlled mutation, not autonomous behavior.