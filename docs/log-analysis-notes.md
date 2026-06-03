# Log Analysis Tool — Concepts & Notes

## What is a Log File?

Every system, server, and application running on a computer keeps a diary called a **Log File**. Every time something happens — a user logs in, a file is accessed, a webpage is requested, or a login attempt fails — the system writes a timestamped entry into this diary automatically.

Log files are among the most important sources of evidence in a forensic investigation because, unlike a human witness, **logs don't lie, don't forget, and record everything with exact timestamps.**

---

## The Two Most Important Log Types for Forensics

### 1. Apache / Nginx Web Server Access Logs

When a website is hosted on a Linux server, every single HTTP request made to that server is recorded. A single line looks like this:

```
192.168.1.105 - - [10/Oct/2024:13:55:36 +0000] "POST /admin/login HTTP/1.1" 401 512
```

Breaking that line down:

| Field | Value | Meaning |
|---|---|---|
| IP Address | `192.168.1.105` | Who made the request |
| Timestamp | `10/Oct/2024:13:55:36 +0000` | Exactly when |
| Method + Path | `POST /admin/login` | What they tried to do and where |
| Status Code | `401` | Unauthorized — wrong credentials |
| Response Size | `512` | Size of the server's reply in bytes |

### 2. Windows Event Logs

Windows records every login attempt, service start, file access, and policy change. Each event carries a unique **Event ID**. The two most critical for forensics:

| Event ID | Meaning |
|---|---|
| `4625` | A user account **failed** to log on |
| `4624` | A user account **successfully** logged on |

A flood of `4625` events from the same source in rapid succession is the textbook signature of a **brute-force attack**. A `4624` immediately following a cluster of `4625` events means the brute-force succeeded.

---

## Key HTTP Status Codes for Forensic Log Analysis

| Status Code | Meaning | Forensic Significance |
|---|---|---|
| `200` | OK — request succeeded | Normal traffic; note if it follows repeated failures |
| `401` | Unauthorized — bad credentials | Primary indicator of brute-force attempts |
| `403` | Forbidden — access denied by server | Attacker probing restricted areas |
| `404` | Not Found | May indicate directory traversal or vulnerability scanning |
| `500` | Internal Server Error | May indicate a successful or attempted injection attack |

---

## What the Apache Log Analyzer Does

The `log_analyzer.py` script processes a raw Apache access log and produces a structured forensic report:

- **Parses** every valid log line using a Regular Expression pattern
- **Profiles** each unique IP address by total request count
- **Flags** all `401` and `403` responses as suspicious events with full timestamps
- **Detects brute-force attacks** — any IP exceeding 5 failed attempts is flagged with the exact count and targeted endpoint
- **Skips malformed lines** — blank lines and corrupted entries are not counted, keeping the report accurate

### Brute Force Detection Logic

The tool tracks failed attempts per IP address in a dictionary. The threshold is set at **5 failed attempts**. In the sample log, `192.168.1.105` made 6 consecutive `POST` requests to `/admin/login` with `401` responses before receiving a `200` on the 7th attempt — a confirmed brute-force breach.

---

## Forensic Notes on Log Analysis

- Always analyze a **verified copy** of the log file, not the original. Hash both before and after analysis.
- Log timestamps reflect the **server's configured timezone**. Normalize all timestamps to UTC before cross-referencing with other evidence sources (e.g., Windows Event Logs from a different machine).
- Sophisticated attackers may use **IP rotation** — distributing failed attempts across multiple IP addresses to stay under any single-IP threshold. Even when no brute-force alert fires, the Suspicious Events section should be reviewed manually.
- Log files can be **tampered with** by an attacker who gained root access. Always verify the log file's hash against a backup if one exists.