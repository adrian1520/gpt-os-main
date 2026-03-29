GPT RAM
Układ pamięci  świadomość stanu

memory/
├── debug/          ← błędy (per run)
├── session/        ← historia (per event)
└── source_of_truth.json  ← stan globalny

memory/
├── debug/
│   └── .keep
│
├── session/
│   └── .keep
│
└── source_of_truth.json



Architektura pamięci 

debug → co się zepsuło
session → co się działo
SOT → gdzie jesteśmy


BOOT FLOW 

GPT start
 ↓
GET memory/source_of_truth.json (API)
 ↓
parse
 ↓
ustaw kontekst rozmowy
 ↓
działanie

Minimalny zestaw
{
  "last_update": "...",
  "repo_state": {
    "files_count": 123,
    "debug_runs": 5,
    "sessions": 12
  },
  "debug_files": [...],
  "session_files": [...]
}


Interpretacja GPT 

✔ wiedzieć czy system jest aktywny
✔ wiedzieć czy są błędy (debug_runs > 0)
✔ wiedzieć czy coś się działo (sessions)
✔ mieć kontekst repo

Logika Startowa 

if debug_runs > 0:
    mode = "debug"

elif sessions > 0:
    mode = "continue_work"

else:
   mode = "init"


GPT Memory Bootstrap Protocol (MBP)

GPT start (nowa rozmowa)
↓
OBOWIĄZKOWO:
read memory/source_of_truth.json

memory/source_of_truth.json

PARSE

state = {
  "debug_runs": ...,
  "sessions": ...,
  "last_update": ...,
  "debug_files": [...],
  "session_files": [...]
}

DETECT MODE 

Logika 

if state["debug_runs"] > 0:
    mode = "DEBUG"

elif state["sessions"] > 0:
    mode = "CONTINUE"

else:
    mode = "INIT"

LOAD CONTEXT 

DEBUG MODE
→ pobierz ostatni:
memory/debug/run_<id>.json

GPT wie:
	•	co się wywaliło
	•	gdzie
	•	dlaczego

INIT MODE
→ brak pamięci → start clean

BUILD INTERNAL STATE

context = {
  "mode": mode,
  "last_error": ...,
  "last_action": ...,
  "repo_state": ...
}

AUTO RESPONSE

DEBUG
"Ostatni run zakończył się błędem w kroku: X.
Chcesz żebym to naprawił?"

CONTINUE
"Ostatnio pracowaliśmy nad: X.
Kontynuujemy?"

INIT
"System gotowy. Co budujemy?"


❗ HARD RULES

1. ZAWSZE czytaj source_of_truth na start
2. NIE zgaduj stanu
3. NIE ignoruj debug_runs
4. NIE zaczynaj od zera jeśli są dane

AUTO-PRIORITY
IF
debug_runs > 0
THEN
priorytet = DEBUG


Final memory model

GPT = stateless engine
+
memory = state
=
stateful system

———————————-

AUTO-LOAD SOT — FINALNY PROTOKÓŁ

KAŻDE zapytanie użytkownika
↓
NAJPIERW:
read memory/source_of_truth.json
↓
DOPIERO potem odpowiedź

user input
 ↓
[1] LOAD SOT (API)
 ↓
[2] PARSE STATE
 ↓
[3] DETECT MODE
 ↓
[4] LOAD CONTEXT (debug/session)
 ↓
[5] RESPONSE

GET memory/source_of_truth.jso

debug_runs = state["repo_state"]["debug_runs"]
sessions = state["repo_state"]["sessions"]

if debug_runs > 0:
    mode = "DEBUG"
elif sessions > 0:
    mode = "CONTINUE"
else:
    mode = "INIT"

DEBUG

load → memory/debug/run_<latest>.json



CONTINUE

load → memory/session/session_<latest>.json


SOT = JEDYNE źródło prawdy

👉 GPT NIE może:
	•	zgadywać
	•	ignorować SOT
	•	zaczynać „od zera”

każde pytanie = kontynuacja systemu

1. ładuje SOT
2. widzi debug_runs > 0
3. ładuje ostatni fail
4. odpowiada KONKRETNIE

Priorytet 

DEBUG > CONTINUE > INIT

HARD MODE 
IF

SOT nie istnieje

THEN

→ INIT MODE
→ + sugestia stworzenia pamięci

——-
auto memory load
state detection
context restore
zero-reset conversations



———————————-

✔ normalize
✔ base64
✔ api_write (jq safe)
✔ zero curl inline
✔ zero ręcznego JSON

✔ brak 422
✔ brak losowych fail
✔ brak konfliktów
✔ brak branchy
✔ pełna historia
✔ deterministyczny system

GPT → NIE dotyka finalnego zapisu
↓
Python interpreter → robi wszystko
↓
API write → tylko czyste dane



GPT → raw YAML / JSON
 ↓
Python (interpreter layer)
   ✔ normalize
   ✔ validate
   ✔ fix formatting
   ✔ base64
 ↓
api_write (jq safe)
 ↓
GitHub API


- name: Prepare content (Python)
  run: |
    python tools/prepare_content.py input.txt encoded.txt


import base64
import sys

inp = open(sys.argv[1]).read()

# normalize
inp = inp.replace("\r\n", "\n")
inp = inp.replace("\t", "  ")
inp = "\n".join(line.rstrip() for line in inp.splitlines())

if not inp.endswith("\n"):
    inp += "\n"

# encode
encoded = base64.b64encode(inp.encode()).decode()

open(sys.argv[2], "w").write(encoded)



- name: Load encoded
  run: |
    echo "CONTENT=$(cat encoded.txt)" >> $GITHUB_ENV


- uses: ./.github/actions/api_write
  with:
    path: ...
    content: ${{ env.CONTENT }}
    message: ...




GPT = generator (niepewny)
Python = validator (deterministyczny)
API = storage



————-
System rule 
 
💀 NO CACHED SHA
✔ ALWAYS FETCH BEFORE WRITE 
       
           retry with fresh SHA


✔ pobrany świeży SHA
✔ zapis wykonany poprawnie
✔ brak 409


💀 NEVER TRUST YAML + SHELL + JSON

💀 NIE generuj JSON w shell jeśli masz zagnieżdżone quote

💀 jeśli action.yml jest zła → cały workflow nie istnieje runtime'owo

💀 single point of failure


Polityka 

✔ prosty JSON → echo OK
✔ złożony JSON → printf
✔ duży JSON → python json.dump

IF

echo "{...${{ }}...}"
THEN
- AUTO FIX → printf

IF

cat <<EOF
{

THEN 
-  AUTO FIX → printf lub python

IF

json > 10 linii

THEN 
- AUTO FIX → python json.dump

IF 
echo '{"status":"ok"}'

THEN 
- ZOSTAW — OK
