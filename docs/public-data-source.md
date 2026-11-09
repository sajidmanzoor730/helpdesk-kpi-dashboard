# Public Helpdesk Data Source Notes

This repository's Streamlit ticket-level dashboard is a synthetic practice exercise. Its ticket rows and calculated ticket KPIs must not be presented as results from the Montgomery County source.

## Official public source

**MCG HelpIT Tickets — Montgomery County Government Open Data**  
https://data.montgomerycountymd.gov/d/qzr8-h9x6

The public source contains aggregated summary rows grouped by fiscal year, report section and item. It includes published counts and percentages where available.

## What can be analyzed

- Published request-type counts, including categories such as Email Support and VPN.
- Contact counts by source.
- Published contact counts by department.
- Survey summary rows as reported by the source.
- Differences across fiscal years where comparable rows are available.

## What the source does not provide

- Individual ticket IDs or ticket-level records.
- Ticket-level timestamps or agent records.
- SLA targets or ticket-level SLA performance.
- Individual CSAT ratings.

Survey summary counts are not equivalent to individual CSAT scores. Do not combine totals from different report sections because sections may overlap.

## How to keep the projects separate

1. Use the synthetic ticket dataset only to demonstrate ticket-level cleaning, KPI calculations and dashboard mechanics.
2. Use the official MCG aggregated source for the public-data helpdesk case study.
3. Label each chart, table and result with its actual source.
4. If the public source is unavailable, show an error rather than silently substituting generated data.
