# BI Validation & Monitoring

## Purpose
This document defines practical controls for validating the Helpdesk BI reporting layer. It is a portfolio implementation guide, not a claim of production monitoring infrastructure.

## 1. Source-to-report reconciliation
Before publishing a reporting refresh, compare the same KPIs across the curated dataset and the BI layer:

| Control | Expected result |
|---|---|
| Unique Ticket_ID count | Matches curated ticket count |
| Resolved/Closed count | Matches SQL result |
| SLA adherence % | Matches SQL result within rounding tolerance |
| Average resolution hours | Matches SQL result within rounding tolerance |
| Average CSAT | Matches SQL result within rounding tolerance |
| Repeat-ticket rate | Matches SQL result within rounding tolerance |
| Escalation rate | Matches SQL result within rounding tolerance |

The SQL queries in sql_analysis.sql provide the comparison baseline.

## 2. Data-quality gates
The Python QA layer should run before reporting:

- Ticket_ID is unique after ETL.
- Created_At is populated.
- Priority values are limited to P1–P4.
- Channel values are from the defined source list.
- Resolution timestamps cannot precede creation timestamps.
- SLA_Breach contains only Yes/No.
- Status values are controlled.
- CSAT values are between 1 and 5 when present.
- Curated row count is greater than zero.

A failed check stops the process instead of silently producing a report.

## 3. Refresh monitoring
For a production implementation, track:

- refresh start/end time;
- refresh duration;
- source row count;
- curated row count;
- duplicate count;
- rejected-record count;
- data-quality status;
- KPI reconciliation status.

The current Streamlit dashboard exposes the ETL audit values for inspection. It does not claim scheduled production refresh monitoring.

## 4. Report performance practices
The semantic model is designed to reduce unnecessary report complexity:

- keep FactTickets at one clear grain;
- use dimensions for filtering and grouping;
- prefer reusable measures over repeated calculations;
- avoid unnecessary bi-directional relationships;
- remove unused columns before loading into a BI model;
- use minimum-volume thresholds when comparing individual agents;
- validate totals against SQL after a refresh.

## 5. Investigation workflow
When a KPI changes unexpectedly:

1. Check source and curated row counts.
2. Check duplicate and rejected-record counts.
3. Compare the KPI with the SQL baseline.
4. Break the KPI down by date, priority, team and category.
5. Inspect the underlying exception records.
6. Document the cause before changing the reporting logic.

## Scope and honesty note
The repository demonstrates the controls and analytical workflow that would be used in a BI environment. It does not claim a live enterprise Power BI gateway, scheduled refresh service, production warehouse, OLAP platform or alerting system that has not actually been implemented.
