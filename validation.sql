-- Run against a populated demo database. Each exception query should return zero rows.
-- Orphan appointments
SELECT a.* FROM appointments a
LEFT JOIN patients p ON p.id=a.patient_id
LEFT JOIN providers d ON d.id=a.provider_id
WHERE p.id IS NULL OR d.id IS NULL;

-- Duplicate active provider slots
SELECT provider_id, visit_date, COUNT(*) AS active_count
FROM appointments WHERE status='scheduled'
GROUP BY provider_id, visit_date HAVING COUNT(*) > 1;

-- Invalid statuses
SELECT * FROM appointments WHERE status NOT IN ('scheduled','cancelled');

-- Reporting query; counts include both zero and nonzero totals.
SELECT p.name, COUNT(a.id) AS appointment_count
FROM patients p LEFT JOIN appointments a ON a.patient_id=p.id
GROUP BY p.id, p.name;
