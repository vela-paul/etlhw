SELECT
  e.employee_id,
  e.first_name || ' ' || e.last_name AS employee_name,
  ROUND(SUM(ef.time_spent),2)           AS total_absence_time
FROM absence_facts ef
JOIN dim_employee e ON ef.employee_id = e.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY total_absence_time DESC;
