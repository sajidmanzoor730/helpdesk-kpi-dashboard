# STRIDE Threat Model
S: JWT spoofing -> short-lived 15m + rotation
T: CSV injection -> sanitization in clean_tickets.py
R: Repudiation -> audit logs for SLA changes
I: Info Disclosure -> PII masking, httpOnly SameSite=Strict
D: DoS -> Bounded queues (chunk 100), p-limit
E: Elevation -> OPA policy engine for Admin/Viewer/Agent
OWASP Top 10 checklist: Done
