-- Dimensional model for the Helpdesk KPI BI solution.
-- Fact grain: one row per unique Ticket_ID.

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    calendar_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    week_number INTEGER NOT NULL,
    day_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_priority (
    priority_key INTEGER PRIMARY KEY,
    priority_code TEXT UNIQUE NOT NULL,
    response_class TEXT NOT NULL,
    target_hours INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_agent (
    agent_key INTEGER PRIMARY KEY,
    agent_name TEXT UNIQUE NOT NULL,
    team TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_category (
    category_key INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_channel (
    channel_key INTEGER PRIMARY KEY,
    channel_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_segment (
    segment_key INTEGER PRIMARY KEY,
    segment_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_region (
    region_key INTEGER PRIMARY KEY,
    region_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_tickets (
    ticket_key INTEGER PRIMARY KEY,
    ticket_id TEXT UNIQUE NOT NULL,
    created_date_key INTEGER NOT NULL,
    agent_key INTEGER,
    category_key INTEGER,
    priority_key INTEGER NOT NULL,
    channel_key INTEGER,
    segment_key INTEGER,
    region_key INTEGER,
    subcategory TEXT,
    status TEXT,
    first_response_minutes INTEGER,
    resolution_hours REAL,
    sla_breach TEXT,
    breach_reason TEXT,
    reopen_count INTEGER,
    escalated TEXT,
    csat REAL,
    is_repeat TEXT,
    contact_reason TEXT,
    root_cause TEXT,
    FOREIGN KEY (created_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (agent_key) REFERENCES dim_agent(agent_key),
    FOREIGN KEY (category_key) REFERENCES dim_category(category_key),
    FOREIGN KEY (priority_key) REFERENCES dim_priority(priority_key),
    FOREIGN KEY (channel_key) REFERENCES dim_channel(channel_key),
    FOREIGN KEY (segment_key) REFERENCES dim_segment(segment_key),
    FOREIGN KEY (region_key) REFERENCES dim_region(region_key)
);

-- Reporting grain remains one row per unique Ticket_ID.
-- Dimensions support reusable filtering and aggregation in Power BI.
