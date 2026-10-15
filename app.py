import pandas as pd
import streamlit as st

from clean_tickets import SOURCE_URL, load_and_clean

st.set_page_config(page_title="Public IT Helpdesk Trends", page_icon="📊", layout="wide")


@st.cache_data(ttl=3600)
def get_data():
    return load_and_clean()


try:
    df, report = get_data()
except Exception as exc:
    st.error("The official public dataset could not be loaded right now.")
    st.markdown(f"Source: [Montgomery County MCG HelpIT Tickets]({SOURCE_URL})")
    st.caption("Refresh the page in a little while. The dashboard does not silently fall back to generated data.")
    st.exception(exc)
    st.stop()

st.title("Public IT Helpdesk Trends")
st.caption(
    "Analysis of published Montgomery County Government IT helpdesk summary data. "
    "These are aggregated public counts, not individual ticket records."
)

with st.sidebar:
    st.header("Report filters")
    years = sorted(df["Fiscal_Year"].dropna().astype(int).unique().tolist())
    selected_years = st.multiselect("Fiscal year", years, default=years)
    groups = sorted(df["Report_Group"].dropna().unique().tolist())
    selected_groups = st.multiselect("Report section", groups, default=groups)

view = df[
    df["Fiscal_Year"].isin(selected_years) &
    df["Report_Group"].isin(selected_groups)
].copy()

if view.empty:
    st.warning("No published rows match these filters.")
    st.stop()

source_view = view[view["Report_Group"].str.casefold().eq("ticket type by source")]
request_view = view[view["Report_Group"].str.casefold().eq("top request")]
department_view = view[view["Report_Group"].str.casefold().eq("contacts by department")]
survey_view = view[view["Report_Group"].str.casefold().eq("surveys")]

latest_year = int(view["Fiscal_Year"].max())
source_total = source_view.loc[source_view["Fiscal_Year"].eq(latest_year), "Total_Count"].sum()
top_request = request_view.sort_values("Total_Count", ascending=False).head(1)
top_request_name = top_request.iloc[0]["Item"] if not top_request.empty else "—"
top_request_count = int(top_request.iloc[0]["Total_Count"]) if not top_request.empty else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Fiscal years in view", f"{view['Fiscal_Year'].nunique():,}")
c2.metric(f"Source-count total · FY {latest_year}", f"{source_total:,.0f}" if pd.notna(source_total) else "—")
c3.metric("Report rows", f"{len(view):,}")
c4.metric("Largest listed request", f"{top_request_name}", help=f"{top_request_count:,} published count")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Executive overview", "Request mix", "Contact channels & departments", "Survey records"]
)

with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader("Published counts by report section")
        section_totals = view.groupby("Report_Group")["Total_Count"].sum().sort_values(ascending=False)
        st.bar_chart(section_totals)
        st.caption("Sections overlap in meaning; do not add their totals together.")
    with right:
        st.subheader("Largest listed requests")
        if request_view.empty:
            st.info("Select Top Request in the sidebar to see request types.")
        else:
            top = request_view.sort_values("Total_Count", ascending=False).head(10)
            st.bar_chart(top.set_index("Item")["Total_Count"])
    st.subheader("Rows in the selected public extract")
    st.dataframe(
        view[["Fiscal_Year", "Report_Group", "Item", "Total_Count", "Percentage"]]
        .sort_values(["Fiscal_Year", "Report_Group", "Total_Count"], ascending=[False, True, False]),
        use_container_width=True,
        hide_index=True,
    )

with tab2:
    st.subheader("Top request types")
    if request_view.empty:
        st.info("Select Top Request in the sidebar to see request types.")
    else:
        requests = request_view.sort_values(["Fiscal_Year", "Total_Count"], ascending=[False, False])
        st.bar_chart(requests.pivot_table(index="Item", columns="Fiscal_Year", values="Total_Count", aggfunc="sum", fill_value=0))
        st.dataframe(
            requests[["Fiscal_Year", "Item", "Description", "Total_Count", "Percentage"]]
            .sort_values(["Fiscal_Year", "Total_Count"], ascending=[False, False]),
            use_container_width=True,
            hide_index=True,
        )

with tab3:
    left, right = st.columns(2)
    with left:
        st.subheader("Contact counts by source")
        if source_view.empty:
            st.info("Select Ticket Type By Source in the sidebar.")
        else:
            st.bar_chart(source_view.pivot_table(index="Item", columns="Fiscal_Year", values="Total_Count", aggfunc="sum", fill_value=0))
            st.dataframe(source_view[["Fiscal_Year", "Item", "Total_Count", "Percentage"]], use_container_width=True, hide_index=True)
    with right:
        st.subheader("Contacts by department")
        if department_view.empty:
            st.info("Select Contacts By Department in the sidebar.")
        else:
            st.bar_chart(department_view.pivot_table(index="Item", columns="Fiscal_Year", values="Total_Count", aggfunc="sum", fill_value=0))
            st.dataframe(department_view[["Fiscal_Year", "Item", "Total_Count", "Percentage"]], use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Published survey summary")
    if survey_view.empty:
        st.info("No survey rows are included in the current filter selection.")
    else:
        st.dataframe(
            survey_view[["Fiscal_Year", "Item", "Description", "Total_Count", "Percentage"]],
            use_container_width=True,
            hide_index=True,
        )
    st.caption("The source contains survey summary counts, not individual CSAT ratings; this dashboard does not calculate average CSAT.")

with st.expander("Data provenance and limitations"):
    st.markdown(
        f"""
        - **Publisher:** Montgomery County, Maryland.
        - **Dataset:** [MCG HelpIT Tickets]({SOURCE_URL}).
        - **Data type:** published summary rows by fiscal year, report section, and item.
        - **Refresh:** fetched from the official public endpoint when the dashboard cache expires.
        - **Important limitation:** the source is aggregated. It does not expose individual ticket IDs, agent-level performance, response/resolution timestamps, SLA targets, or individual CSAT scores. Those KPIs are intentionally not reported here.
        - **Quality checks:** {report['rows_loaded']} source rows loaded; {report['invalid_count_rows']} rows with missing or invalid counts excluded; {report['duplicate_rows']} duplicate summary rows removed.
        """
    )
