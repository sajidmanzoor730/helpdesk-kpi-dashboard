# Helpdesk Data Dictionary

The source export is synthetic demonstration data modeled on a typical enterprise support export.

| Field | Meaning | Example / allowed values |
|---|---|---|
| Ticket_ID | Unique support ticket identifier | HD-260301-01001 |
| Created_At | Ticket creation timestamp | 2026-03-01 09:15 |
| First_Response_Minutes | Minutes until first response | 18 |
| Resolved_At | Resolution timestamp when available | timestamp / blank |
| Priority | Support priority | P1, P2, P3, P4 |
| Category | Primary issue category | Network, Hardware, etc. |
| Subcategory | More specific issue type | VPN, Password Reset, etc. |
| Channel | Intake channel | Portal, Email, Chat, Phone |
| Customer_Segment | Account/support segment | Enterprise, Mid-Market, SMB, Internal |
| Team | Assigned support team | Service Desk L1, Network Ops, etc. |
| Agent | Assigned analyst | named synthetic agent / Unassigned |
| Status | Current ticket state | Resolved, Closed, Pending, Open |
| SLA_Target_Hours | Target resolution window | 4, 8, 24, 72 |
| Resolution_Hours | Time from creation to resolution | 3.5 |
| SLA_Breach | Whether the ticket exceeded target | Yes / No |
| Breach_Reason | Operational reason for breach | escalation, workload, dependency, etc. |
| Reopen_Count | Number of reopen events | 0, 1, 2... |
| Escalated | Whether ticket was escalated | Yes / No |
| CSAT | Customer satisfaction score | 1–5 |
| Is_Repeat | Repeat-demand indicator | Yes / No |
| Contact_Reason | Why the customer contacted support | issue type / request |
| Root_Cause | Classified underlying cause | configuration, access, hardware, etc. |
| Region | Operating region | North America, EMEA, APAC |

## Derived ETL fields

The Python ETL also derives:

- Created_Date
- Month
- Week_Start
- Hour
- Day_Name
- Is_Resolved
- SLA_Met
- SLA_Variance_Hours

## Data-quality behavior

- Duplicate Ticket_ID records are removed during ETL.
- Missing Category values become Unknown.
- Missing Agent values become Unassigned.
- Impossible resolution timestamps are rejected.
- Quality checks validate controlled categorical values and CSAT range.
