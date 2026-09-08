"""
clean_tickets.py
Loads the raw helpdesk ticket dataset, profiles data quality issues,
cleans the data, flags SLA breaches, and calculates key KPIs.

Usage:
    python clean_tickets.py
"""
import pandas as pd

FILE_PATH = "Helpdesk_Tickets_Dataset_1000.xlsx"

# ---------- 1. Load ----------
df = pd.read_excel(FILE_PATH, sheet_name="Tickets_Raw")

print("=" * 50)
print("DATA QUALITY PROFILE (before cleaning)")
print("=" * 50)
print(f"Total rows: {len(df)}")
print(f"Duplicate Ticket_IDs: {df.duplicated(subset='Ticket_ID').sum()}")
print("\nNull values per column:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# ---------- 2. Clean ----------
df_clean = df.drop_duplicates(subset=["Ticket_ID"]).copy()

df_clean["CSAT_Score"] = df_clean["CSAT_Score"].fillna(df_clean["CSAT_Score"].median())
df_clean["Category"] = df_clean["Category"].fillna("Unknown")

print("\n" + "=" * 50)
print("DATA QUALITY PROFILE (after cleaning)")
print("=" * 50)
print(f"Total rows: {len(df_clean)}")
print(f"Remaining nulls:\n{df_clean.isnull().sum()[df_clean.isnull().sum() > 0]}")

# ---------- 3. Flag P1 SLA breaches ----------
p1_breaches = df_clean[(df_clean["Priority"] == "P1") & (df_clean["SLA_Breach"] == 1)]
print(f"\nFlagged P1 SLA breaches: {len(p1_breaches)}")

# ---------- 4. KPIs ----------
sla_adherence_pct = (1 - df_clean["SLA_Breach"].mean()) * 100
avg_csat = df_clean["CSAT_Score"].mean()
avg_mttr = df_clean["Resolution_Time_Hours"].mean()
repeat_pct = df_clean["Is_Repeat_Ticket"].mean() * 100

print("\n" + "=" * 50)
print("KEY PERFORMANCE INDICATORS")
print("=" * 50)
print(f"SLA Adherence %: {sla_adherence_pct:.1f}%")
print(f"Avg CSAT: {avg_csat:.2f} / 5")
print(f"Avg MTTR (Resolution Time): {avg_mttr:.1f} hours")
print(f"Repeat Ticket %: {repeat_pct:.1f}%")

# ---------- 5. Save cleaned output ----------
df_clean.to_excel("Tickets_Cleaned.xlsx", index=False)
print("\nCleaned file saved as Tickets_Cleaned.xlsx")
