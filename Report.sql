-- change the names if your columns differ
VARIABLE emp_id NUMBER;

BEGIN
  SELECT employee_id
    INTO :emp_id
  FROM dim_employee
  WHERE first_name = 'Paul-Valentin'
    AND last_name  = 'Vela';
END;
/

SELECT
  d.full_date,
  COALESCE(a.hours_worked,0)     AS hours_worked,
  COALESCE(m.hours_in_meetings,0) AS hours_in_meetings
FROM dim_date d

  LEFT JOIN (
    SELECT date_id, hours_worked
    FROM activity_facts
    WHERE employee_id = :emp_id
  ) a  ON a.date_id = d.date_id

  LEFT JOIN (
    SELECT date_id, SUM(time_spent) AS hours_in_meetings
    FROM event_facts
    WHERE employee_id = :emp_id
    GROUP BY date_id
  ) m  ON m.date_id = d.date_id

WHERE d.full_date
  BETWEEN DATE '2025-06-01'  -- ← adjust your date range
      AND DATE '2025-06-30'
ORDER BY d.full_date;

SELECT
  d.full_date,
  COALESCE(a.hours_worked,0)     AS hours_worked,
  COALESCE(m.hours_in_meetings,0) AS hours_in_meetings
FROM dim_date d

  LEFT JOIN (
    SELECT date_id, hours_worked
    FROM activity_facts
    WHERE employee_id = :emp_id
  ) a  ON a.date_id = d.date_id

  LEFT JOIN (
    SELECT date_id, SUM(time_spent) AS hours_in_meetings
    FROM event_facts
    WHERE employee_id = :emp_id
    GROUP BY date_id
  ) m  ON m.date_id = d.date_id

WHERE d.full_date
  BETWEEN DATE '2025-06-01'  -- ← adjust your date range
      AND DATE '2025-06-30'
ORDER BY d.full_date;
