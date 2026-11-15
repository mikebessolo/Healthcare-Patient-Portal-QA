# Exploratory testing charter (not yet executed)

Mission: Spend 30 minutes investigating booking and cancellation behavior across two fictional patient identities.

1. Book with Patient A and list with both A and B.
2. Try cancelling A's booking as B; confirm status remains scheduled.
3. Cancel as A twice, then rebook the same provider/date.
4. Explore leap dates, tomorrow, today, empty fields and extra fields.
5. Repeat requests rapidly and inspect database state for duplicate active slots.

Record: environment, elapsed time, requests/responses, observations, questions and defect links. Do not mark an issue as confirmed until reproduced. No exploratory session is claimed in this starter.
