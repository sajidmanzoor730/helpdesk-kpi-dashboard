"""Automated data-quality checks for the curated helpdesk dataset."""

from clean_tickets import load_and_clean


def run_quality_checks():
    df, report = load_and_clean()

    checks = {
        "ticket_id_unique": df["Ticket_ID"].is_unique,
        "created_at_present": df["Created_At"].notna().all(),
        "priority_valid": df["Priority"].isin(["P1", "P2", "P3", "P4"]).all(),
        "channel_valid": df["Channel"].isin(["Portal", "Email", "Chat", "Phone"]).all(),
        "resolution_dates_valid": (
            df["Resolved_At"].isna() |
            (df["Resolved_At"] >= df["Created_At"])
        ).all(),
        "sla_values_valid": df["SLA_Breach"].isin(["Yes", "No"]).all(),
        "status_valid": df["Status"].isin(["Resolved", "Closed", "Pending", "Open"]).all(),
        "csat_valid": df["CSAT"].dropna().between(1, 5).all(),
        "row_count_positive": len(df) > 0,
    }

    failed = [name for name, passed in checks.items() if not passed]

    print("DATA QUALITY CHECKS")
    print("=" * 24)
    for name, passed in checks.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print(f"Raw rows: {report['raw_rows']:,}")
    print(f"Curated rows: {report['clean_rows']:,}")
    print(f"Duplicates removed: {report['duplicates_removed']:,}")
    print(f"Rejected date records: {report['bad_dates_removed']:,}")

    if failed:
        raise ValueError(f"Quality checks failed: {', '.join(failed)}")

    print("Overall status: PASS")


if __name__ == "__main__":
    run_quality_checks()
