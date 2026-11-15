# Test plan

## Objective
Evaluate the fictional appointment API against R01-R09, concentrating on patient isolation, booking correctness, persistence and input handling.

## Scope
Functional API behavior, negative cases, boundary dates and types, duplicate/concurrent booking, cancellation, and database constraints. No UI, clinical validation, live EHR, accessibility, load, penetration, or regulatory certification testing is included.

## Environment and test data
Python 3.11+ standard library, localhost HTTP, SQLite. Each automated method uses a fresh temporary database and a random port. Two fictional patients and two providers are seeded. Tests compute dates relative to today. Manual checks use the persistent portal.db and require a clean database for deterministic starting results.

## Risks and priority
High: another patient viewing or changing a record; double booking; incorrect persisted data. Medium: invalid inputs accepted or incorrect error status. Low: health endpoint and unknown routes. The access and concurrency checks exercise selected controls, not a complete security assessment.

## Entry criteria
Python available, project extracted, requirements reviewed, no real patient data entered.

## Execution
Run the README test command. Run the manual cases separately with curl or a REST client and record actual results. Use sql/validation.sql on populated data. Save observed failures with steps, expected/actual results, environment and response body.

## Exit criteria
All automated tests pass; high-priority manual cases executed with actual results; no unresolved high-severity defects. This starter's manual cases remain Not Run, so full exit criteria are not met.

## Deliverables
Requirements, manual case CSV, traceability, regression source/output, SQL checks, exploratory charter and a clearly labelled illustrative defect. No invented production outcomes or employer metrics are included.
