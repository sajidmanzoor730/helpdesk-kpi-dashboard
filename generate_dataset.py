"""
Generate a SIMULATED helpdesk ticket dataset (about 5,000 tickets, 6 months).

The data is synthetic. It is built to follow typical helpdesk patterns:
weekday and business-hour peaks, priority mix, longer resolution for
low priority, more SLA breaches on P1, lower CSAT after a breach, and a
few deliberate data problems (duplicates, blanks) for the cleaning step.

Run:  python generate_dataset.py
Out:  Helpdesk_Tickets_Dataset_Raw.csv
      Helpdesk_Tickets_Dataset_Raw.xlsx
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 5000
START, END = pd.Timestamp("2026-03-01"), pd.Timestamp("2026-08-31")

# ---- created time: weekday and business-hour heavy --------------------
days = pd.date_range(START, END, freq="D")
day_w = np.array([1.0 if d.weekday() < 5 else 0.25 for d in days])
day_w *= 1 + 0.15 * np.sin(np.linspace(0, 3 * np.pi, len(days)))  # mild waves
day_w /= day_w.sum()
hour_w = np.array([0.5, 0.3, 0.2, 0.2, 0.3, 0.6, 1.2, 2.5, 5, 7, 7.5, 7,
                   5.5, 6, 7, 6.5, 5.5, 4, 3, 2.2, 1.5, 1.2, 0.9, 0.6])
hour_w /= hour_w.sum()

created = (
    rng.choice(days, N, p=day_w)
    + rng.choice(24, N, p=hour_w).astype("timedelta64[h]")
    + rng.integers(0, 60, N).astype("timedelta64[m]")
)

# ---- attributes -------------------------------------------------------
priority = rng.choice(["P1", "P2", "P3", "P4"], N, p=[0.05, 0.15, 0.45, 0.35])
category = rng.choice(
    ["Network", "Software", "Hardware", "Access/Password", "Email", "VPN", "Other"],
    N, p=[0.14, 0.24, 0.12, 0.22, 0.12, 0.10, 0.06])
channel = rng.choice(["Email", "Phone", "Chat", "Portal"], N, p=[0.30, 0.25, 0.25, 0.20])

agents = {
    "L1": ["Aisha K.", "Rohan M.", "Priya S.", "Imran D.", "Neha T.", "Karan V."],
    "L2": ["Sana R.", "Vikram P.", "Meera J."],
    "Network": ["Arjun B.", "Farah L."],
    "Infra": ["Deepak N.", "Zoya H."],
}
team = np.where(np.isin(priority, ["P1", "P2"]),
                rng.choice(["L2", "Network", "Infra"], N, p=[0.4, 0.35, 0.25]),
                rng.choice(["L1", "L2"], N, p=[0.85, 0.15]))
agent = np.array([rng.choice(agents[t]) for t in team])

# ---- SLA and resolution time (hours) ----------------------------------
sla_target = pd.Series(priority).map({"P1": 4, "P2": 8, "P3": 24, "P4": 72}).to_numpy()
median_frac = pd.Series(priority).map({"P1": 0.55, "P2": 0.5, "P3": 0.4, "P4": 0.35}).to_numpy()
sigma = pd.Series(priority).map({"P1": 0.75, "P2": 0.6, "P3": 0.55, "P4": 0.55}).to_numpy()
res_hours = sla_target * median_frac * rng.lognormal(0, sigma)
res_hours = np.round(res_hours, 1)
breach = res_hours > sla_target

# ---- status and resolved time -----------------------------------------
status = rng.choice(["Resolved", "Closed", "Pending", "Open"], N, p=[0.55, 0.37, 0.05, 0.03])
open_mask = np.isin(status, ["Pending", "Open"])
resolved_at = created + (res_hours * 60).astype("timedelta64[m]")
resolved_at = pd.Series(resolved_at)
resolved_at[open_mask] = pd.NaT
res_hours_out = pd.Series(res_hours)
res_hours_out[open_mask] = np.nan
breach_out = pd.Series(np.where(breach, "Yes", "No"))
breach_out[open_mask] = "No"

# ---- CSAT: lower after a breach, about 30% left blank ------------------
csat = np.where(breach,
                rng.choice([1, 2, 3, 4, 5], N, p=[0.15, 0.25, 0.30, 0.20, 0.10]),
                rng.choice([1, 2, 3, 4, 5], N, p=[0.02, 0.05, 0.18, 0.40, 0.35])).astype(float)
csat[rng.random(N) < 0.30] = np.nan
csat[open_mask] = np.nan

is_repeat = np.where(rng.random(N) < 0.11, "Yes", "No")

df = pd.DataFrame({
    "Ticket_ID": [f"TKT-{100000 + i}" for i in range(N)],
    "Created_At": created,
    "Resolved_At": resolved_at,
    "Priority": priority,
    "Category": category,
    "Channel": channel,
    "Team": team,
    "Agent": agent,
    "Status": status,
    "SLA_Target_Hours": sla_target,
    "Resolution_Hours": res_hours_out,
    "SLA_Breach": breach_out,
    "CSAT": csat,
    "Is_Repeat": is_repeat,
}).sort_values("Created_At").reset_index(drop=True)

# ---- deliberate data problems for the cleaning step --------------------
dups = df.sample(int(0.02 * N), random_state=1)
df = pd.concat([df, dups], ignore_index=True)
df.loc[df.sample(frac=0.015, random_state=2).index, "Category"] = np.nan
df.loc[df.sample(frac=0.01, random_state=3).index, "Agent"] = np.nan
df = df.sample(frac=1, random_state=4).reset_index(drop=True)

df.to_csv("Helpdesk_Tickets_Dataset_Raw.csv", index=False)
df.to_excel("Helpdesk_Tickets_Dataset_Raw.xlsx", index=False)

closed = df.drop_duplicates("Ticket_ID")
closed = closed[closed["Status"].isin(["Resolved", "Closed"])]
print(f"Rows written: {len(df)} (unique tickets: {df['Ticket_ID'].nunique()})")
print(f"SLA adherence (resolved/closed): {(closed['SLA_Breach'] == 'No').mean():.1%}")
print(f"Avg CSAT: {closed['CSAT'].mean():.2f}")
print(f"Repeat rate: {(closed['Is_Repeat'] == 'Yes').mean():.1%}")
print(closed.groupby('Priority')['SLA_Breach'].apply(lambda s: (s == 'Yes').mean()).round(3))
