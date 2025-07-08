SELECT
  de.employee_id,
  de.first_name || ' ' || de.last_name AS employee_name,
  ROUND(SUM(af.time_spent),2)           AS total_hours_attended
FROM attendence_facts af
JOIN dim_employee de  ON af.employee_id = de.employee_id
GROUP BY de.employee_id, de.first_name, de.last_name
ORDER BY total_hours_attended DESC;


