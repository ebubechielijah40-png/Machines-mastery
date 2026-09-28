# Security

Only synthetic data and a local database are used. Parameterized queries separate values from SQL syntax, but they do not provide authentication or authorization. Those are explicitly absent. Input limits constrain this exercise, not all resource abuse. Never put credentials in logs. Any future local deliberately vulnerable variant requires a written threat model, trust boundaries, controlled demonstration, detection, mitigation and regression tests. No external probing is authorized by this lab.
