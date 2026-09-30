"""
Production-style ETL layer for the helpdesk analytics demonstration.

Pipeline:
1. Read the raw operational export.
2. Standardize dates and categorical fields.
3. Remove duplicate Ticket_ID records.
4. Validate ticket chronology.
5. Fill controlled missing dimensions.
6. Derive reporting attributes used by the analytical model.
7. Return the curated dataset plus an auditable quality report.

The source file is a realistic demonstration export, not customer data.
"""

import pandas as pd

RAW_FILE = "Helpdesk_Tickets_Dataset_Raw.xlsx"
CLEAN_FILE = "Helpdesk_Tickets_Clean.csv"


def load_and_clean(path=RAW_FILE):
    raw = pd.read_excel(path, parse_dates=["Created_At", "Resolved_At"])
    report = {
        "raw_rows": len(raw),
        "raw_columns": len(raw.columns),
    }

    # Standardize text fields before quality checks.
    text_columns = ["Ticket_ID", "Priority", "Category", "Channel",
                    "Team", "Agent", "Status", "SLA_Breach", "Is_Repeat"]
    for column in text_columns:
        if column in raw.columns:
            raw[column] = raw[column].astype("string").str.strip()

    # Business key: one analytical record per Ticket_ID.
    df = raw.drop_duplicates(subset="Ticket_ID", keep="first").copy()
    report["duplicates_removed"] = report["raw_rows"] - len(df)

    report["blank_category"] = int(df["Category"].isna().sum())
    report["blank_agent"] = int(df["Agent"].isna().sum())

    df["Category"] = df["Category"].fillna("Unknown")
    df["Agent"] = df["Agent"].fillna("Unassigned")

    # Reject impossible ticket timelines rather than silently changing them.
    bad_dates = df["Resolved_At"].notna() & (df["Resolved_At"] < df["Created_At"])
    report["bad_dates_removed"] = int(bad_dates.sum())
    df = df.loc[~bad_dates].copy()

    # Analytical/reporting dimensions.
    df["Created_Date"] = df["Created_At"].dt.date
    df["Month"] = df["Created_At"].dt.to_period("M").astype(str)
    df["Week_Start"] = df["Created_At"].dt.to_period("W").dt.start_time
    df["Hour"] = df["Created_At"].dt.hour
    df["Day_Name"] = df["Created_At"].dt.day_name()
    df["Is_Resolved"] = df["Status"].isin(["Resolved", "Closed"])
    df["SLA_Met"] = df["SLA_Breach"].eq("No")

    # A useful analytical measure for prioritization.
    df["SLA_Variance_Hours"] = (
        df["Resolution_Hours"] - df["SLA_Target_Hours"]
    ).round(2)

    total_issues = (
        report["duplicates_removed"]
        + report["blank_category"]
        + report["blank_agent"]
        + report["bad_dates_removed"]
    )
    report["clean_rows"] = len(df)
    report["data_quality_pct"] = round(
        100 * (1 - total_issues / report["raw_rows"]), 1
    )

    return df.reset_index(drop=True), report


if __name__ == "__main__":
    clean, report = load_and_clean()
    clean.to_csv(CLEAN_FILE, index=False)

    print("ETL completed successfully")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"Saved: {CLEAN_FILE}")
