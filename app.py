import pandas as pd
import streamlit as st

from clean_tickets import load_and_clean

st.set_page_config(page_title="Helpdesk KPI Dashboard", page_icon="📊", layout="wide")


@st.cache_data(ttl=3600)
def get_data():
    return load_and_clean()


df, report = get_data()

st.title("Helpdesk Ticket KPI Dashboard")
st.caption(
    "Enterprise-style support operations analytics demonstration — "
    "source export → Python ETL → quality controls → SQL/BI reporting."
)

with st.sidebar:
    st.header("Report filters")
    min_d, max_d = df["Created_At"].min().date(), df["Created_At"].max().date()
    date_range = st.date_input("Created between", (min_d, max_d),
                               min_value=min_d, max_value=max_d)
    priorities = st.multiselect("Priority", sorted(df["Priority"].unique()),
                                default=sorted(df["Priority"].unique()))
    teams = st.multiselect("Team", sorted(df["Team"].unique()),
                           default=sorted(df["Team"].unique()))
    channels = st.multiselect("Channel", sorted(df["Channel"].unique()),
                              default=sorted(df["Channel"].unique()))
    categories = st.multiselect("Category", sorted(df["Category"].unique()),
                                default=sorted(df["Category"].unique()))

if len(date_range) == 2:
    df = df[(df["Created_At"].dt.date >= date_range[0]) &
            (df["Created_At"].dt.date <= date_range[1])]

df = df[
    df["Priority"].isin(priorities) &
    df["Team"].isin(teams) &
    df["Channel"].isin(channels) &
    df["Category"].isin(categories)
]

done = df[df["Status"].isin(["Resolved", "Closed"])]
if done.empty:
    st.warning("No resolved or closed tickets match these filters.")
    st.stop()

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Tickets", f"{len(df):,}")
c2.metric("SLA adherence", f"{(done['SLA_Breach'] == 'No').mean():.1%}")
c3.metric("Avg resolution", f"{done['Resolution_Hours'].mean():.1f} hrs")
c4.metric("Avg CSAT", f"{done['CSAT'].mean():.2f} / 5")
c5.metric("Repeat rate", f"{(done['Is_Repeat'] == 'Yes').mean():.1%}")
c6.metric("Escalation rate", f"{(done['Escalated'] == 'Yes').mean():.1%}")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Executive overview", "SLA & operations", "Demand & workload", "Team performance"]
)

with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader("Tickets by month")
        st.line_chart(df.groupby("Month").size())
    with right:
        st.subheader("SLA breach rate by priority")
        breach = done.groupby("Priority")["SLA_Breach"].apply(
            lambda s: (s == "Yes").mean() * 100
        ).round(1)
        st.bar_chart(breach)
    st.subheader("Ticket volume by category")
    st.bar_chart(df["Category"].value_counts())

with tab2:
    left, right = st.columns(2)
    with left:
        st.subheader("Resolution hours by priority")
        st.bar_chart(done.groupby("Priority")["Resolution_Hours"].mean().round(1))
    with right:
        st.subheader("SLA breach reason")
        reasons = done[done["SLA_Breach"] == "Yes"]["Breach_Reason"].value_counts()
        st.bar_chart(reasons)
    st.subheader("High-priority exception queue")
    exceptions = done[(done["SLA_Breach"] == "Yes") & done["Priority"].isin(["P1", "P2"])].copy()
    exceptions["SLA_Variance_Hours"] = (
        exceptions["Resolution_Hours"] - exceptions["SLA_Target_Hours"]
    ).round(2)
    st.dataframe(
        exceptions[["Ticket_ID", "Created_At", "Priority", "Category", "Team",
                    "Agent", "Resolution_Hours", "SLA_Target_Hours",
                    "SLA_Variance_Hours"]]
        .sort_values("SLA_Variance_Hours", ascending=False)
        .head(50),
        use_container_width=True, hide_index=True
    )

with tab3:
    left, right = st.columns(2)
    with left:
        st.subheader("Tickets by channel")
        st.bar_chart(df["Channel"].value_counts())
    with right:
        st.subheader("Tickets by hour")
        st.bar_chart(df.groupby("Hour").size())
    st.subheader("Repeat-ticket rate by category")
    repeat = done.groupby("Category")["Is_Repeat"].apply(
        lambda s: (s == "Yes").mean() * 100
    ).round(1).sort_values(ascending=False)
    st.bar_chart(repeat)

with tab4:
    st.subheader("Agent performance — 20+ resolved tickets")
    agents = (
        done[done["Agent"] != "Unassigned"]
        .groupby(["Team", "Agent"])
        .agg(
            tickets=("Ticket_ID", "count"),
            sla_pct=("SLA_Breach", lambda s: round((s == "No").mean() * 100, 1)),
            avg_resolution_hrs=("Resolution_Hours", lambda s: round(s.mean(), 1)),
            avg_csat=("CSAT", lambda s: round(s.mean(), 2)),
            escalations=("Escalated", lambda s: (s == "Yes").mean() * 100),
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
        "Unassigned agents": report["unassigned_agent"],
        "Open / pending": report["open_or_pending"],
        "Data quality": f"{report['data_quality_pct']}%",
    })

with st.expander("BI semantic model"):
    st.markdown(
        """
        **Fact:** FactTickets — one row per unique ticket.

        **Dimensions:** DimDate, DimAgent, DimCategory, DimPriority,
        DimChannel, DimCustomerSegment and DimRegion.

        **Reporting:** reusable measures support executive KPIs,
        SLA exceptions, demand analysis and team performance.
        """
    )
