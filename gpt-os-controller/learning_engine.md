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
- steps sequence
- frequency
- context

---

## STEP 2 - FREQUENCY ANALYSIS

If pattern.count > threshold:
    mark as candidate

---

## STEP 3 - CONFIDENCE SCORE

confidence = ¢
  (count / total_runs) *
  (step_stability) *
  (error_rate_inverse)

---

## STEP 4 - GENERATE SUGGESTION

Create:
suggested_hot_paths.json entry

---

## STEP 5 - GPT INTERACTION

GPT:
 "This pattern appeared N4 times. Add as hot_path?"

---

## RULES

- NEVE auto-apply
- NEVE modify system files directly
- ALWAYS require user confirmation

---

## FINAL

LEARNING = OBSRVERVATION + SUGGESTION
NOT AUTONOMOU EVOLUTION
