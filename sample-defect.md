# Illustrative defect report — not an observed current defect

ID: SAMPLE-001
Title: Patient B can cancel Patient A's appointment
Severity: High (hypothetical access-control failure)
Status: Training example only; current regression asserts this action returns 404.
Environment: Local fictional API, two demo tokens, fresh SQLite database.

## Reproduction for a vulnerable implementation
1. POST /appointments using demo-patient-1 with provider_id 1 and a future visit_date.
2. Save the returned appointment id.
3. POST /appointments/{id}/cancel using demo-patient-2.
4. GET /appointments as demo-patient-1 and inspect the appointment status.

Expected: Step 3 returns 404 and the appointment remains scheduled.
Hypothetical faulty result: Step 3 returns 200 and cancels another patient's booking.
Business impact: Unauthorized appointment changes and disrupted patient access.
Suggested investigation: Check whether the UPDATE filters on both appointment ID and authenticated patient ID.
Regression: test_cannot_cancel_another_patient_record in tests/test_api.py.

This template demonstrates defect reporting. It is not evidence that this defect was found in an employer system or in the delivered code.
