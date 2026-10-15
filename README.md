# Public IT Helpdesk Trends Dashboard

**End-to-end data analytics project** using a published government IT helpdesk summary dataset: source retrieval → data validation → cleaning → trend analysis → interactive dashboard.

- **Live dashboard:** https://hedesk-dashboard.streamlit.app/
- **Portfolio case study:** https://sajidmanzoor730.github.io/sajid-portfolio/helpdesk-kpi-dashboard.html
- **Official source:** [Montgomery County Government — MCG HelpIT Tickets](https://data.montgomerycountymd.gov/d/qzr8-h9x6)

## What changed

The dashboard now reads the official public source at runtime. It no longer uses the generated Helpdesk_Tickets_Dataset_Raw.csv for dashboard metrics, and it does not fall back to synthetic data if the source is unavailable. If the source cannot be loaded or its schema changes, the dashboard reports an error instead of showing fabricated results.

## What the source can support

The source contains published summary rows, grouped by fiscal year, report section and item. The dashboard reports published counts and percentages, compares fiscal years where available, and explores request types, contact sources, departments and survey-summary rows.

**Important limitation:** this is aggregated public reporting data, not individual helpdesk tickets. It does not provide ticket-level timestamps, individual agents, SLA targets, or individual customer satisfaction ratings. Therefore, this project does **not** claim actual SLA adherence, MTTR, agent productivity, repeat-ticket rate, or average CSAT from this source.

## Analytics workflow

Official public CSV → schema checks → numeric and missing-value validation → duplicate-summary checks → interactive Streamlit charts and tables.

The dashboard uses a one-hour cache. Refresh the app after the cache expires to fetch the latest source response.

## Run locally

```bash
git clone https://github.com/sajidmanzoor730/helpdesk-kpi-dashboard.git
cd helpdesk-kpi-dashboard
pip install -r requirements.txt
streamlit run app.py
```

The app needs internet access to fetch the official CSV. It will show a clear error if the endpoint is unavailable.

## Repository notes

- app.py — Streamlit dashboard and report filters.
- clean_tickets.py — official-source loader, schema normalization and data-quality checks.
- sql_analysis.sql — legacy SQL example written for the former synthetic ticket-level demonstration data; not used to calculate current live dashboard figures.
- generate_dataset.py — legacy synthetic-data generator retained as a learning artifact only; it is not the live dashboard source.
- data_dictionary.md — source fields, assumptions and limitations.

## Skills demonstrated

Python, Pandas, data ingestion, schema validation, data-quality checks, aggregation, interactive visualization, source documentation, and communicating limitations honestly.

Built by Sajid Manzoor.