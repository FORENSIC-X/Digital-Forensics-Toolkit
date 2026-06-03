# 🔍 Apache Web Server Log Analyzer

> **Part of the Digital Forensics Toolkit** — A CLI-based forensic tool for analyzing Apache web server access logs, detecting suspicious activity, and identifying brute-force attacks.

---

## 📌 Overview

When a web server is compromised, the attacker leaves footprints in the server's access logs. This tool parses raw Apache access logs, extracts structured forensic data using Regular Expressions, and automatically flags malicious behavior — all from the command line.

This is a **standalone CLI tool**. A separate Windows Event Log Analyzer is maintained in a different repository.

---

## 🧠 What It Does

| Feature | Description |
|---|---|
| **Log Parsing** | Reads raw Apache Combined Log Format entries line by line |
| **Request Profiling** | Counts total requests made by each unique IP address |
| **Suspicious Event Detection** | Flags all `401 Unauthorized` and `403 Forbidden` HTTP responses |
| **Brute Force Detection** | Alerts when a single IP exceeds 5 failed login attempts |
| **Forensic Report** | Prints a structured, human-readable summary to the terminal |

---

## 🗂️ Log Format Supported

This tool is built for the **Apache Combined Log Format**. A sample line looks like this:

```
192.168.1.105 - - [10/Oct/2024:13:55:10 +0000] "POST /admin/login HTTP/1.1" 401 512
```

Each line contains: IP address, timestamp, HTTP method, requested path, status code, and response size.

---

## ⚙️ How It Works

The tool uses a compiled **Regular Expression pattern** (`LOG_PATTERN`) to extract structured fields from each log line:

```python
LOG_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)'
    r'.+?'
    r'\[(?P<timestamp>[^\]]+)\]'
    r'\s"(?P<method>\w+)\s(?P<path>\S+)'
    r'.+?"'
    r'\s(?P<status>\d{3})'
    r'\s(?P<size>\d+)'
)
```

Lines that don't match the expected format (blank lines, corrupted entries) are silently skipped and not counted in the parsed total — ensuring report accuracy.

---

## 🚀 Usage

**Requirements:** Python 3.x — no external libraries needed.

```bash
python log_analyzer.py <path_to_log_file>
```

**Example:**
```bash
python log_analyzer.py access.log
```

---

## 📊 Sample Output

```
============================================================
FORENSIC LOG ANALYSIS REPORT
============================================================

[*] Total log entries parsed :  12
[*] Unique IP addresses found :  4

--- REQUEST COUNT PER IP ---

192.168.1.101 -> 1 requests
192.168.1.105 -> 7 requests
10.0.0.22 -> 2 requests
203.0.113.42 -> 2 requests

--- SUSPICIOUS EVENTS (401 / 403) ---

10/Oct/2024:13:55:10 +0000    192.168.1.105 -> POST    /admin/login    401
10/Oct/2024:13:55:11 +0000    192.168.1.105 -> POST    /admin/login    401
10/Oct/2024:13:55:12 +0000    192.168.1.105 -> POST    /admin/login    401
10/Oct/2024:13:55:13 +0000    192.168.1.105 -> POST    /admin/login    401
10/Oct/2024:13:55:14 +0000    192.168.1.105 -> POST    /admin/login    401
10/Oct/2024:13:55:15 +0000    192.168.1.105 -> POST    /admin/login    401
10/Oct/2024:13:56:45 +0000    10.0.0.22 -> GET         /admin          403

--- BRUTE FORCE DETECTION (Threshold : 5 failed attempts) ---

[!!] BRUTE FORCE DETECTED : 192.168.1.105 -> 6 failed attempts on /admin/login

============================================================
```

---

## 🔎 Reading the Report

**Suspicious Events (401/403)**
- `401 Unauthorized` → The server received a request but rejected it due to bad credentials. A repeated pattern of 401s against a login endpoint is the textbook signature of a **brute-force attack**.
- `403 Forbidden` → The server understood the request but refused it. Often indicates an attacker **probing for restricted areas** they don't have permission to access.

**Brute Force Detection**
- The threshold is set at **5 failed attempts** from a single IP. Any IP exceeding this is flagged with the exact number of attempts and the targeted endpoint.
- In the sample above, `192.168.1.105` made **6 failed attempts** before successfully logging in on the 7th try — a confirmed brute-force breach.

---

## ⚠️ Forensic Notes

- Always run this tool on a **copy** of the log file, never the original.
- Verify the SHA-256 hash of the log file before and after analysis to confirm it was not altered during investigation. *(See the File Hasher Tool in the DIGITAL-FORENSICS repository.)*
- Log timestamps are in the server's local timezone. Normalize to UTC before cross-referencing with other evidence sources.
- Sophisticated attackers may use **IP rotation** to stay under the brute-force threshold. Manual review of the Suspicious Events section is still recommended even when no brute-force alert fires.

---
> **Disclaimer:** This tool is built as part of a my Digital Forensics learning journey documentation intended strictly for educational purposes and legitimate forensic investigations conducted with proper legal authorization. Unauthorized use against systems or files you do not own or have explicit permission to analyze is illegal.
