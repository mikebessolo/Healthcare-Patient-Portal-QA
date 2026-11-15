# Local execution summary

Date: 2026-11-13
Environment: Linux, Python 3.12.14, standard-library SQLite and HTTP client/server.
Command: `python3 -m unittest discover -s tests -v`

Result: **20 test methods passed**, 0 failures, 0 errors. Some methods cover multiple values through subtests. Captured terminal output is in `automated-results.txt`.

Covered: real localhost HTTP behavior, valid and invalid booking, owner-scoped reads and cancellation, conflicting simultaneous bookings, state persistence and database constraints.

Limitations: manual cases and exploratory charter have not been executed. Standalone SQL validation queries are provided for manual use; automated tests check selected database conditions directly. No GitHub Actions run, Windows/macOS run, performance assessment, external integration or production compliance assessment is claimed. GitHub Actions is configured for Python 3.11-3.13 but those cloud jobs have not run here. The sample defect is illustrative and is not an observed failure.
