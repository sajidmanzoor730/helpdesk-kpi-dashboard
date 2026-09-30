# Helpdesk Ticket KPI Dashboard

An end-to-end business intelligence demonstration for support operations. The project takes a realistic helpdesk-style source export through data quality checks, Python ETL, SQL analysis, dimensional modeling and BI reporting.

> **Data provenance:** The dataset is synthetic demonstration data modeled on a typical enterprise helpdesk export. It contains no customer, employer or confidential production records.

## Start here

| Area | File / page | What to inspect |
|---|---|---|
| Project overview | `README.md` | Architecture, business questions and scope |
| Source data | `Helpdesk_Tickets_Dataset_Raw.csv` | 3,672 raw rows / 3,600 unique tickets |
| ETL | `clean_tickets.py` | Cleaning, validation and derived fields |
| Quality checks | `quality_checks.py` | Automated validation rules |
| SQL | `sql_analysis.sql` | KPIs, trends, rankings and exceptions |
| Data model | `data_model.sql` | Star-schema table design |
| Power BI | `powerbi_model_spec.md` | Semantic model, measures and report pages |
| BI validation | `bi_validation_and_monitoring.md` | KPI reconciliation, QA gates and monitoring design |
| Data dictionary | `data_dictionary.md` | Source and derived field definitions |
| Dashboard | `app.py` | Interactive Streamlit reporting |
| Generator | `generate_dataset.py` | Reproducible source-data generation |
| Portfolio case study | GitHub Pages | Visual case study and project walkthrough |

## BI solution architecture

```
Helpdesk-style source export
        |
        v
Python ETL
- type normalization
- duplicate control
- missing-value handling
- date validation
- derived reporting fields
        |
        v
Curated ticket-level dataset
        |
        +-----------------------+
        |                       |
        v                       v
SQL analytical layer       Power BI / Streamlit
- KPI queries             - Executive overview
- trend analysis          - SLA & operations
- RANK / LAG              - Demand & workload
- exception queue         - Team performance
        |                       |
        +-----------+-----------+
                    v
             Business review
```

## Business questions

- Are support teams meeting SLA commitments?
- Which priorities and teams have the highest breach rates?
- Is first-response or resolution time changing over time?
- Which categories generate repeat demand or reopen activity?
- Which channels and customer segments generate the most volume?
- What operational reasons are associated with SLA breaches?
- Which team/agent patterns require further investigation?

## Source dataset

The committed demonstration export contains:

- **3,672 raw rows**
- **3,600 unique tickets**
- **March–August 2026**
- deliberate duplicate rows for ETL testing
- controlled missing Category and Agent values
- weekday/business-hour workload variation
- P1–P4 priorities
- multiple support teams and agents
- Portal, Email, Chat and Phone channels
- customer/account segments and regions
- first-response and resolution times
- SLA targets and breach reasons
- reopen and escalation indicators
- CSAT and repeat-ticket flags
- contact reason and root-cause fields

The richer schema is intended to resemble the shape of an operational export rather than a small classroom table.

## Current demonstration KPIs

Using the committed source export, the headline reporting layer currently shows approximately:

| KPI | Result |
|---|---:|
| SLA adherence | 90.5% |
| P1 SLA breach rate | 36.5% |
| P4 SLA breach rate | 7.7% |
| Average CSAT | 3.77 / 5 |
| Repeat-ticket rate | 9.2% |

These values are demonstration outputs, not production business results.

## Data quality workflow

The ETL layer:

1. reads the CSV source export;
2. standardizes categorical fields;
3. removes duplicate Ticket_ID records;
4. handles controlled missing Category/Agent values;
5. rejects impossible resolution timestamps;
6. derives Month, Week_Start, Hour and Day_Name;
7. calculates SLA variance;
8. produces an auditable quality report.

## SQL analysis

The SQL layer includes:

- `ROW_NUMBER()` for duplicate control;
- SLA policy `JOIN`;
- KPI aggregations;
- monthly `LAG()` trend comparison;
- agent `RANK()` within teams;
- repeat/reopen analysis;
- channel and customer-segment analysis;
- high-priority exception reporting.

## BI semantic model

The Power BI design uses a star schema:

**FactTickets**

surrounded by:

**DimDate · DimAgent · DimCategory · DimPriority · DimChannel · DimSegment · DimRegion**

See `powerbi_model_spec.md` for the relationships, reusable DAX measures, report pages and data-quality design.

## BI validation and monitoring

The project includes a practical validation layer covering source-to-report KPI reconciliation, data-quality gates, refresh metrics and report-performance practices. These controls are documented for the portfolio implementation; no production gateway, scheduled refresh service or alerting system is claimed.

See `bi_validation_and_monitoring.md`.

## Data dictionary

See `data_dictionary.md` for the source fields, derived ETL fields and data-quality behavior.

## Interactive dashboard

Run locally:

```bash
pip install -r requirements.txt
python clean_tickets.py
python quality_checks.py
streamlit run app.py
```

The dashboard is organized into:

1. **Executive overview**
2. **SLA & operations**
3. **Demand & workload**
4. **Team performance**
5. **ETL & data-quality audit**
6. **BI semantic model**

## Repository structure

```text
Helpdesk_Tickets_Dataset_Raw.csv   source export
generate_dataset.py                source-data generator
clean_tickets.py                   Python ETL
quality_checks.py                  automated QA checks
sql_analysis.sql                   analytical SQL
data_model.sql                     dimensional model
powerbi_model_spec.md              Power BI design
bi_validation_and_monitoring.md     BI validation and monitoring
data_dictionary.md                 field definitions
app.py                             Streamlit dashboard
bi_requirements.md                 business requirements
README.md                          project documentation
```

## Portfolio presentation

The project is presented on the portfolio as a separate case study, with the BI semantic model split into its own page so the main analysis remains easy to scan.

## Integrity note

This project deliberately uses synthetic demonstration data. It is designed to demonstrate analytics methods, data modeling, BI thinking and reporting workflow without exposing customer, employer or confidential production information.

## Author

Sajid Manzoor
