# BI Requirements & Solution Design

## Business context

The dashboard is designed for a support operations manager who needs a consistent view of ticket volume, SLA performance, resolution efficiency, customer satisfaction, repeat demand, and workload patterns.

The source is a synthetic demonstration export modeled on a typical enterprise helpdesk feed. It does not contain customer or employer production data.

## Business questions

| Business question | BI output |
|---|---|
| Are support teams meeting SLA commitments? | SLA adherence and breach-rate KPIs |
| Which priorities create the greatest operational risk? | Priority-level SLA and resolution analysis |
| How is support demand changing over time? | Weekly/monthly volume trends |
| Where is repeat demand concentrated? | Repeat-ticket rate by category |
| Are workload patterns affecting staffing? | Ticket volume by hour/day |
| Which agent/team patterns require review? | Team and agent performance table |

## Solution architecture

```
Raw Excel / CSV Export
        |
        v
Python ETL
- type normalization
- duplicate control
- missing-value handling
- chronology validation
- derived reporting fields
        |
        v
Curated Analytical Dataset
        |
        +----------------------+
        |                      |
        v                      v
SQL Analytical Layer       Power BI / Streamlit
- KPI queries             - KPI cards
- trends                 - filters
- rankings               - drill-down analysis
- exception lists        - operational views
        |
        v
Business Review
- SLA exceptions
- repeat-demand drivers
- workload patterns
- team/agent follow-up
```

## Reporting principles

- KPI definitions are kept consistent between Python, SQL, and the dashboard.
- Duplicate Ticket_ID records are removed before KPI calculation.
- Missing dimensions are assigned controlled values rather than silently discarded.
- Impossible date sequences are rejected and counted in the quality report.
- Closed/resolved tickets are used for resolution-based KPIs.
- The dashboard supports filtering by date, priority, and team.

## Analytical model

The intended reporting model follows a dimensional structure:

- **FactTickets** — one row per unique ticket.
- **DimDate** — reporting calendar.
- **DimAgent** — agent/team attributes.
- **DimCategory** — support category.
- **DimPriority** — priority and SLA target attributes.
- **DimChannel** — intake channel.
- **DimSegment** — customer/account segment.
- **DimRegion** — operating region.

This structure separates transactional facts from reusable reporting dimensions and is suitable for a Power BI tabular/semantic model.

## Data-quality controls

Before reporting, validate:

1. Ticket_ID uniqueness.
2. Required date fields.
3. Resolved_At >= Created_At when a resolution exists.
4. Valid priority values.
5. Valid SLA status values.
6. Controlled handling of missing category/agent values.
7. Row-count reconciliation from raw to curated data.
8. KPI reconciliation between Python and SQL.

## Performance checks

For a production implementation, the refresh process should monitor:

- source row count
- curated row count
- duplicate count
- rejected-record count
- refresh duration
- query/report response time
- unexpected KPI movement

Thresholds should be agreed with the business owner rather than hard-coded without operational context.
