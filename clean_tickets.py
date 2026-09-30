"""
Clean the simulated helpdesk ticket export.

Steps: remove duplicate tickets, fill blank category/agent, parse dates,
check resolved time is after created time, and report data quality.

Run:  python clean_tickets.py
Out:  Helpdesk_Tickets_Clean.csv
"""
import pandas as pd

RAW_FILE = "Helpdesk_Tickets_Dataset_Raw.xlsx"
CLEAN_FILE = "Helpdesk_Tickets_Clean.csv"


def load_and_clean(path=RAW_FILE):
    raw = pd.read_excel(path, parse_dates=["Created_At", "Resolved_At"])
    report = {"raw_rows": len(raw)}

    df = raw.drop_duplicates(subset="Ticket_ID", keep="first").copy()
    report["duplicates_removed"] = report["raw_rows"] - len(df)

    report["blank_category"] = int(df["Category"].isna().sum())
    report["blank_agent"] = int(df["Agent"].isna().sum())
    df["Category"] = df["Category"].fillna("Unknown")
    df["Agent"] = df["Agent"].fillna("Unassigned")

    bad_dates = df["Resolved_At"].notna() & (df["Resolved_At"] < df["Created_At"])
    report["bad_dates_removed"] = int(bad_dates.sum())
    df = df[~bad_dates]

    df["Month"] = df["Created_At"].dt.to_period("M").astype(str)
    df["Week"] = df["Created_At"].dt.to_period("W").dt.start_time
    df["Hour"] = df["Created_At"].dt.hour

    issues = report["duplicates_removed"] + report["blank_category"] + report["blank_agent"]
    report["clean_rows"] = len(df)
    report["data_quality_pct"] = round(100 * (1 - issues / report["raw_rows"]), 1)
    return df.reset_index(drop=True), report


if __name__ == "__main__":
    clean, rep = load_and_clean()
    clean.to_csv(CLEAN_FILE, index=False)
    for k, v in rep.items():
        print(f"{k}: {v}")
    print(f"Saved {CLEAN_FILE}")
