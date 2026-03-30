# RULES & API PROTOCOL

## MEMORY ENFORCEMENT (CRITICAL)

BEFORE ANY ACTION:
- MUST read memory/source_of_truth.json via API
- MUST validate SOT load

IF SOT not available:
→ STOP

IF SOT read fails:
→ respond: ⚠ BRAK DANYCH

IF SOT not loaded:
→ NO EXECUTION

---

## MODE AWARENESS (CRITICAL)

System MUST respect mode from SOT:

- DEBUG
- CONTINUE
- INIT

Priority:
DEBUG > CONTINUE > INIT

---

## INTERPRETER LAYER (CRITICAL)

- GPT MUST NOT perform final writes
- GPT MUST NOT encode Base64
- GPT MUST NOT construct final API payload

ALL writes MUST go through Python interpreter layer:

FLOW:
RAW → normalize → validate → format → encode → API write

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

## MEMORY WRITE PROTOCOL

All memory operations MUST follow SAFE WRITE PROTOCOL:

Applies to:
- memory/debug/*
- memory/session/*
- memory/source_of_truth.json

Memory updates MUST:
- be deterministic
- preserve structure
- append, not overwrite (unless required)

---

## JSON SAFETY

- simple JSON → echo OK  
- complex JSON → printf  
- large JSON → python json.dump  

NEVER build complex JSON inline in shell  

---

## NO SIMULATION

If API not called → action not done
