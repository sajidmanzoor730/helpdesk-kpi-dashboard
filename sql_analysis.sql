-- Helpdesk BI analytical layer.
-- Source table: tickets_raw
-- Demonstrates CTEs, JOINs, ROW_NUMBER, LAG, RANK and exception analysis.

CREATE TABLE IF NOT EXISTS sla_policy (
    Priority TEXT PRIMARY KEY,
    Target_Hours INTEGER,
    Response_Class TEXT
);

INSERT OR REPLACE INTO sla_policy VALUES
    ('P1', 4, 'Critical'),
    ('P2', 8, 'High'),
    ('P3', 24, 'Normal'),
    ('P4', 72, 'Low');

CREATE VIEW IF NOT EXISTS tickets AS
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY Ticket_ID
               ORDER BY Created_At
           ) AS rn
    FROM tickets_raw
)
SELECT
    Ticket_ID, Created_At, First_Response_Minutes, Resolved_At,
    Priority, COALESCE(Category, 'Unknown') AS Category,
    Subcategory, Channel, Customer_Segment, Team,
    COALESCE(Agent, 'Unassigned') AS Agent,
    Status, SLA_Target_Hours, Resolution_Hours, SLA_Breach,
    Breach_Reason, Reopen_Count, Escalated, CSAT, Is_Repeat,
    Contact_Reason, Root_Cause, Region
FROM ranked
WHERE rn = 1;

-- 1. Executive KPI layer.
SELECT
    COUNT(*) AS resolved_tickets,
    ROUND(100.0 * SUM(SLA_Breach = 'No') / COUNT(*), 1) AS sla_adherence_pct,
    ROUND(AVG(Resolution_Hours), 1) AS avg_resolution_hours,
    ROUND(AVG(First_Response_Minutes), 0) AS avg_first_response_minutes,
    ROUND(AVG(CSAT), 2) AS avg_csat,
    ROUND(100.0 * SUM(Is_Repeat = 'Yes') / COUNT(*), 1) AS repeat_pct,
    ROUND(100.0 * SUM(Escalated = 'Yes') / COUNT(*), 1) AS escalation_pct
FROM tickets
WHERE Status IN ('Resolved', 'Closed');

-- 2. Priority-level SLA and resolution performance.
SELECT
    t.Priority,
    p.Response_Class,
    COUNT(*) AS tickets,
    ROUND(100.0 * SUM(t.SLA_Breach = 'Yes') / COUNT(*), 1) AS breach_pct,
    ROUND(AVG(t.Resolution_Hours), 1) AS avg_resolution_hours,
    p.Target_Hours
FROM tickets t
JOIN sla_policy p ON p.Priority = t.Priority
WHERE t.Status IN ('Resolved', 'Closed')
GROUP BY t.Priority, p.Response_Class, p.Target_Hours
ORDER BY t.Priority;

-- 3. Monthly trend with month-over-month SLA movement.
WITH monthly AS (
    SELECT
        SUBSTR(Created_At, 1, 7) AS month,
        COUNT(*) AS tickets,
        ROUND(100.0 * SUM(SLA_Breach = 'No') / COUNT(*), 1) AS sla_pct,
        ROUND(AVG(Resolution_Hours), 1) AS avg_resolution_hours,
        ROUND(AVG(CSAT), 2) AS avg_csat
    FROM tickets
    WHERE Status IN ('Resolved', 'Closed')
    GROUP BY SUBSTR(Created_At, 1, 7)
)
SELECT
    month, tickets, sla_pct, avg_resolution_hours, avg_csat,
    ROUND(sla_pct - LAG(sla_pct) OVER (ORDER BY month), 1) AS change_vs_prev_month
FROM monthly
ORDER BY month;

-- 4. Team and agent performance with minimum volume.
WITH agent_stats AS (
    SELECT
        Team, Agent, COUNT(*) AS tickets,
        ROUND(100.0 * SUM(SLA_Breach = 'No') / COUNT(*), 1) AS sla_pct,
        ROUND(AVG(Resolution_Hours), 1) AS avg_resolution_hours,
        ROUND(AVG(CSAT), 2) AS avg_csat,
        ROUND(100.0 * SUM(Escalated = 'Yes') / COUNT(*), 1) AS escalation_pct
    FROM tickets
    WHERE Status IN ('Resolved', 'Closed') AND Agent <> 'Unassigned'
    GROUP BY Team, Agent
    HAVING COUNT(*) >= 20
)
SELECT
    Team, Agent, tickets, sla_pct, avg_resolution_hours, avg_csat, escalation_pct,
    RANK() OVER (
        PARTITION BY Team
        ORDER BY sla_pct DESC, avg_resolution_hours ASC
    ) AS team_rank
FROM agent_stats
ORDER BY Team, team_rank;

-- 5. Repeat demand and reopen behavior by category.
SELECT
    Category,
    COUNT(*) AS tickets,
    ROUND(100.0 * SUM(Is_Repeat = 'Yes') / COUNT(*), 1) AS repeat_pct,
    ROUND(AVG(Reopen_Count), 2) AS avg_reopens,
    ROUND(AVG(Resolution_Hours), 1) AS avg_resolution_hours
FROM tickets
WHERE Status IN ('Resolved', 'Closed')
GROUP BY Category
ORDER BY repeat_pct DESC;

-- 6. Demand by channel and customer segment.
SELECT
    Channel,
    Customer_Segment,
    COUNT(*) AS tickets,
    ROUND(AVG(First_Response_Minutes), 0) AS avg_first_response_minutes,
    ROUND(100.0 * SUM(SLA_Breach = 'Yes') / COUNT(*), 1) AS breach_pct
FROM tickets
GROUP BY Channel, Customer_Segment
ORDER BY tickets DESC;

-- 7. Workload by hour and day.
SELECT
    SUBSTR(Created_At, 12, 2) AS hour_of_day,
    COUNT(*) AS tickets
FROM tickets
GROUP BY SUBSTR(Created_At, 12, 2)
ORDER BY tickets DESC
LIMIT 8;

-- 8. High-priority exception queue.
SELECT
    Ticket_ID, Created_At, Priority, Category, Subcategory,
    Team, Agent, Channel, Resolution_Hours, SLA_Target_Hours,
    ROUND(Resolution_Hours - SLA_Target_Hours, 2) AS SLA_Variance_Hours,
    Breach_Reason, Escalated
FROM tickets
WHERE SLA_Breach = 'Yes'
  AND Priority IN ('P1', 'P2')
ORDER BY SLA_Variance_Hours DESC
LIMIT 100;
