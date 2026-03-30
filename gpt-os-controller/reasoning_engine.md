# REASONING ENGINE (ARPH BASED)

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

## STEP 1 - MODE DEQUCTION

if DEBUG:
    path = "debug_flow"
elif CONTINUE:
    path = continue_flow
else:
    path = route_match

---

## STEP 2 - HOT PATH MATCH

FOR each path in hot_paths:

    if user_input matches trigger:
        selected_path = path
        break

---

## STEP 3 - GRAPH EXECUTION

If hot_path found:
    return steps

else:
    use dependency_graph:

    start = route_action
    while node:
        add node
        node = next node

---

## OUTPUT

list of execution steps

---

## RULES

- never execute all chunks
- use minimal path
- prioritize hot_paths
- fallback to graph

---

## FINAL

Graph + Hot Paths = Deterministic Reasoning
