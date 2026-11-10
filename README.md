# Helpdesk KPI Dashboard

A Python and Streamlit project for exploring published IT helpdesk reporting data. The live dashboard loads the official Montgomery County Government **MCG HelpIT Tickets** public dataset, validates the published summary rows, and provides fiscal-year and report-section views.

**Stack:** Python · Pandas · Streamlit  
**Live dashboard:** https://hedesk-dashboard.streamlit.app/  
**Public source:** https://data.montgomerycountymd.gov/d/qzr8-h9x6

> **Important data distinction:** The live dashboard uses aggregated public summary data. It is not a row-per-ticket export. This repository also retains an earlier synthetic ticket-level practice exercise. Do not combine the two sources or attribute the synthetic ticket KPI values to Montgomery County or a real employer.

## Live dashboard overview

The Streamlit app:
1. Downloads the official public CSV when the one-hour cache expires.
2. Normalizes source column names into a consistent reporting schema.
3. Converts fiscal years, counts and percentages to numeric fields.
4. Excludes rows missing required fields and removes duplicate summary rows.
5. Provides filters for fiscal year and report section.
6. Displays executive summaries, request mix, contact-source and department views, survey summary rows, and the selected source records.

If the public source is unavailable or its required schema changes, the app displays an error. It does not silently switch to generated data.

## Public-data fields

| Normalized field | Description |
|---|---|
| `Fiscal_Year` | Fiscal year in the published report |
| `Report_Group` | Report section or summary group |
| `Item` | Request type, source, department or other listed item |
| `Total_Count` | Published count |
| `Percentage` | Published percentage where available |
| `Description` | Optional source description |

## Data quality handling

The public-data loader:
- Identifies source columns using normalized header aliases.
- Raises a schema error if a required field cannot be mapped.
- Converts numeric fields explicitly and excludes unusable rows.
- Removes duplicate summary rows using fiscal year, report group, item and count.
- Returns an audit report with loaded, invalid, duplicate and cleaned row counts.

See [data_dictionary.md](data_dictionary.md) and [docs/public-data-source.md](docs/public-data-source.md).

## What the public source can—and cannot—measure

The published summaries support analysis of:
- Request categories and counts.
- Contact counts by source.
- Published counts by department.
- Survey summary rows.
- Fiscal-year comparisons where categories are comparable.

The public source does **not** provide individual ticket IDs, per-ticket created/resolved timestamps, SLA targets, agent-level outcomes or individual CSAT scores. Therefore, this live dashboard does not calculate MTTR, ticket-level SLA adherence, agent productivity, repeat-ticket rate or average CSAT from the public dataset.

Do not add totals from different report groups together without checking their definitions; sections may overlap.

## Legacy synthetic ticket exercise

The repository retains files from an earlier synthetic ticket-level practice project, including `Helpdesk_Tickets_Dataset_Raw.csv`, `Helpdesk_Tickets_Dataset_Raw.xlsx` and `generate_dataset.py`. These are not loaded by the current live Streamlit app.

The earlier exercise used 1,020 synthetic rows, including 20 intentional duplicate or null rows, and demonstrated ticket-level calculations such as SLA adherence, CSAT and repeat-ticket rate. Its reported sample values (91.2% SLA adherence, 3.73/5 average CSAT and 12% repeat-ticket rate) belong only to that synthetic exercise. They are not results from the official public dataset.

The legacy SQL examples in `sql_analysis.sql` are also retained for learning and are not used to produce the live dashboard.

## Run locally

Python 3.10+ recommended.

```bash
git clone https://github.com/sajidmanzoor730/helpdesk-kpi-dashboard.git
cd helpdesk-kpi-dashboard
pip install -r requirements.txt
streamlit run app.py
```

The app requires internet access to retrieve the official public CSV.

## Main files

| File | Purpose |
|---|---|
| `app.py` | Streamlit application and report views |
| `clean_tickets.py` | Public CSV loading, normalization and validation |
| `requirements.txt` | Python dependencies |
| `data_dictionary.md` | Normalized field definitions and limitations |
| `docs/public-data-source.md` | Public-source provenance and boundaries |
| `bi_validation_and_monitoring.md` | BI validation and monitoring design notes |
| `powerbi_model_spec.md` | Semantic model design notes |
| `sql_analysis.sql` | Legacy synthetic-data SQL examples, not used by the live app |

## What this project demonstrates

- Working with a published open-data source.
- Building a resilient CSV ingestion and normalization step.
- Applying explicit data-quality checks and duplicate handling.
- Designing interactive Streamlit reporting views.
- Separating supported measures from metrics the source cannot substantiate.
- Documenting provenance and limitations for non-technical readers.

---

Built by **Sajid Manzoor** · Technical Support & Operations Analytics
