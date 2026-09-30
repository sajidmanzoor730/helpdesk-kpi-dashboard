# Power BI Semantic Model & Reporting Specification

This document defines the Power BI implementation for the Helpdesk KPI Dashboard.

## 1. Model design
Use a star schema with FactTickets at the center.

### FactTickets
Grain: one row per unique Ticket_ID.
Columns: Ticket_ID, Created_Date, Agent_Key, Category_Key, Priority_Key, Channel, Status, Resolution_Hours, SLA_Breach, CSAT, Is_Repeat.

### Dimensions
DimDate: Date, Year, Month, Month Number, Week, Day Name.
DimAgent: Agent, Team.
DimCategory: Category.
DimPriority: Priority, Response Class, Target Hours.

## 2. Relationships
Recommended single-direction relationships:
- DimDate[Date] 1 → * FactTickets[Created_Date]
- DimAgent[Agent] 1 → * FactTickets[Agent]
- DimCategory[Category] 1 → * FactTickets[Category]
- DimPriority[Priority] 1 → * FactTickets[Priority]

Use dimension attributes for slicers and grouping. Keep reusable business logic in measures.

## 3. Core DAX measures

Tickets = COUNTROWS(FactTickets)

Resolved Tickets = CALCULATE([Tickets], FactTickets[Status] IN {"Resolved", "Closed"})

SLA Adherence % = DIVIDE(CALCULATE([Resolved Tickets], FactTickets[SLA_Breach] = "No"), [Resolved Tickets])

SLA Breaches = CALCULATE([Resolved Tickets], FactTickets[SLA_Breach] = "Yes")

Average Resolution Hours = AVERAGEX(FILTER(FactTickets, FactTickets[Status] IN {"Resolved", "Closed"}), FactTickets[Resolution_Hours])

Average CSAT = AVERAGEX(FILTER(FactTickets, FactTickets[Status] IN {"Resolved", "Closed"}), FactTickets[CSAT])

Repeat Ticket Rate % = DIVIDE(CALCULATE([Resolved Tickets], FactTickets[Is_Repeat] = "Yes"), [Resolved Tickets])

P1 SLA Breach % = DIVIDE(CALCULATE([SLA Breaches], FactTickets[Priority] = "P1"), CALCULATE([Resolved Tickets], FactTickets[Priority] = "P1"))

## 4. Report pages

### Executive Overview
KPI cards: Tickets, SLA Adherence %, Average Resolution Hours, Average CSAT, Repeat Ticket Rate %.
Visuals: monthly ticket trend, SLA adherence by priority, ticket volume by category, team performance.

### SLA & Operations
Visuals: SLA breach rate by priority, SLA trend by month, resolution hours by priority, P1/P2 exception table.

### Demand & Workload
Visuals: tickets by category, tickets by channel, tickets by hour/day, repeat-ticket rate by category.

### Team Performance
Table: Team, Agent, Tickets, SLA %, Average Resolution Hours, Average CSAT.
Apply a minimum-volume rule before comparing agent-level results.

## 5. Slicers
Date, Priority, Team, Category, Channel.

## 6. Data-quality page
Expose source row count, curated row count, duplicate count, invalid-date count, unassigned-agent count, missing-category count and last refresh timestamp.

## 7. Performance considerations
- Prefer a star schema over a wide flat reporting table.
- Keep reusable logic in measures where practical.
- Avoid unnecessary bi-directional relationships.
- Remove unused columns before loading the model.
- Pre-aggregate only when query volume requires it.
- Monitor refresh duration and visual/query performance.
- Validate KPI totals after every source refresh.

## 8. Business-to-report mapping
| Business need | Measure / visual |
|---|---|
| Are SLAs being met? | SLA Adherence % |
| Which priorities create risk? | SLA Breach % by Priority |
| Is resolution getting slower? | Average Resolution Hours + trend |
| Where is repeat demand concentrated? | Repeat Ticket Rate by Category |
| When is demand highest? | Tickets by Hour/Day |
| Which teams need review? | Team performance table |
| Are source data issues affecting reporting? | Data-quality page |

## 9. Implementation note
This repository documents the semantic-model and Power BI design. It should not claim an enterprise Power BI deployment, data warehouse, OLAP cube, or production refresh infrastructure unless those have actually been implemented.