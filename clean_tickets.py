"""Load and validate the official public MCG HelpIT summary dataset.

The source is aggregated government reporting data, not individual ticket records.
No synthetic fallback is used: if the public source is unavailable, the dashboard
shows an error rather than quietly switching to generated data.
"""
from io import BytesIO
from urllib.request import Request, urlopen

import pandas as pd

SOURCE_URL = "https://data.montgomerycountymd.gov/api/v3/views/qzr8-h9x6/export.csv?accessType=DOWNLOAD"


def _normalise_header(value):
    return "".join(ch.lower() for ch in str(value) if ch.isalnum())


def load_and_clean():
    request = Request(SOURCE_URL, headers={"User-Agent": "SajidHelpdeskPublicDataDashboard/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()
    raw = pd.read_csv(BytesIO(payload))
    report = {"rows_loaded": len(raw), "invalid_count_rows": 0, "duplicate_rows": 0}

    aliases = {
        "Fiscal_Year": {"fiscalyear"},
        "Report_Group": {"tickettypename", "reportgroup", "reportsection"},
        "Item": {"tickettypedescription", "item", "name"},
        "Total_Count": {"totalcount", "count", "total"},
        "Percentage": {"percentage", "percent"},
    }
    header_lookup = {_normalise_header(col): col for col in raw.columns}
    selected = {}
    for target, possible in aliases.items():
        match = next((header_lookup[name] for name in possible if name in header_lookup), None)
        if match is None:
            raise ValueError(
                f"Official source schema changed: could not identify {target}. "
                f"Available columns: {list(raw.columns)}"
            )
        selected[target] = match

    description_source = next(
        (header_lookup[name] for name in {"tickettypedescription", "description"} if name in header_lookup),
        None,
    )
    if description_source and description_source != selected["Item"]:
        raw["Description"] = raw[description_source].astype("string").fillna("")
    else:
        raw["Description"] = ""

    df = raw.rename(columns={source: target for target, source in selected.items()}).copy()
    df["Fiscal_Year"] = pd.to_numeric(df["Fiscal_Year"], errors="coerce")
    df["Total_Count"] = pd.to_numeric(
        df["Total_Count"].astype("string").str.replace(",", "", regex=False).str.replace("%", "", regex=False),
        errors="coerce",
    )
    df["Percentage"] = pd.to_numeric(
        df["Percentage"].astype("string").str.replace("%", "", regex=False).str.replace(",", "", regex=False),
        errors="coerce",
    )
    df["Report_Group"] = df["Report_Group"].astype("string").str.strip()
    df["Item"] = df["Item"].astype("string").str.strip()
    df["Description"] = df["Description"].astype("string").fillna("").str.strip()

    invalid = df["Fiscal_Year"].isna() | df["Total_Count"].isna() | df["Report_Group"].eq("") | df["Item"].eq("")
    report["invalid_count_rows"] = int(invalid.sum())
    df = df.loc[~invalid].copy()
    df["Fiscal_Year"] = df["Fiscal_Year"].astype(int)

    before = len(df)
    df = df.drop_duplicates(subset=["Fiscal_Year", "Report_Group", "Item", "Total_Count"], keep="first")
    report["duplicate_rows"] = before - len(df)
    report["rows_clean"] = len(df)
    if df.empty:
        raise ValueError("The official source returned no usable summary rows.")
    return df.sort_values(["Fiscal_Year", "Report_Group", "Total_Count"], ascending=[False, True, False]).reset_index(drop=True), report
