import streamlit as st
import pandas as pd

st.set_page_config(page_title="Helpdesk KPI Dashboard", layout="wide")
st.title("📊 Helpdesk KPI Dashboard - 1000 Tickets")

# ---- Load raw data ----
df_raw = pd.read_excel("Helpdesk_Tickets_Dataset_1000.xlsx", sheet_name="Tickets_Raw")
st.write("Raw rows loaded:", len(df_raw))  # debug — should print 1020

# ---- Clean (remove duplicate Ticket_IDs) ----
df = df_raw.drop_duplicates('Ticket_ID').head(1000)
st.write("After dedup:", len(df))  # debug — should print 1000

# ---- KPI metrics ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", len(df))
col2.metric("SLA Adherence", f"{(1 - df['SLA_Breach'].mean()) * 100:.1f}%")
col3.metric("Avg CSAT", f"{df['CSAT_Score'].mean():.2f}")
col4.metric("Avg MTTR (hrs)", f"{df['Resolution_Time_Hours'].mean():.1f}")

st.divider()

# ---- Charts ----
st.subheader("Tickets by Priority")
st.bar_chart(df['Priority'].value_counts())

st.subheader("Avg Resolution Time by Category")
st.bar_chart(df.groupby('Category')['Resolution_Time_Hours'].mean())

st.subheader("Ticket Volume by Client")
st.bar_chart(df['Client_Name'].value_counts())

st.divider()

# ---- Raw data table ----
st.subheader("Ticket Data")
st.dataframe(df, use_container_width=True)
