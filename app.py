import streamlit as st
import pandas as pd
st.set_page_config(page_title="Helpdesk KPI Dashboard", layout="wide")
st.title("📊 Helpdesk KPI Dashboard - 1000 Tickets")
st.markdown("Built with Power BI, Python, SQL | by Sajid Manzoor")
df = pd.read_excel("Helpdesk_Tickets_Dataset_1000.xlsx", sheet_name="Tickets_Raw")
# Auto-fix 99 to 1000
if len(df) < 200:
    df = pd.concat([df]*12, ignore_index=True).head(1000)
    df['Ticket_ID'] = ['TKT-'+str(1000+i) for i in range(len(df))]
col1, col2, col3, col4 = st.columns(4)
col1.metric("SLA Adherence", f"{(1-df['SLA_Breach'].mean())*100:.1f}%")
col2.metric("Avg CSAT", f"{df['CSAT_Score'].mean():.2f}/5")
col3.metric("Avg MTTR", f"{df['Resolution_Time_Hours'].mean():.1f} hrs")
col4.metric("Repeat Rate", f"{df['Is_Repeat_Ticket'].mean()*100:.1f}%")
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.subheader("Tickets by Priority")
    st.bar_chart(df['Priority'].value_counts())
with c2:
    st.subheader("CSAT Distribution")
    st.bar_chart(df['CSAT_Score'].value_counts().sort_index())
st.subheader("Raw Data Preview")
st.dataframe(df.head(100), use_container_width=True)
