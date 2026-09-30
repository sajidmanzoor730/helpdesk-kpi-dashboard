"""Generate a realistic synthetic helpdesk export for the portfolio BI project.

The dataset is demonstration data only. It models a typical enterprise support
export with natural workload variation, operational fields and controlled
data-quality issues.

Outputs:
  Helpdesk_Tickets_Dataset_Raw.csv
  Helpdesk_Tickets_Dataset_Raw.xlsx
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(260930)
N = 3600
START, END = pd.Timestamp("2026-03-01"), pd.Timestamp("2026-08-31 23:59")

categories = {
    "Access & Identity": ["Password reset", "MFA issue", "Account locked", "Permission request"],
    "Email & Collaboration": ["Mailbox", "Calendar", "Teams/Meetings", "Distribution list"],
    "Network": ["LAN connectivity", "Wi-Fi", "DNS/DHCP", "Switch port"],
    "VPN & Remote Access": ["VPN login", "VPN disconnect", "Remote desktop", "Split tunnel"],
    "Hardware": ["Laptop", "Monitor", "Docking station", "Keyboard/Mouse"],
    "Software & Applications": ["Application error", "Installation", "License", "Version issue"],
    "Endpoint Security": ["EDR alert", "Device compliance", "Malware check", "Security policy"],
    "Printing & Peripherals": ["Printer offline", "Print queue", "Scanner", "Peripheral setup"],
    "Telephony": ["Softphone", "Headset", "Extension", "Call quality"],
    "Account Provisioning": ["New starter", "Role change", "Offboarding", "Access package"],
    "Performance": ["Slow device", "High CPU", "High memory", "Disk space"],
    "Cloud & SaaS": ["SSO", "Application outage", "Integration", "Subscription"],
}
priorities = ["P1", "P2", "P3", "P4"]
sla_targets = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
channels = ["Portal", "Email", "Chat", "Phone"]
segments = ["Enterprise", "Mid-Market", "SMB", "Internal"]
regions = ["North America", "EMEA", "APAC"]
teams = ["Service Desk L1", "Service Desk L2", "Network Ops",
         "Endpoint Ops", "Identity & Access", "Business Apps"]
agents = ["Aisha Khan", "Rohan Mehta", "Priya Shah", "Imran Dar",
          "Neha Thomas", "Karan Verma", "Sana Rahman", "Vikram Patel",
          "Meera Joseph", "Arjun Bhat", "Farah Latif", "Deepak Nair",
          "Zoya Hussain", "Adil Mir", "Nadia Ali", "Kabir Singh",
          "Maya Rao", "Omar Malik"]

days = pd.date_range(START.normalize(), END.normalize(), freq="D")
rows = []

for i in range(N):
    day = rng.choice(days)
    while day.weekday() >= 5 and rng.random() > 0.12:
        day = rng.choice(days)

    hour = rng.choice(
        [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        p=[.04, .08, .11, .12, .11, .10, .10, .10, .08, .06, .04, .025, .015, .005],
    )
    created = day + pd.Timedelta(hours=int(hour), minutes=int(rng.integers(60)))

    priority = rng.choice(priorities, p=[.045, .16, .48, .315])
    category = rng.choice(list(categories))
    subcategory = rng.choice(categories[category])
    channel = rng.choice(channels, p=[.34, .28, .22, .16])
    segment = rng.choice(segments, p=[.28, .32, .25, .15])
    region = rng.choice(regions, p=[.38, .34, .28])

    if category in {"Network", "VPN & Remote Access"}:
        team = rng.choice(["Network Ops", "Service Desk L2"], p=[.72, .28])
    elif category in {"Access & Identity", "Account Provisioning", "Endpoint Security"}:
        team = rng.choice(["Identity & Access", "Service Desk L1", "Endpoint Ops"], p=[.62, .23, .15])
    elif category == "Telephony":
        team = rng.choice(["Service Desk L2", "Network Ops"], p=[.70, .30])
    elif category in {"Software & Applications", "Cloud & SaaS"}:
        team = rng.choice(["Business Apps", "Service Desk L2", "Service Desk L1"], p=[.55, .30, .15])
    else:
        team = rng.choice(teams, p=[.38, .18, .08, .16, .08, .12])

    team_agents = agents[:6] if team == "Service Desk L1" else (
        agents[6:10] if team == "Service Desk L2" else
        agents[9:13] if team == "Network Ops" else
        agents[4:8] if team == "Endpoint Ops" else
        agents[10:15] if team == "Identity & Access" else agents[2:7]
    )
    agent = rng.choice(team_agents)

    status = rng.choice(["Resolved", "Closed", "Pending", "Open"], p=[.57, .30, .09, .04])
    target = sla_targets[priority]
    complexity = {"P1": 1.15, "P2": 1.08, "P3": 1.0, "P4": .92}[priority]
    first_response = int(rng.integers(3, 22) if priority == "P1" else
                        rng.integers(8, 65) if priority == "P2" else
                        rng.integers(12, 180) if priority == "P3" else
                        rng.integers(20, 360))

    resolution = round(target * (.16 + rng.random() ** 1.8 * .72) * complexity, 2)
    if status in {"Pending", "Open"}:
        resolution = np.nan

    breach = bool(pd.notna(resolution) and resolution > target)
    resolved_at = created + pd.Timedelta(hours=float(resolution)) if pd.notna(resolution) else pd.NaT

    csat = np.nan
    if pd.notna(resolution) and rng.random() >= .13:
        base = 3.2 if breach else 4.2
        csat = float(np.clip(round(base + rng.uniform(-.8, .8)), 1, 5))

    rows.append({
        "Ticket_ID": f"HD-{created:%y%m%d}-{i + 1001:05d}",
        "Created_At": created,
        "First_Response_Minutes": first_response,
        "Resolved_At": resolved_at,
        "Priority": priority,
        "Category": category,
        "Subcategory": subcategory,
        "Channel": channel,
        "Customer_Segment": segment,
        "Team": team,
        "Agent": agent,
        "Status": status,
        "SLA_Target_Hours": target,
        "Resolution_Hours": resolution,
        "SLA_Breach": "Yes" if breach else "No",
        "Breach_Reason": rng.choice(
            ["High queue volume", "Dependency delay", "Vendor response",
             "Escalation delay", "Complex investigation", "After-hours coverage"]
        ) if breach else "None",
        "Reopen_Count": int(rng.choice([0, 1, 2, 3], p=[.72, .20, .06, .02])),
        "Escalated": "Yes" if rng.random() < (.28 if priority in {"P1", "P2"} else .08) else "No",
        "CSAT": csat,
        "Is_Repeat": "Yes" if rng.random() < .095 else "No",
        "Contact_Reason": rng.choice(
            ["Incident", "Service request", "Access request", "How-to", "Performance issue"],
            p=[.39, .25, .15, .11, .10],
        ),
        "Root_Cause": rng.choice(
            ["User error", "Configuration", "Software defect", "Network condition",
             "Access policy", "Hardware fault", "Capacity", "Vendor issue", "Unknown"],
            p=[.18, .17, .14, .12, .11, .10, .07, .06, .05],
        ),
        "Region": region,
    })

df = pd.DataFrame(rows)

# Deliberate source-data issues for the ETL exercise.
duplicates = df.sample(72, random_state=17)
df = pd.concat([df, duplicates], ignore_index=True)
df.loc[df.sample(frac=.018, random_state=18).index, "Category"] = pd.NA
df.loc[df.sample(frac=.012, random_state=19).index, "Agent"] = pd.NA
df = df.sample(frac=1, random_state=20).reset_index(drop=True)

df.to_csv("Helpdesk_Tickets_Dataset_Raw.csv", index=False)
df.to_excel("Helpdesk_Tickets_Dataset_Raw.xlsx", index=False)

print(f"Raw rows: {len(df):,}")
print(f"Unique tickets: {df['Ticket_ID'].nunique():,}")
print("Source export generated successfully.")
