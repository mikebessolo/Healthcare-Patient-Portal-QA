# Requirements and acceptance criteria

This fictional project models appointment management, not a clinical system. Each provider has one bookable appointment per date.

| ID | Requirement / acceptance criteria |
|---|---|
| R01 | Public GET /health returns 200 and status ok. |
| R02 | Appointment routes reject absent or unknown bearer tokens with 401. |
| R03 | A new patient receives an empty list; lists contain only the authenticated patient's records. |
| R04 | A valid booking returns 201 and stores matching patient, provider, date and scheduled status. The patient is derived only from the token. |
| R05 | Body must be a JSON object with exactly provider_id and visit_date. Provider must be a positive integer (not boolean). Dates must be valid YYYY-MM-DD strictly after the local current date. Unknown provider returns 404. Malformed input returns 400; wrong content type returns 415. |
| R06 | Only one active booking per provider/date is allowed, including concurrent requests; conflict returns 409 without an extra row. |
| R07 | Only the owner can cancel a booking. Unknown and other-patient IDs return 404. Cancellation persists; repeating it returns 200. Cancelled slots can be booked again. |
| R08 | Foreign keys prevent orphan records and a check constraint rejects invalid statuses. |
| R09 | Unknown routes return 404 for authenticated requests. |
