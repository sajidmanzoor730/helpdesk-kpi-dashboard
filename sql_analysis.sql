-- Helpdesk ticket analysis (SQLite syntax; works with small changes in PostgreSQL)
-- Load Helpdesk_Tickets_Dataset_Raw.csv into a table called tickets_raw first.
-- Concepts used: CTE, JOIN, aggregation, ROW_NUMBER, RANK, LAG, CASE.

-- 0. Reference table for the SLA policy (used in a JOIN below)
CREATE TABLE IF NOT EXISTS sla_policy (
    Priority TEXT PRIMARY KEY,
    Target_Hours INTEGER,
    Response_Class TEXT
);
INSERT OR REPLACE INTO sla_policy VALUES
    ('P1', 4,  'Critical'),
    ('P2', 8,  'High'),
    ('P3', 24, 'Normal'),
    ('P4', 72, 'Low');

-- 1. Clean view: remove duplicate tickets, fill blanks
CREATE VIEW IF NOT EXISTS tickets AS
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY Ticket_ID ORDER BY Created_At) AS rn
    FROM tickets_raw
)
SELECT Ticket_ID, Created_At, Resolved_At, Priority,
       COALESCE(Category, 'Unknown') AS Category,
       Channel, Team,
       COALESCE(Agent, 'Unassigned') AS Agent,
       Status, SLA_Target_Hours, Resolution_Hours,
       SLA_Breach, CSAT, Is_Repeat
FROM ranked
WHERE rn = 1;

-- 2. Headline KPIs (resolved/closed tickets only)
SELECT COUNT(*)                                              AS tickets,
       ROUND(100.0 * SUM(SLA_Breach = 'No') / COUNT(*), 1)   AS sla_adherence_pct,
       ROUND(AVG(Resolution_Hours), 1)                       AS mttr_hours,
       ROUND(AVG(CSAT), 2)                                   AS avg_csat,
       ROUND(100.0 * SUM(Is_Repeat = 'Yes') / COUNT(*), 1)   AS repeat_pct
FROM tickets
WHERE Status IN ('Resolved', 'Closed');

-- 3. SLA breach rate and MTTR by priority (JOIN to policy table)
SELECT t.Priority,
       p.Response_Class,
       COUNT(*)                                              AS tickets,
       ROUND(100.0 * SUM(t.SLA_Breach = 'Yes') / COUNT(*), 1) AS breach_pct,
       ROUND(AVG(t.Resolution_Hours), 1)                     AS mttr_hours,
       p.Target_Hours
FROM tickets t
JOIN sla_policy p ON p.Priority = t.Priority
WHERE t.Status IN ('Resolved', 'Closed')
GROUP BY t.Priority, p.Response_Class, p.Target_Hours
ORDER BY t.Priority;

-- 4. Monthly SLA trend with month-over-month change (CTE + LAG)
WITH monthly AS (
    SELECT SUBSTR(Created_At, 1, 7) AS month,
           COUNT(*) AS tickets,
           ROUND(100.0 * SUM(SLA_Breach = 'No') / COUNT(*), 1) AS sla_pct
    FROM tickets
    WHERE Status IN ('Resolved', 'Closed')
    GROUP BY SUBSTR(Created_At, 1, 7)
)
SELECT month, tickets, sla_pct,
       ROUND(sla_pct - LAG(sla_pct) OVER (ORDER BY month), 1) AS change_vs_prev_month
FROM monthly
ORDER BY month;

-- 5. Agent ranking inside each team (CTE + RANK)
WITH agent_stats AS (
    SELECT Team, Agent,
           COUNT(*) AS tickets,
           ROUND(100.0 * SUM(SLA_Breach = 'No') / COUNT(*), 1) AS sla_pct,
           ROUND(AVG(Resolution_Hours), 1) AS mttr_hours,
           ROUND(AVG(CSAT), 2) AS avg_csat
    FROM tickets
    WHERE Status IN ('Resolved', 'Closed') AND Agent <> 'Unassigned'
    GROUP BY Team, Agent
    HAVING COUNT(*) >= 20
)
SELECT Team, Agent, tickets, sla_pct, mttr_hours, avg_csat,
       RANK() OVER (PARTITION BY Team ORDER BY sla_pct DESC, mttr_hours ASC) AS team_rank
FROM agent_stats
ORDER BY Team, team_rank;

-- 6. Categories with the highest repeat rate
SELECT Category,
       COUNT(*) AS tickets,
       ROUND(100.0 * SUM(Is_Repeat = 'Yes') / COUNT(*), 1) AS repeat_pct,
       ROUND(AVG(Resolution_Hours), 1) AS mttr_hours
FROM tickets
WHERE Status IN ('Resolved', 'Closed')
GROUP BY Category
ORDER BY repeat_pct DESC;

-- 7. Busiest hours of the day (staffing insight)
SELECT SUBSTR(Created_At, 12, 2) AS hour_of_day,
       COUNT(*) AS tickets
FROM tickets
GROUP BY SUBSTR(Created_At, 12, 2)
ORDER BY tickets DESC
LIMIT 5;

-- 8. Breached P1/P2 tickets in the latest month (for a review list)
SELECT Ticket_ID, Created_At, Priority, Category, Agent,
       Resolution_Hours, SLA_Target_Hours
FROM tickets
WHERE SLA_Breach = 'Yes'
  AND Priority IN ('P1', 'P2')
  AND SUBSTR(Created_At, 1, 7) = (SELECT MAX(SUBSTR(Created_At, 1, 7)) FROM tickets)
ORDER BY Resolution_Hours - SLA_Target_Hours DESC;
