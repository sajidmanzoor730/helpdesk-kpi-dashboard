# Data Dictionary — Public MCG HelpIT Summary Data

## Source

Montgomery County Government's public **MCG HelpIT Tickets** dataset:
https://data.montgomerycountymd.gov/d/qzr8-h9x6

The dashboard fetches the published CSV at runtime. This is aggregated public reporting data, not a row-per-ticket export.

## Normalized fields used by the dashboard

| Field | Meaning |
|---|---|
| Fiscal_Year | Fiscal year from the published source |
| Report_Group | Report section or summary grouping |
| Item | Category, channel, department, or other item listed within a report group |
| Total_Count | Published count, parsed as numeric |
| Percentage | Published percentage where provided |
| Description | Optional description field if the source exposes one |

The loader normalizes source column names to these fields. If required columns cannot be identified, it raises an explicit schema error rather than substituting generated data.

## Data-quality checks

- Coerce fiscal year and count fields to numeric values.
- Exclude rows without a usable fiscal year, count, report group, or item.
- Remove duplicate summary rows with the same fiscal year, report group, item, and count.
- Report loaded, invalid, duplicate, and cleaned row counts in the dashboard.

## Limitations

The source is aggregated. It does not provide individual ticket IDs, per-ticket created/resolved timestamps, SLA targets, agent-level outcomes, or individual CSAT scores. As a result, the dashboard does not calculate MTTR, SLA adherence, agent productivity, repeat-ticket rate, or average CSAT as if those were measured ticket-level facts.

The old Helpdesk_Tickets_Dataset_Raw.csv and generate_dataset.py belong to an earlier synthetic demonstration and are not used by the live dashboard.