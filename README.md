# 📊 Helpdesk Ticket Analytics Dashboard

An end-to-end helpdesk analytics project built to demonstrate data cleaning, SQL analysis, KPI reporting, and interactive dashboard development.

**Live Dashboard:** https://hedesk-dashboard.streamlit.app/

**Stack:** Python · Pandas · SQL · Power BI · Streamlit · Excel

---

## 📌 Project Overview

This project analyzes helpdesk ticket data to understand support performance, SLA adherence, customer satisfaction, repeat tickets, and resolution trends.

The workflow starts with a messy ticket export, cleans and validates the data using Python and Pandas, performs analytical queries using SQL, calculates operational KPIs, and presents the results through Power BI and Streamlit dashboards.

**Analytics workflow:**

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

The original project dataset contains intentionally introduced data-quality issues so the cleaning and validation workflow can be demonstrated.

### Dataset

**File:** `Helpdesk_Tickets_Dataset_1000.xlsx`

**Dataset type:** Synthetic sample data

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

Data-quality checks are performed before KPI reporting to ensure duplicate and invalid records do not distort the analysis.

---

## 📊 Key Findings

Based on the current project dataset, the analysis identified several support-performance patterns:

- SLA adherence is approximately **91.2%**.
- Higher-priority P1 tickets show significantly higher SLA-breach rates than lower-priority tickets.
- Average CSAT is approximately **3.73 / 5**.
- Repeat tickets account for approximately **12%** of the analyzed records.
- Resolution time varies by ticket priority.
- Data cleaning and validation improve the reliability of the final analytical dataset.

> **Note:** These figures come from the current synthetic project dataset and are included to demonstrate the analytical workflow. They should not be interpreted as production business metrics.

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

Example SQL techniques include:

- `ROW_NUMBER()`
- `LAG()`
- `GROUP BY`
- `COUNT()`
- `AVG()`
- `CASE`

Window functions are used to support duplicate handling and period-over-period analysis.

---

## 🐍 Python Analysis

Python and Pandas are used for data preparation and analytical processing.

The workflow includes:

1. Loading the ticket dataset
2. Inspecting the raw data
3. Detecting duplicate records
4. Checking missing values
5. Validating fields
6. Cleaning the dataset
7. Preparing analytical columns
8. Calculating KPIs
9. Passing the cleaned data into the dashboard workflow

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

The dashboard allows users to explore the cleaned ticket data and review the calculated support KPIs.

---

## 🖼️ Dashboard Preview

![Priority distribution](priority_distribution.png)

---

## 🧪 Data Validation

Data validation is an important part of the project because inaccurate source data can directly affect KPI reporting.

Validation checks include:

- Duplicate detection
- Missing-value checks
- Ticket ID validation
- Field consistency
- KPI validation
- Cleaned-data verification

The project also includes testing and documentation to make the analytical workflow easier to reproduce and review.

---

## 📁 Project Files

The repository contains the main components used in the analytics workflow:

- `clean_tickets.py` — data-cleaning workflow
- `app.py` — Streamlit dashboard
- `sql_analysis.sql` — SQL analysis
- `data_dictionary.md` — field definitions and data documentation
- `requirements.txt` — Python dependencies
- `tests/` — project tests
- `docs/` — supporting documentation
- `priority_distribution.png` — dashboard visualization
- `README.md` — project documentation

---

## 🚀 Run Locally

Clone the repository:

`git clone https://github.com/sajidmanzoor730/helpdesk-kpi-dashboard.git`

Move into the project directory:

`cd helpdesk-kpi-dashboard`

Install the required packages:

`pip install -r requirements.txt`

Run the data-cleaning workflow:

`python clean_tickets.py`

Start the Streamlit dashboard:

`streamlit run app.py`

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

This project demonstrates an end-to-end analytics workflow rather than only dashboard creation.

It shows how to:

**Clean → Validate → Analyze → Calculate KPIs → Visualize → Communicate**

The project is particularly focused on operational analytics and support-performance reporting.

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
