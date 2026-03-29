# RULES & API PROTOCOL

## MEMORY ENFORCEMENT (CRITICAL)

BEFORE ANY ACTION:
- MUST read memory/source_of_truth.json via API
- MUST validate SOT load
- IF SOT not available => STOP
- IF SOT not loaded => NO EXECUTION

---

## INTERPRETER LAYER (CRITICAL)

- GPT MUST NOT perform final writes
- GPT MUST NOT encode Base64
- GPT MUST NOT construct final API payload

ALL writes MUST go through Python interpreter layer:
- normalize
- validate
- format
- encode (base64)

ONLY validated content may reach API

---

## EXECUTION RULE

If API or command is available:
→ MUST execute  
→ DO NOT explain instead of executing  

---

## GLOBAL PRIORITY ENGINE

System MUST always follow priority:

1. CRITICAL ERROR
2. DEBUG
3. EXECUTION
4. MEMORY
5. EVOLUTION

---

## SAFE WRITE PROTOCOL

Before ANY write:

1. READ file
2. FETCH fresh SHA
3. VALIDATE
4. APPLY minimal change

NEVER use cached SHA
ALWAYS retry on conflict

---

## JSON SAFETY

- simple JSON → echo OK
- complex JSON → printf
- large JSON → python json.dump

NEVER build complex JSON inline in shell

---

## NO SIMULATION

If API not called → action not done
