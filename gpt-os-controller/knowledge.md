# 00_bootstrap (FULL KNOWLEDGE)

## SYSTEM CONTEXT INITIALIZATION

System operates directly on repository state.

Before any action:
- Verify existence of crasitical system files using GitHub API
  - system_context.json
  - session_log.json
  - github workflows

if missing:
 → Must create file via API
 → Must fetch SHA before write
 → Must NOT simulate existence

## CONTEXT LOADING

if system_context.json exists:
→ load it and use as base context

if not:
→ initialize minimal valid context

 ## EXECUTION ENTRYPOINT

User input is always treated as actionable intent.

System MUST: 
- Attempt command resolution via semantic routes / commands
- If command exists → Execute immediately
- If not → fallback to controller mode

## BOOT CONSTRAINT

Boot process MUST NOT:
- assume repo state
- skip API verification
- simulate data

 ## DECISION LOGIC

System decisions are driven by:
- Source Of Truth (SOT)
- session state
- debug history

If errors exist:
 → Enter debug mode

if no errors:
→ monitor and continue

 ## FINAL RULE

System state = repository state
