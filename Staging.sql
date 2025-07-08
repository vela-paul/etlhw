DROP TABLE stg_calendar_events;
CREATE TABLE stg_calendar_events (
  event_id   INTEGER,
  email VARCHAR2(100),
  start_time     DATE,
  end_time       DATE,
  summary        VARCHAR2(200),
  description    VARCHAR2(1000)
);

SELECT COUNT(*) FROM stg_calendar_events;

INSERT INTO event_facts (employee_id, event_id, date_id, time_spent)
SELECT
  e.employee_id,
  ev.event_id,
  d.date_id,
  (s.end_time - s.start_time) * 24 AS time_spent
FROM stg_calendar_events s
  JOIN dim_employee  e  ON e.email         = s.email
  JOIN dim_events    ev ON ev.event_id = s.event_id
  JOIN dim_date      d  ON d.full_date     = TRUNC(s.start_time);

SELECT COUNT(*) FROM event_facts;


CREATE TABLE stg_participants (
  name   VARCHAR2(100),
  email VARCHAR2(100),
  first_join     DATE,
  last_leave       DATE,
  in_meeting_duration INTEGER,
  role    VARCHAR2(30),
  meeting_id INTEGER
);


INSERT INTO attendence_facts (
  employee_id,
  meeting_id,
  date_id,
  time_spent,
  role
)
SELECT
  de.employee_id,
  dm.meeting_id,
  dd.date_id,
  ROUND(sp.in_meeting_duration / 3600, 2) AS time_spent,
  sp.role
FROM stg_participants sp
  JOIN dim_employee de
    ON de.email = sp.email

  JOIN dim_meetings dm
    ON dm.meeting_id = sp.meeting_id

  JOIN dim_date dd
    ON dd.full_date = TRUNC(sp.first_join);
;

SELECT * from attendence_facts;

