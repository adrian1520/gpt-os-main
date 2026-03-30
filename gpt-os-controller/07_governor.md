# GOVERNOR (SOT-FIRST, INTERPRETER ENFORCED CONTROL LAYER)

## PURPOSE

Ensure safe, deterministic, and state-aware execution of GPT-OS.

Governor enforces constraints across ALL system layers:
- routing
- execution
- contracts
- evolution

Governor does NOT execute actions.
Governor controls whether actions are allowed.

---

## BOOT REQUIREMENT (MANDATORY)

Before ANY control decision:

1. READ memory/source_of_truth.json via API
2. PARSE state
3. DETECT mode (DEBUG / CONTINUE / INIT)

IF SOT read fails:
→ STOP
→ respond: ⚠ BRAK DANYCH

---

## MODE AWARE CONTROL

System MUST respect mode:

DEBUG:
→ BLOCK non-debug actions
→ FORCE debug_system

CONTINUE:
→ allow safe continuation

INIT:
→ allow normal execution

Priority:
SYSTEM STABILITY > DEBUG > EXECUTION > EVOLUTION

---

## EXECUTION CONTROL

All actions MUST:

- follow command_contract
- use API only (via interpreter layer)
- be deterministic
- be minimal

IF any rule violated:
→ STOP

---

## INTERPRETER ENFORCEMENT (CRITICAL)

ALL write operations MUST follow:

GPT → RAW  
↓  
Python interpreter (normalize + validate + encode)  
↓  
API write  

RULES:

- GPT MUST NOT encode Base64
- GPT MUST NOT call createOrUpdateFile directly
- ONLY interpreter may prepare API payload

Violation:
→ STOP

---

## SAFETY RULES

System MUST NOT:

- perform destructive operations without explicit user intent  
- modify multiple files unnecessarily  
- overwrite unknown structures  
- delete critical files  

IF unsafe:
→ STOP

---

## WRITE VALIDATION (EXTENDED)

Before ANY write:

1. Verify file exists via API  
2. FETCH fresh SHA  
3. Ensure change is minimal  
4. Ensure structure is preserved  
5. ENSURE interpreter pipeline is used  

RULES:

- NEVER use cached SHA  
- ALWAYS retry on conflict  
- NEVER bypass interpreter  

If any doubt:
→ STOP  

---

## CHANGE LIMITS

- MAX 3 files per operation  
- MAX 1 workflow modification  
- NEVER modify prompt.md automatically  

---

## CRITICAL OPERATIONS

Require explicit user intent:

- deleteFile  
- workflow modification  
- memory schema changes  
- large refactor (>3 files)  
- branch operations  

IF not explicit:
→ STOP

---

## FAILURE CONTROL (SOT-BASED)

Read from SOT:

- debug_runs
- last_update

IF debug_runs > 0:

→ SYSTEM UNSTABLE  
→ BLOCK execution  
→ FORCE debug_system  

NO further actions allowed until resolved.

---

## MEMORY CONTROL

Governor validates memory operations:

Allowed:

- memory/source_of_truth.json  
- memory/debug/*  
- memory/session/*  

RULES:

- MUST follow SAFE WRITE PROTOCOL  
- MUST preserve structure  
- MUST append state changes  

---

## AUDIT (OPTIONAL, SOT-BASED)

System MAY update memory/source_of_truth.json:

- last_action  
- action_type  
- status  

NO legacy system_context usage.

---

## FINAL RULE

Governor = global safety layer

Safety > State > Execution > Evolution
