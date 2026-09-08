# Helpdesk Ticket Analytics — Data Analyst Portfolio Project

A self-contained analytics project simulating a B2B IT helpdesk: raw ticket data with realistic
data-quality issues, a Python cleaning pipeline, calculated KPIs, and a Power BI dashboard.

> **Note on the data:** This dataset is synthetically generated (see `generate_dataset.py`) to
> mimic a real helpdesk export, including intentional duplicates and nulls. It is built for
> practicing and demonstrating the analysis workflow end-to-end, not sourced from a live system.

## Overview

Support teams need visibility into whether they're meeting SLAs, keeping customers satisfied,
and resolving issues efficiently. This project builds that visibility from a raw, messy ticket
export through to a cleaned dataset, calculated KPIs, and an interactive dashboard.

## Dataset

**File:** `Helpdesk_Tickets_Dataset_1000.xlsx`
**Sheets:** `Tickets_Raw` (1,020 rows) · `KPI_Summary`

| Column | Description |
|---|---|
| Ticket_ID | Unique ticket identifier (`TKT-10001` format) |
| Created_Date | Date/time the ticket was opened (Jan–Dec 2024) |
| Client_Name | One of 6 client accounts |
| Priority | P1 (critical) – P4 (low) |
| Category | Network, VPN, Email/AD, Hardware, Software, VoIP, Security, API |
| Issue_Type | Internet Down, VPN Down, Email Failure, Login Failure, App Crash, DNS Failure |
| Status | Resolved, Closed, Open, In Progress |
| Agent | Assigned support agent |
| First_Response_Mins | Minutes to first response |
| Resolution_Time_Hours | Hours to resolution (MTTR) |
| SLA_Breach / SLA_Breach_Flag | 1/0 and Yes/No SLA breach indicator |
| CSAT_Score | Customer satisfaction, 1–5 |
| Is_Repeat_Ticket | 1/0 flag for repeat issues |
| Channel | Email, Portal, Phone, Chat |

**Intentional data quality issues** (for cleaning practice):
- 20 duplicate rows on `Ticket_ID` (1,020 total rows, 1,000 unique tickets)
- ~25 null values in `CSAT_Score`
- ~25 null values in `Category`

## How This Maps to a Data Analyst Job Description

| JD Requirement | Where it's covered |
|---|---|
| Regular / ad-hoc analyses | `clean_tickets.py` data profiling + KPI breakdowns by category/client |
| KPI tracking | SLA Adherence %, Avg CSAT, Avg MTTR, Repeat % — calculated in Python and DAX |
| Reports / dashboards | Power BI dashboard (bar, line, KPI cards) |
| Trend identification | CSAT-by-month line chart, MTTR-by-category comparison |
| Data quality monitoring | Duplicate/null detection and cleaning logic in `clean_tickets.py` |
| Documentation | This README + inline code comments |

## DAX Measures (Power BI)

```dax
SLA Adherence % = 1 - DIVIDE(
    COUNTROWS(FILTER(Tickets, Tickets[SLA_Breach] = 1)),
    COUNTROWS(Tickets)
)

Avg CSAT = AVERAGE(Tickets[CSAT_Score])

Avg MTTR = AVERAGE(Tickets[Resolution_Time_Hours])

Repeat % = DIVIDE(
    SUM(Tickets[Is_Repeat_Ticket]),
    COUNTROWS(Tickets)
)
```

## Tools Used

- **Python** (pandas, openpyxl) — data generation, cleaning, KPI calculation
- **Power BI** — dashboard and DAX measures
- **Excel** — source data format
- **SQL** — suggested next step: load `Tickets_Cleaned.xlsx` into a table and reproduce the KPIs
  above as `GROUP BY` / `CASE WHEN` queries for a SQL-specific writeup

## How to Run

```bash
pip install pandas openpyxl matplotlib

# 1. Regenerate the raw dataset (optional — the .xlsx is already included)
python generate_dataset.py

# 2. Profile, clean, and calculate KPIs
python clean_tickets.py
```

`clean_tickets.py` prints the data quality profile before/after cleaning, flags P1 SLA breaches,
and writes `Tickets_Cleaned.xlsx`.

## Key Findings

- **Duplicates:** 20 duplicate `Ticket_ID` rows removed (1,020 → 1,000 unique tickets).
- **SLA Adherence:** ~91% overall; P1 tickets breach SLA far more often (~30%) than P3/P4 (~5%),
  consistent with tighter response windows on critical issues.
- **CSAT vs. SLA breach:** Tickets that breach SLA skew toward lower CSAT scores (1–2), showing a
  clear link between response speed and customer satisfaction.
- **Repeat tickets:** ~12% of tickets are repeat issues — a candidate area for root-cause analysis.
- **MTTR:** Resolution time scales with priority as expected (P1 fastest, P3/P4 slowest), useful
  as a staffing/triage sanity check.

## Files in This Project

| File | Purpose |
|---|---|
| `Helpdesk_Tickets_Dataset_1000.xlsx` | Raw dataset (2 sheets) |
| `generate_dataset.py` | Generates the synthetic raw dataset |
| `clean_tickets.py` | Cleans data and calculates KPIs |
| `Tickets_Cleaned.xlsx` | Output of the cleaning script |
| `priority_distribution.png` | Preview chart: tickets by priority |
| `table_preview.png` | Preview: first 10 rows of raw data |
