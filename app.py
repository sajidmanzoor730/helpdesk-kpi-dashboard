import streamlit as st
import pandas as pd
st.set_page_config(page_title="Helpdesk KPI Dashboard", layout="wide")
st.title("📊 Helpdesk KPI Dashboard - 1000 Tickets")
df = pd.read_excel("Helpdesk_Tickets_Dataset_1000.xlsx", sheet_name="Tickets_Raw")
df = df.drop_duplicates('Ticket_ID').head(1000)
st.metric("Total Tickets", len(df))
st.metric("SLA", f"{(1-df['SLA_Breach'].mean())*100:.1f}%")
st.metric("CSAT", f"{df['CSAT_Score'].mean():.2f}")
st.bar_chart(df['Priority'].value_counts())
st.dataframe(df.head(100))
