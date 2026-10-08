# 📊 Helpdesk KPI Analytics Dashboard

**End-to-end Data Analyst project:** clean operational ticket data → validate quality → analyze with SQL/Python → calculate support KPIs → communicate findings through dashboards.

**Live Dashboard:** https://hedesk-dashboard.streamlit.app/

**Portfolio case study:** https://sajidmanzoor730.github.io/sajid-portfolio/helpdesk-kpi-dashboard.html

**Core skills demonstrated:** SQL · Python/Pandas · Power BI · KPI Reporting · Data Quality · Operational Analytics

**Stack:** Python · Pandas · SQL · Power BI · Streamlit · Excel

---

## 🎯 Business Problem

Support teams need reliable answers to a few practical questions: Are tickets meeting SLA? Where is performance under pressure? Are repeat issues increasing? Can management trust the reported KPIs?

This project treats the dashboard as the final step of the analysis, not the starting point. The source data is profiled, cleaned, validated, analyzed, and then converted into operational KPIs.

## 📌 Project Overview

This project analyzes structured helpdesk ticket data to understand support performance, SLA adherence, customer satisfaction, repeat tickets, resolution trends, and data quality.

The workflow starts with a structured ticket export, cleans and validates the data using Python and Pandas, performs analytical queries using SQL, calculates operational KPIs, and presents the results through Power BI and Streamlit dashboards.

### Analytics Workflow

**Raw Ticket Data → Data Cleaning → Data Validation → SQL Analysis → KPI Calculation → Power BI + Streamlit**

---

## 🧹 Data Cleaning

The project includes a dedicated data-cleaning workflow using Python and Pandas.

The cleaning process handles:

- Duplicate ticket records
- Missing values
- Data validation
- Data type consistency
- Ticket-level validation
- KPI preparation
- Structured output for analysis

The raw export contains data-quality issues that are identified and addressed before the final KPI analysis.

### Dataset

**Disclosure:** This is a synthetic demonstration dataset created for portfolio analytics and validation. It is not a production company export or real customer data.

**Source files:** `Helpdesk_Tickets_Dataset_Raw.csv` and `Helpdesk_Tickets_Dataset_Raw.xlsx`

**Coverage:** March–August 2026

**Raw records:** 3,672

**Unique tickets after cleaning:** 3,600

### Main Fields

| Column | Description |
|---|---|
| `Ticket_ID` | Unique ticket identifier |
| `Priority` | Ticket priority from P1 to P4 |
| `Category` | Support issue category |
| `Status` | Current ticket status |
| `SLA_Breach` | Indicates whether the SLA was breached |
| `CSAT` | Customer satisfaction score |
| `Is_Repeat` | Indicates whether the ticket is a repeat issue |

---

## 📈 KPI Analysis

The dashboard focuses on the following support-performance metrics.

### SLA Adherence

Measures the percentage of tickets handled within the defined SLA.

The analysis also compares SLA performance across ticket priorities to identify where higher-priority tickets experience greater SLA pressure.

### Customer Satisfaction

Tracks average CSAT scores on a 1–5 scale and allows satisfaction to be analyzed alongside ticket priority and support performance.

### Repeat Tickets

Measures the proportion of tickets identified as repeat issues.

This helps highlight recurring customer or operational problems that may require root-cause analysis.

### Mean Time to Resolution

MTTR is used to analyze how long tickets take to resolve and how resolution time changes across different priority levels.

### Data Quality

Data-quality checks are performed before KPI reporting to ensure duplicate, incomplete, or inconsistent records do not distort the analysis.

---

## 💡 Key Findings & Business Takeaways

The analysis highlights several support-performance patterns:

- SLA adherence: **90.5%**
- P1 SLA breach rate: **36.5%**
- P4 SLA breach rate: **7.7%**
- Average CSAT: **3.77 / 5**
- Repeat-ticket rate: **9.2%**
- Source-data quality: **95.1%**

**Business takeaway:** P1 tickets have substantially higher SLA pressure than P4 tickets, so priority-level SLA monitoring is more useful than looking only at an overall SLA percentage. The analysis also shows why data-quality checks should happen before KPI reporting: duplicate and incomplete records can distort operational metrics.

---

## 🗄️ SQL Analysis

SQL is used to perform the analytical layer of the project.

The analysis includes:

- Aggregations
- `GROUP BY`
- Filtering
- KPI calculations
- Priority-level comparisons
- Ticket trend analysis
- Resolution-time analysis
- Window functions

### SQL Techniques

- `ROW_NUMBER()`
- `LAG()`
- `RANK()`
- `JOIN`
- `GROUP BY`
- `COUNT()`
- `AVG()`
- `CASE`

`ROW_NUMBER()` is used for duplicate-ticket handling, while `LAG()` and other window functions support period-level and comparative analysis.

---

## 🐍 Python Analysis

Python and Pandas are used for data preparation, cleaning, validation, and analytical processing.

The workflow includes:

1. Loading the ticket dataset
2. Inspecting the raw data
3. Detecting duplicate records
4. Checking missing values
5. Validating fields
6. Cleaning the dataset
7. Preparing analytical columns
8. Calculating KPIs
9. Passing the validated data into the dashboard workflow

---

## 📊 Power BI Dashboard

The Power BI component provides an interactive reporting layer for the helpdesk analysis.

The dashboard focuses on:

- Ticket volume
- SLA performance
- CSAT
- Repeat tickets
- Resolution time
- Priority distribution
- Operational trends

The goal is to make support performance easier to monitor and identify areas requiring further investigation.

---

## 🌐 Streamlit Dashboard

The project also includes a live Streamlit dashboard for interactive exploration.

### Live Demo

**https://hedesk-dashboard.streamlit.app/**

The dashboard allows users to explore the cleaned ticket data and review calculated support KPIs.

---

## 🖼️ Dashboard Preview

### Operational KPI Dashboard

![Helpdesk KPI dashboard](dashboard.jpg)

### Priority Distribution

![Priority distribution](priority_distribution.png)

---

## 🧪 Data Validation

Data validation is an important part of the project because inaccurate source data can directly affect KPI reporting.

Validation checks include:

- Duplicate detection
- Missing-value checks
- Ticket ID validation
- Date-field validation
- Priority and SLA validation
- Field consistency
- KPI validation
- Cleaned-data verification

The validation workflow identified:

- **72 duplicate ticket rows**
- **66 blank Category values**
- **43 blank Agent values**

The resulting source-data quality score was **95.1%** before the final analytical workflow.

---

## 📁 Project Files

The repository contains the main components used in the analytics workflow:

- `clean_tickets.py` — data-cleaning workflow
- `sql_analysis.sql` — SQL analysis
- `app.py` — Streamlit dashboard
- `generate_dataset.py` — reproducible data preparation script
- `data_dictionary.md` — field definitions and data documentation
- `requirements.txt` — Python dependencies
- `tests/` — automated project tests
- `docs/` — supporting documentation
- `priority_distribution.png` — dashboard visualization
- `README.md` — project documentation

---

## 🚀 Run Locally

Clone the repository:

```bash
git clone https://github.com/sajidmanzoor730/helpdesk-kpi-dashboard.git
```

Move into the project directory:

```bash
cd helpdesk-kpi-dashboard
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the data-cleaning workflow:

```bash
python clean_tickets.py
```

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

The dashboard will then be available through the local Streamlit URL shown in the terminal.

---

## 🛠️ Technologies

### Data Analysis

- Python
- Pandas
- NumPy

### SQL

- SQL
- Aggregations
- CTEs
- Window Functions
- JOINs
- Data filtering
- KPI calculations

### Business Intelligence

- Power BI
- KPI dashboards
- Interactive reporting
- Operational analysis

### Dashboarding

- Streamlit

### Data Quality

- Duplicate detection
- Missing-value validation
- Data reconciliation
- Data validation
- Documentation

---

## 📚 Documentation

The repository includes supporting documentation covering:

- Data dictionary
- Data-cleaning workflow
- SQL analysis
- Validation checks
- Dashboard workflow
- Testing
- Project decisions

---

## 🎯 What This Project Demonstrates

This project demonstrates an end-to-end **Data Analyst workflow**, rather than only dashboard creation.

It shows how to:

**Clean → Validate → Analyze → Calculate KPIs → Visualize → Communicate**

The project is focused on operational analytics and support-performance reporting, with an emphasis on trustworthy KPI definitions and business interpretation.

Relevant areas include:

- Data Analysis
- Operations Analytics
- Business Intelligence
- KPI Reporting
- Data Quality
- Support Analytics

---

## 👤 About

**Sajid Manzoor**

Data Analyst focused on:

- SQL
- Python
- Pandas
- Power BI
- Excel
- KPI Reporting
- Data Quality
- Operational Analytics

**LinkedIn:** https://www.linkedin.com/in/sajid-manzoor-730zz/

**GitHub:** https://github.com/sajidmanzoor730

---

## 🤝 Let's Connect

Interested in data analytics, KPI reporting, operational analytics, or business intelligence?

[Connect with me on LinkedIn](https://www.linkedin.com/in/sajid-manzoor-730zz/)

---

*Built by Sajid Manzoor*
