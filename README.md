# 📊 Helpdesk Ticket Analytics Dashboard

**🔗 Live demo:** https://hedesk-dashboard.streamlit.app/
**Stack:** Python · Pandas · SQL · Streamlit · Power BI

> Messy ticket export → Python cleaning → KPI calculation → Power BI + live Streamlit dashboard.



![Priority distribution](priority_distribution.png)



## 🧹 Overview
1,020 raw rows (20 duplicates/nulls added on purpose) → 1,000 clean unique tickets → 5 KPIs → interactive dashboard.

**Dataset:** `Helpdesk_Tickets_Dataset_1000.xlsx`, synthetic sample data
**Columns:** Ticket_ID, Priority (P1-P4), Category, Status, SLA_Breach, CSAT (1-5), Is_Repeat

## 📈 KPIs
- **SLA adherence:** 91.2% (P1 breach ~30% vs ~5% for P3/P4)
- **Average CSAT:** 3.73 / 5
- **Repeat tickets:** 12%
- **Data quality after cleaning:** 98%
- **MTTR:** scales with priority

## ⚙️ Engineering notes
Patterns I explored while building this. Status shows what is in the code today.

| Area | Pattern | Where | Status |
|---|---|---|---|
| Caching | `@st.cache_data` with 1-hour TTL | `app.py` | CONFIRM |
| Rate limiting | Rate limiter | `src/ratelimiter/` | CONFIRM |
| Queues / DLQ | Bounded queue, Kafka DLQ for SLA breaches | YOUR_FILE_OR_DOC | Implemented / Design only |
| Locking | Locks in the dedup step | YOUR_FILE_OR_DOC | Implemented / Design only |
| Auth | Role-based access (Admin / Viewer / Agent) | YOUR_FILE_OR_DOC | Implemented / Design only |
| Security | Threat model (STRIDE) | `docs/` | Documented |
| Decisions | Cache ADR | `docs/` | Documented |

## 🚀 Run it
```bash
pip install -r requirements.txt
python clean_tickets.py
streamlit run app.py
```

## 📁 Files
`clean_tickets.py` · `app.py` · `sql_analysis.sql` · `data_dictionary.md` · `tests/` · `docs/`

## 🤝 Let's talk
Always happy to compare notes on support analytics. Message me on [LinkedIn](YOUR_LINKEDIN_URL) or open an issue.

*Built by Sajid Manzoor*
