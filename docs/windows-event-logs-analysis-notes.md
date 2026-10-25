# Windows Event Log Analysis — Theory Notes

> Part of the Digital Forensics Toolkit — Theory documentation for Windows Event Log forensics, covering log structure, forensically significant Event IDs, and analysis methodology.

---

## What are Windows Event Logs?

Windows keeps a detailed diary of everything that happens on the system. Every login, every failed password attempt, every service that starts or crashes, every user account that gets created — Windows writes a record of it to a structured database called the **Event Log**.

These logs live at:

```
C:\Windows\System32\winevt\Logs\
```

The three most important log files for forensics are:

| Log File | What it records |
|---|---|
| `Security.evtx` | Logins, logouts, failed passwords, privilege use |
| `System.evtx` | Service crashes, driver failures, system reboots |
| `Application.evtx` | Application errors, crashes, warnings |

---

## Event IDs — The Core Concept

Every event in Windows has a unique **Event ID** number that tells you exactly what happened. Think of Event IDs as the Magic Numbers of Windows forensics — a 4-digit number that instantly tells an investigator what occurred.

### Forensically Significant Event IDs

| Event ID | Meaning | Why it matters |
|---|---|---|
| **4624** | Successful login | Someone logged in — who, when, from where? |
| **4625** | Failed login | Wrong password — repeated failures = brute force |
| **4634** | Logoff | Session ended |
| **4648** | Login with explicit credentials | Possible lateral movement |
| **4672** | Admin privileges assigned | Privilege escalation attempt |
| **4698** | Scheduled task created | Malware persistence mechanism |
| **4720** | New user account created | Backdoor account creation |
| **4726** | User account deleted | Covering tracks |
| **7034** | Service crashed unexpectedly | Possible exploitation attempt |
| **7045** | New service installed | Malware installing itself as a service |

---

## The Problem with Real `.evtx` Files

Real Windows Event Log files (`.evtx`) are **binary files** — not plain text. You cannot open them in a text editor or parse them with basic Python string operations.

To parse them in Python, there are two approaches:

### Approach 1 — python-evtx Library
A third-party library called `python-evtx` can read the raw binary `.evtx` format directly and extract structured data from it.

```bash
pip install python-evtx
```

### Approach 2 — Exported XML Format (Used in this toolkit)
Windows allows you to export any Event Log as an XML file via **Event Viewer**, which produces plain text that is perfectly parseable with Python's built-in `xml` library — no external dependencies needed.

**How to export from Event Viewer:**
1. Open **Event Viewer** (`eventvwr.msc`)
2. Navigate to **Windows Logs → Security** (or System / Application)
3. Click **Save All Events As...**
4. Choose **XML** as the file format

This is the approach used in this toolkit for maximum portability and zero external dependencies.

---

## XML Structure of a Windows Event Log Entry

When exported as XML, each event follows this structure:

```xml
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  <System>
    <EventID>4625</EventID>
    <TimeCreated SystemTime="2024-10-10T13:55:10.000000000Z"/>
    <Computer>DESKTOP-ABC123</Computer>
  </System>
  <EventData>
    <Data Name="SubjectUserName">-</Data>
    <Data Name="TargetUserName">administrator</Data>
    <Data Name="IpAddress">192.168.1.105</Data>
    <Data Name="IpPort">54321</Data>
    <Data Name="LogonType">3</Data>
  </EventData>
</Event>
```

---

## The Namespace Issue

Windows Event Log XML uses a long **namespace prefix** on every single tag:

```
http://schemas.microsoft.com/win/2004/08/events/event
```

This namespace must be included in every `find()` call when parsing with Python's `xml.etree.ElementTree` — otherwise Python finds nothing. The correct pattern is:

```python
NS = "http://schemas.microsoft.com/win/2004/08/events/event"

# Correct — namespace included
event_id = event.find(f".//{{{NS}}}EventID").text

# Wrong — will return None every time
event_id = event.find(".//EventID").text
```

---

## Core Parsing Logic

```python
import xml.etree.ElementTree as ET

NS = "http://schemas.microsoft.com/win/2004/08/events/event"

tree = ET.parse(xml_file_path)
root = tree.getroot()

for event in root.findall(f"{{{NS}}}Event"):

    # Extract Event ID
    event_id = event.find(f".//{{{NS}}}EventID").text

    # Extract Timestamp
    timestamp = event.find(f".//{{{NS}}}TimeCreated").get("SystemTime")

    # Extract all Data fields (username, IP, logon type, etc.)
    data_fields = event.findall(f".//{{{NS}}}Data")
```

---

## Brute Force Detection Logic

Same principle as Apache log brute force detection — use a dictionary to count
`4625` (Failed Login) events per username or source IP, and flag anything
exceeding a threshold:

```python
# Count failed attempts per IP
failed_attempts = dict()

if event_id == "4625":
    source_ip = ...  # extracted from EventData
    failed_attempts[source_ip] = failed_attempts.get(source_ip, 0) + 1

# Flag IPs exceeding threshold
THRESHOLD = 5
for ip, count in failed_attempts.items():
    if count > THRESHOLD:
        print(f"[!!] BRUTE FORCE DETECTED: {ip} -> {count} failed attempts")
```

---

## Key Forensic Notes

- Always analyze a **copy** of the `.evtx` or exported XML file — never the original.
- Verify the **SHA-256 hash** of the log file before and after analysis to confirm it was not altered. *(See File Hasher Tool in this repository.)*
- Event Log **timestamps are in UTC** by default in the XML export — no timezone normalization needed unlike Apache logs.
- Sophisticated attackers may **clear the Event Log entirely** — the act of clearing itself generates **Event ID 1102** (Security log cleared) or **Event ID 104** (System log cleared), which are themselves forensic red flags.
- Attackers may also use **multiple accounts** to stay under the brute force threshold per username. Always review the full 4625 section manually even when no alert fires.
- **Event ID 4648** (Login with explicit credentials) combined with **4624** from an unusual source IP is a strong indicator of **lateral movement** inside a network.

---

## Logon Types — Reading 4624 and 4625 Events

When analyzing login events, the `LogonType` field tells you *how* the login was attempted:

| Logon Type | Meaning | Forensic Significance |
|---|---|---|
| 2 | Interactive (local keyboard) | Physical access to the machine |
| 3 | Network | Remote file share or mapped drive access |
| 4 | Batch | Scheduled task execution |
| 5 | Service | A Windows service logging in |
| 7 | Unlock | Workstation unlock after screensaver |
| 10 | RemoteInteractive | RDP (Remote Desktop) login |
| 11 | CachedInteractive | Login using cached domain credentials (offline) |

A `4625` with `LogonType 10` means a **failed RDP login** — a very common attack vector that attackers use to brute-force remote desktop access.

---

*These notes are part of the Digital Forensics Toolkit learning documentation. All examples use reserved/private IP ranges and fictional usernames for safety.*
