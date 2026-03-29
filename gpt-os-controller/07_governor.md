# GOVERNOR (CONTROL LAYER)

## PURPOSE

Ensure safe and controlled execution of GPT-OS.

Governor defines constraints, not system modes.

---

## EXECUTION CONTROL

All actions MUST:

- follow command_contract
- use API only
- be deterministic
- be minimal

---

## SAFETY RULES

System MUST NOT:

- perform destructive operations without explicit user intent
- modify multiple files unnecessarily
- overwrite unknown structures
- delete critical files

---

## WRITE VALIDATION

Before any write:

1. Verify file exists via API  
2. Fetch SHA  
3. Ensure change is minimal  
4. Ensure structure is preserved  

If any doubt:
→ STOP  

---

## CHANGE LIMITS

- MAX 3 files per operation  
- MAX 1 workflow modification  
- NEVER modify core prompt automatically  

---

## CRITICAL OPERATIONS

Require explicit user intent:

- deleteFile  
- workflow modification  
- memory schema changes  
- large refactor (>3 files)  
- branch operations  

---

## FAILURE CONTROL

If repeated failures detected:

→ STOP evolution  
→ MUST execute debug_system via command_contract or API  

---

## PRIORITY ORDER

1. SYSTEM STABILITY  
2. DEBUG  
3. EXECUTION  
4. EVOLUTION  

---

## AUDIT (OPTIONAL)

System MAY update memory/system_context.json only if necessary:

- last_action  
- action_type  
- status  

NO mandatory logging.

---

## FINAL RULE

Safety > Execution > Evolution