# Healthcare Patient Portal QA

An independent QA portfolio project by **Michael Abessolo** demonstrating healthcare workflow analysis, API testing, SQL validation, and test documentation using fictional data.

## What this demonstrates

- Translate requirements into test scenarios and traceable checks.
- Test an actual local HTTP API with positive, negative, boundary, access-control, and concurrent requests.
- Verify API changes persist correctly in SQLite.
- Explain risk, report a reproducible defect, and distinguish executed evidence from planned work.

## Quick start (macOS, Linux, or Windows)

Install Python 3.11 or newer. No third-party packages, paid services, or API keys are needed.
From this project's root folder:

```bash
python3 -m unittest discover -s tests -v
python3 -m app.server
```

On Windows, use `py` in place of `python3`. The second command starts the demo at `http://127.0.0.1:8000`. Stop it with Ctrl+C. It creates `portal.db`; deleting that file while the server is stopped resets the demo data.

## Try a request

```bash
curl http://127.0.0.1:8000/health
curl -H 'Authorization: Bearer demo-patient-1' http://127.0.0.1:8000/appointments
curl -X POST http://127.0.0.1:8000/appointments \
  -H 'Authorization: Bearer demo-patient-1' \
  -H 'Content-Type: application/json' \
  -d '{"provider_id":1,"visit_date":"2099-06-15"}'
```

Use any future date; repeating an active provider/date combination returns 409. On Windows PowerShell, use `curl.exe`. Public tokens are fixed demo identities, not real authentication credentials.

## API contract

| Method | Route | Expected behavior |
|---|---|---|
| GET | `/health` | 200 without a token |
| GET | `/appointments` | 200; only the token owner's appointments |
| POST | `/appointments` | 201; requires exactly integer provider_id and future YYYY-MM-DD visit_date |
| POST | `/appointments/{id}/cancel` | 200 for an owned appointment; repeated cancellation returns 200 |

Other responses: 400 invalid body, 401 missing/invalid token, 404 missing provider/appointment/route, 409 occupied slot, 415 incorrect content type. Appointment routes require `Bearer demo-patient-1` or `Bearer demo-patient-2`. Unknown HTTP methods use the standard HTTP handler's 501 response.

## Project map

| Folder | Contents |
|---|---|
| `app/` | Runnable local API |
| `tests/` | HTTP regression tests and database assertions |
| `docs/` | Requirements, test plan, manual cases, traceability, exploratory charter, sample defect |
| `sql/` | Schema, fictional seed records, validation queries |
| `reports/` | Actual local execution output and summary |
| `.github/workflows/` | Proposed GitHub Actions regression workflow |

## Manual and SQL practice

Follow `docs/manual-test-cases.csv` while the API is running. A REST client such as Postman can send the same requests as curl. Record your own results in the Actual Result and Status columns; these cases are initially Not Run.

If the sqlite3 command-line tool is installed:

```bash
sqlite3 -header -column portal.db < sql/validation.sql
```

The first three SQL queries should return no rows; the final query shows per-patient totals. Run these after booking and cancelling appointments so the checks operate on meaningful data. Automated tests also inspect the database directly.

## Scope and limitations

This is an educational API simulation, with no user interface or real health records. It does not integrate with Epic, insurers, or a production EHR and makes no HIPAA compliance claim. Fixed demo tokens, local date handling, and one appointment per provider per day are intentional simplifications. It has no real login, time slots, rate limiting, audit trail, HTTPS, or production deployment design. Bind remains localhost; do not expose it as a production service.

## Upload to GitHub

1. Unzip this package and open the project folder.
2. Sign in to GitHub and create an empty repository named `healthcare-patient-portal-qa` (do not add a README).
3. In a terminal inside this project folder, run:

```bash
git init
git add .
git commit -m "Add healthcare API QA portfolio project"
git branch -M main
git remote add origin https://github.com/mikebessolo/healthcare-patient-portal-qa.git
git push -u origin main
```

Replace the username if needed. If that repository name already exists, choose a new name and update the URL; do not overwrite an existing project. Authenticate using GitHub's supported login flow. After pushing, check the Actions tab; cloud execution has not been verified in this package.

## Suggested next improvements

Run the manual cases yourself, add evidence from your REST client, write a small set of new tests, and explain one defect investigation in your own words before featuring the repository on LinkedIn. This starter was created with AI assistance; review and understand it before presenting it as portfolio work.
