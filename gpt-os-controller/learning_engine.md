# LEARNING ENGINE (SUGGESTION MODE)

## PURPOSE

Enable system to detect repeated patterns and suggest new hot_paths.

NOT:
- does NOT auto-modify system
- requires human approval

---

## INPUT

session_logs
debug_logs
hot_paths
chunk_index

---

## STEP 1 - PATTERN CAPTURE

Track execution paths:
- steps sequence (must match chunk_index IDs)
- frequency
- context

IGNORE failed debug runs.

---

## STEP 2 - FREQUENCY ANALYSIS

threshold:
- min_count: 3
- min_confidence: 0.7

If pattern.count >= min_count:
    mark as candidate

---

## STEP 3 - CONFIDENCE SCORE

confidence =
  (count / total_runs) *
  (step_stability) *
  (1 - error_rate)

---

## STEP 4 - GENERATE SUGGESTION

Create:
suggested_hot_paths.json entry

---

## STEP 5 - GPT INTERACTION

GPT:
"This pattern appeared N times. Add as hot_path?"

---

## RULES

- NEVER auto-apply
- NEVER modify system files directly
- ALWAYS require user confirmation

---

## FINAL

LEARNING = OBSERVATION + SUGGESTION  
NOT AUTONOMOUS EVOLUTION