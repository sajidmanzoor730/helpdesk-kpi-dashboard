# Power BI Semantic Model & Reporting Specification

## 1. Model purpose
The reporting layer turns a ticket-level operational export into a reusable BI model for support operations reviews.

## 2. Semantic model
Use a star schema with **FactTickets** at the center.

### FactTickets
Grain: one row per unique Ticket_ID.

Key analytical fields:
Ticket_ID, Created_Date, Priority_Key, Agent_Key, Category_Key, Channel_Key,
Segment_Key, Region_Key, Status, First_Response_Minutes, Resolution_Hours,
SLA_Breach, Breach_Reason, Reopen_Count, Escalated, CSAT, Is_Repeat,
Contact_Reason and Root_Cause.

### Dimensions
- **DimDate** — date, year, month, week and day.
- **DimAgent** — agent and team.
- **DimCategory** — category.
- **DimPriority** — priority, response class and SLA target.
- **DimChannel** — Portal, Email, Chat, Phone.
- **DimSegment** — customer/account segment.
- **DimRegion** — operating region.

## 3. Relationships
Use one-to-many, single-direction relationships from dimensions to FactTickets:
- DimDate → FactTickets
- DimAgent → FactTickets
- DimCategory → FactTickets
- DimPriority → FactTickets
- DimChannel → FactTickets
- DimSegment → FactTickets
- DimRegion → FactTickets

## 4. Core DAX measures

```DAX
Tickets = COUNTROWS(FactTickets)

Resolved Tickets =
CALCULATE([Tickets], FactTickets[Status] IN {"Resolved", "Closed"})

SLA Adherence % =
DIVIDE(
    CALCULATE([Resolved Tickets], FactTickets[SLA_Breach] = "No"),
    [Resolved Tickets]
)

SLA Breaches =
CALCULATE([Resolved Tickets], FactTickets[SLA_Breach] = "Yes")

Average Resolution Hours =
AVERAGEX(
    FILTER(FactTickets, FactTickets[Status] IN {"Resolved", "Closed"}),
    FactTickets[Resolution_Hours]
)

Average First Response Minutes =
AVERAGEX(
    FILTER(FactTickets, FactTickets[Status] IN {"Resolved", "Closed"}),
    FactTickets[First_Response_Minutes]
)

Average CSAT =
AVERAGEX(
    FILTER(FactTickets, FactTickets[Status] IN {"Resolved", "Closed"}),
    FactTickets[CSAT]
)

Repeat Ticket Rate % =
DIVIDE(
    CALCULATE([Resolved Tickets], FactTickets[Is_Repeat] = "Yes"),
    [Resolved Tickets]
)

Escalation Rate % =
DIVIDE(
    CALCULATE([Resolved Tickets], FactTickets[Escalated] = "Yes"),
    [Resolved Tickets]
)
```

## 5. Report pages

### Executive Overview
KPI cards for tickets, SLA adherence, resolution time, first response, CSAT,
repeat rate and escalation rate. Add monthly volume and SLA trend visuals.

### SLA & Operations
Priority-level breach rate, resolution hours, breach reasons and a P1/P2 exception table.

### Demand & Workload
Category, subcategory, channel, hour/day, customer segment and repeat-demand analysis.

### Team Performance
Team and agent table with ticket volume, SLA %, resolution hours, CSAT and escalation rate.
Use a minimum-volume threshold before comparing individual agents.

### Data Quality
Source rows, curated rows, duplicates removed, missing category/agent values,
invalid dates, open/pending volume and last refresh timestamp.

## 6. Recommended slicers
Date, Priority, Team, Category, Channel, Customer Segment and Region.

## 7. Performance considerations
- Keep the model at a clear ticket-level grain.
- Prefer reusable measures over repeated visual-level calculations.
- Avoid unnecessary bi-directional relationships.
- Remove unused columns before loading.
- Validate KPI totals against SQL after refresh.
- Monitor refresh duration and visual/query response time.

## 8. KPI validation and reconciliation

After a model refresh, compare the core measures with the SQL analytical baseline for the same filter context. At minimum validate ticket count, resolved/closed count, SLA adherence, average resolution hours, average CSAT, repeat rate and escalation rate. Investigate material differences before publishing a report update.

See `bi_validation_and_monitoring.md` for the practical control workflow.

## 9. Business question → BI output

| Business need | BI output |
|---|---|
| Are SLAs being met? | SLA Adherence % and breach trend |
| Which priorities create risk? | Breach % by Priority |
| Is response/resolution slowing? | First-response and resolution trends |
| Where is repeat demand concentrated? | Repeat rate by Category/Subcategory |
| Which channels generate demand? | Volume and SLA by Channel |
| Which teams need review? | Team/Agent performance |
| Why are SLAs missed? | Breach Reason analysis |
| Are source issues affecting reporting? | Data-quality page |

## 10. Implementation note
This repository documents the semantic-model and Power BI design for a portfolio demonstration.
It does not claim enterprise Power BI deployment, a production data warehouse, OLAP cube,
or live scheduled refresh infrastructure unless those components are actually implemented.
