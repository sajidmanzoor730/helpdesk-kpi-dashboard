# Helpdesk Ticket KPI Dashboard

A small end-to-end analytics project: clean a messy helpdesk ticket export, calculate support KPIs with Python and SQL, and show them in an interactive dashboard.

**Live demo:** https://hedesk-dashboard.streamlit.app/

> **Note:** The dataset is synthetic. I generated it to look like a real helpdesk export, including deliberate duplicates and missing values, so the cleaning steps are realistic.

![Dashboard](dashboard.jpg)

## What this project does

1. **Raw data:** 1,020 ticket rows, including 20 duplicate or null rows.
2. **Cleaning (Python + Pandas):** removes duplicates, handles nulls, fixes types. Result: 1,000 unique tickets.
3. **KPIs:** calculated in Python and SQL.
4. **Dashboard:** Streamlit app (live) and Power BI report.

## Dataset

File: `Helpdesk_Tickets_Dataset_1000.xlsx`

Columns: Ticket_ID, Priority (P1-P4), Category, Status, SLA_Breach, CSAT (1-5), Is_Repeat

See `data_dictionary.md` for column definitions.

## KPIs and findings

| KPI | Result |
|---|---|
| SLA adherence | 91.2% (8.8% breached) |
| P1 SLA breach rate | 30%, versus about 5% for P3/P4 |
| Average CSAT | 3.73 / 5 |
| Repeat ticket rate | 12% |
| Data quality after cleaning | 98% |

Main takeaway: high-priority tickets breach SLA far more often than low-priority ones, so P1 handling is the first thing to improve.

![Priority distribution](priority_distribution.png)

## SQL analysis

`sql_analysis.sql` contains the queries behind the KPIs: [add one line here on what it covers, e.g. joins, CTEs, window functions].

## How to run

```bash
pip install -r requirements.txt
python clean_tickets.py
streamlit run app.py
```

## Files

| File | Purpose |
|---|---|
| `clean_tickets.py` | Cleaning pipeline |
| `app.py` | Streamlit dashboard |
| `sql_analysis.sql` | KPI queries |
| `Helpdesk_Tickets_Dataset_1000.xlsx` | Dataset |
| `data_dictionary.md` | Column definitions |
| `docs/` | Design notes |

## Possible extensions

- Add caching and role-based access for a multi-user setup
- Send SLA breaches to a review queue
- Connect to a real ticketing system (JIRA, ServiceNow, Zendesk)

## Author

Sajid Manzoor | Technical Support / Operations
LinkedIn: [add your correct profile link]
