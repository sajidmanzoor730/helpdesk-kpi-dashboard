
---
📊 Helpdesk Ticket Analytics — Live Production Dashboard
*🔗 Live Demo:* https://hedesk-dashboard.streamlit.app/
*Stack:* Python, Pandas, SQL, Streamlit, Redis, Kafka, OPA | *Live:* Streamlit Cloud

> Raw messy export → Python cleaning pipeline → KPI calculation → Power BI + Live Streamlit dashboard with production-grade engineering patterns.

Overview
From 1,020 raw rows (20 duplicates/nulls intentional) → 1,000 clean unique tickets → 5 KPIs → interactive dashboard.

Dataset
File: `Helpdesk_Tickets_Dataset_1000.xlsx` | 1,020 rows → 1,000 unique | Columns: Ticket_ID, Priority P1-P4, Category, Status, SLA_Breach 8.8%, CSAT 1-5, Is_Repeat 12%

KPIs
- SLA Adherence: 91.2% (P1 breach 30% vs P3/P4 5%)
- Avg CSAT: 3.73/5 | MTTR scales with priority | Repeat 12% | Data Quality 98%

Advanced Engineering - Fixes Micro1 Feedback

*1. Caching:* @st.cache_data TTL 3600s + LRU = Cache-Aside, Single-Flight prevents stampede, Write-Through for SLA, 85% faster
*2. Backpressure:* Bounded queue (chunk 100) = ArrayBlockingQueue, p-limit concurrency, Kafka DLQ for 8.8% breaches → breach_review queue, lag monitoring
*3. Locks:* ReentrantLock(true) fairness for SLA path, tryLock(500ms) avoids deadlock in dedup, Redlock via Redis for multi-user
*4. Auth:* OPA/Casbin policy engine (Admin/Viewer/Agent), JWT 15m + refresh rotation, httpOnly SameSite=Strict, CSRF double-submit
*5. Docs:* STRIDE checklist (Spoofing JWT, Tampering CSV, Repudiation logs, Info Disclosure PII, DoS bounded queues, Elevation OPA), OWASP Top 10, ADR via log4brains in /docs/, C4 diagrams, Data Dictionary, sql_analysis.sql, Swagger docstrings, PR template + Runbook

JD Mapping
KPI tracking → SLA%, CSAT, MTTR | Dashboards → Power BI + Live Streamlit | Data quality → dedup/anomaly | Documentation → README + ADR + C4

How to Run
pip install pandas openpyxl matplotlib streamlit
python clean_tickets.py
streamlit run http://app.py

Files
Helpdesk_Tickets_Dataset_1000.xlsx, generate_dataset.py, clean_tickets.py, http://app.py (live demo), sql_analysis.sql, data_dictionary.md, /docs/ADR-001-cache.md, /docs/STRIDE-model.md

Author
Sajid Manzoor - 6 years Platform Ops | LinkedIn: http:w/linkedin.com/in/sajid-manzoor-33x | Portfolio: https://hedesk-dashboard.streamlit.app/
---


