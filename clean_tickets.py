"""ETL and validation layer for the Helpdesk KPI demonstration.

The committed CSV is the primary source so the Streamlit app works directly
from the repository. The generator can also create an Excel copy locally.
"""

from pathlib import Path
import pandas as pd

RAW_CSV = "Helpdesk_Tickets_Dataset_Raw.csv"
RAW_XLSX = "Helpdesk_Tickets_Dataset_Raw.xlsx"
CLEAN_FILE = "Helpdesk_Tickets_Clean.csv"


def load_raw(path=None):
    source = Path(path or RAW_CSV)
    if source.suffix.lower() == ".xlsx":
        return pd.read_excel(source, parse_dates=["Created_At", "Resolved_At"])
    return pd.read_csv(source, parse_dates=["Created_At", "Resolved_At"])


def load_and_clean(path=None):
    raw = load_raw(path)
    report = {"raw_rows": len(raw), "raw_columns": len(raw.columns)}

    text_columns = [
        "Ticket_ID", "Priority", "Category", "Subcategory", "Channel",
        "Customer_Segment", "Team", "Agent", "Status", "SLA_Breach",
        "Breach_Reason", "Escalated", "Is_Repeat", "Contact_Reason",
        "Root_Cause", "Region",
    ]
    for column in text_columns:
        if column in raw.columns:
            raw[column] = raw[column].astype("string").str.strip()

    df = raw.drop_duplicates(subset="Ticket_ID", keep="first").copy()
    report["duplicates_removed"] = report["raw_rows"] - len(df)

    report["blank_category"] = int(df["Category"].isna().sum())
    report["blank_agent"] = int(df["Agent"].isna().sum())
    df["Category"] = df["Category"].fillna("Unknown")
    df["Agent"] = df["Agent"].fillna("Unassigned")

    bad_dates = df["Resolved_At"].notna() & (df["Resolved_At"] < df["Created_At"])
    report["bad_dates_removed"] = int(bad_dates.sum())
    df = df.loc[~bad_dates].copy()

    df["Created_Date"] = df["Created_At"].dt.date
    df["Month"] = df["Created_At"].dt.to_period("M").astype(str)
    df["Week_Start"] = df["Created_At"].dt.to_period("W").dt.start_time
    df["Hour"] = df["Created_At"].dt.hour
    df["Day_Name"] = df["Created_At"].dt.day_name()
    df["Is_Resolved"] = df["Status"].isin(["Resolved", "Closed"])
    df["SLA_Met"] = df["SLA_Breach"].eq("No")
    df["SLA_Variance_Hours"] = (
        df["Resolution_Hours"] - df["SLA_Target_Hours"]
    ).round(2)

    report["clean_rows"] = len(df)
    report["unassigned_agent"] = int((df["Agent"] == "Unassigned").sum())
    report["unknown_category"] = int((df["Category"] == "Unknown").sum())
    report["open_or_pending"] = int((~df["Is_Resolved"]).sum())
    report["data_quality_pct"] = round(
        100 * (1 - (report["duplicates_removed"] +
                    report["blank_category"] +
                    report["blank_agent"] +
                    report["bad_dates_removed"]) / report["raw_rows"]), 1
    )
    return df.reset_index(drop=True), report


if __name__ == "__main__":
    clean, report = load_and_clean()
    clean.to_csv(CLEAN_FILE, index=False)
    print("ETL completed successfully")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"Saved: {CLEAN_FILE}")
