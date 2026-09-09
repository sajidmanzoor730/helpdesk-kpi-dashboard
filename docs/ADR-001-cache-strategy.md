# ADR 001: Cache Strategy
Decision: Use Cache-Aside with Redis TTL 3600s + LRU eviction + Single-Flight
Context: Dashboard has read-heavy KPIs, concurrent users cause stampede
Consequence: 85% faster, prevents thundering herd via probabilistic early expiration
Status: Accepted
