import pandas as pd
import streamlit as st

from clean_tickets import load_and_clean

st.set_page_config(page_title="Helpdesk KPI Dashboard", layout="wide")


@st.cache_data(ttl=3600)
def get_data():
    return load_and_clean()


df, report = get_data()

st.title("Helpdesk Ticket KPI Dashboard")
st.caption(
    "Operational support analytics demonstration. "
    "Pipeline: source export → Python ETL → quality controls → KPI analysis."
)

with st.sidebar:
    st.header("Filters")
    min_d, max_d = df["Created_At"].min().date(), df["Created_At"].max().date()
    date_range = st.date_input(
        "Created between",
        (min_d, max_d),
        min_value=min_d,
        max_value=max_d,
    )
    priorities = st.multiselect(
        "Priority",
        sorted(df["Priority"].unique()),
        default=sorted(df["Priority"].unique()),
    )
    teams = st.multiselect(
        "Team",
        sorted(df["Team"].unique()),
        default=sorted(df["Team"].unique()),
    )

if len(date_range) == 2:
    df = df[
        (df["Created_At"].dt.date >= date_range[0])
        & (df["Created_At"].dt.date <= date_range[1])
    ]

df = df[df["Priority"].isin(priorities) & df["Team"].isin(teams)]

done = df[df["Status"].isin(["Resolved", "Closed"])]
if done.empty:
    st.warning("No resolved tickets for these filters.")
    st.stop()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Tickets", f"{len(df):,}")
c2.metric("SLA adherence", f"{(done['SLA_Breach'] == 'No').mean():.1%}")
c3.metric("Avg resolution (hrs)", f"{done['Resolution_Hours'].mean():.1f}")
c4.metric("Avg CSAT", f"{done['CSAT'].mean():.2f} / 5")
c5.metric("Repeat rate", f"{(done['Is_Repeat'] == 'Yes').mean():.1%}")

left, right = st.columns(2)
with left:
    st.subheader("Tickets per week")
    st.line_chart(df.groupby("Week_Start").size())

with right:
    st.subheader("SLA breach rate by priority (%)")
    breach = (
        done.groupby("Priority")["SLA_Breach"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .round(1)
    )
    st.bar_chart(breach)

left, right = st.columns(2)
with left:
    st.subheader("Tickets by category")
    st.bar_chart(df["Category"].value_counts())

with right:
    st.subheader("Tickets by hour")
    st.bar_chart(df.groupby("Hour").size())

st.subheader("Agent performance (20+ resolved tickets)")
agents = (
    done[done["Agent"] != "Unassigned"]
    .groupby(["Team", "Agent"])
    .agg(
        tickets=("Ticket_ID", "count"),
        sla_pct=("SLA_Breach", lambda s: round((s == "No").mean() * 100, 1)),
        avg_resolution_hrs=("Resolution_Hours", lambda s: round(s.mean(), 1)),
        avg_csat=("CSAT", lambda s: round(s.mean(), 2)),
    )
    .query("tickets >= 20")
    .sort_values(["Team", "sla_pct"], ascending=[True, False])
    .reset_index()
)
st.dataframe(agents, use_container_width=True, hide_index=True)

with st.expander("ETL & data-quality audit"):
    st.write({
        "Raw rows": report["raw_rows"],
        "Raw columns": report["raw_columns"],
        "Duplicates removed": report["duplicates_removed"],
        "Blank category handled": report["blank_category"],
        "Blank agent handled": report["blank_agent"],
        "Invalid date records removed": report["bad_dates_removed"],
        "Curated rows": report["clean_rows"],
        "Data quality": f"{report['data_quality_pct']}%",
    })

with st.expander("BI model"):
    st.markdown(
        """
        **Fact:** FactTickets — one row per unique ticket.

        **Dimensions:** DimDate, DimAgent, DimCategory and DimPriority.

        **Reporting layer:** SQL analytical queries feed KPI definitions,
        exception analysis and dashboard views.
        """
    )
