# REASONING ENGINE (GRAPH BASED)

## PURPOSE

Defines how GPT-OS selects and executes chunks using:
- dependency_graph
- hot_paths

---

## INPUT

user_input
SOT state
semantic_routes

---

## STEP 1 - MODE DETECTION

if DEBUG:
    FORCE path = "debug_flow"
    SKIP other routing

elif CONTINUE:
    path = "route_match"

else:
    path = "route_match"

---

## STEP 2 - ROUTE MATCH

route_match = semantic_routes match

---

## STEP 3 - HOT PATH MATCH

FOR each path in hot_paths:

    if semantic match (user_input, trigger):
        selected_path = path
        break

---

## STEP 4 - GRAPH EXECUTION

IF hot_path found:
    steps = hot_path steps

ELSE:
    use dependency_graph

    start = route_match node

    traverse graph (DFS/BFS):
        - follow dependencies
        - avoid cycles
        - stop at execution layer

---

## STEP 5 - GOVERNOR CHECK

ALL steps MUST include:
→ governor.control

---

## STEP 6 - INTERPRETER ENFORCEMENT

IF write operation:
→ MUST include interpreter.layer

---

## OUTPUT

list of execution steps

---

## RULES

- NEVER execute all chunks
- use minimal path
- prioritize hot_paths
- fallback to graph

---

## FINAL

Graph + Hot Paths = Deterministic Reasoning