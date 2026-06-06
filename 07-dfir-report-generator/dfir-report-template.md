# DIGITAL FORENSICS & INCIDENT RESPONSE REPORT

---

## DOCUMENT CONTROL

| Field | Details |
|---|---|
| **Report Title** | Digital Forensics & Incident Response Report — Data Breach Investigation |
| **Case Reference** | CASE-MU-2026-001 |
| **Client Organization** | A Software Solutions Firm, Bengaluru |
| **Investigating Firm** | [Your Firm Name] |
| **Lead Analyst** | [Analyst Name] |
| **Report Classification** | CONFIDENTIAL |
| **Report Status** | FINAL |
| **Date of Incident** | [Date of Incident] |
| **Date of Engagement** | [Date of Engagement] |
| **Date of Report** | [Date of Report] |
| **Report Version** | 1.0 |

---

## CHAIN OF CUSTODY

| Evidence ID | Description | Collected By | Date & Time | Hash (SHA-256) | Current Location |
|---|---|---|---|---|---|
| EVD-001 | Network monitoring console logs | [Analyst Name] | [Date] 10:45 AM | [hash] | Secure Evidence Locker |
| EVD-002 | Firewall logs | [Analyst Name] | [Date] 10:47 AM | [hash] | Secure Evidence Locker |
| EVD-003 | Database server query logs | [Analyst Name] | [Date] 11:30 AM | [hash] | Secure Evidence Locker |
| EVD-004 | Web server application and access logs | [Analyst Name] | [Date] 11:32 AM | [hash] | Secure Evidence Locker |
| EVD-005 | Web server system and scheduled task logs | [Analyst Name] | [Date] 11:35 AM | [hash] | Secure Evidence Locker |
| EVD-006 | Database server authentication logs | [Analyst Name] | [Date] 11:37 AM | [hash] | Secure Evidence Locker |
| EVD-007 | Forensic images of five compromised workstations | [Analyst Name] | [Date] 12:30 PM | [hash] | Secure Evidence Locker |

> All evidence items were hashed using SHA-256 immediately upon collection. Hash values were verified before and after examination to confirm evidence integrity throughout the investigation.

---

## TABLE OF CONTENTS

1. Executive Summary
2. Scope of Investigation
3. Investigation Methodology
4. Timeline of Events
5. Technical Findings
6. Attack Chain Reconstruction
7. Impact Assessment
8. Eradication and Remediation
9. Compliance Implications
10. Recommendations
11. Conclusion
12. Appendices

---

## 1. EXECUTIVE SUMMARY

On [Date of Incident], the client organization experienced a targeted data breach originating from a phishing campaign directed at employees in the marketing and sales departments. Five employees clicked a malicious link contained in a phishing email disguised as an internal IT security alert. The link delivered a malicious payload that executed on the victims' workstations, establishing an attacker foothold inside the corporate network.

The attacker subsequently harvested valid employee credentials from workstation memory, used those credentials to laterally move to a database server, and executed bulk data extraction queries against tables containing customer personally identifiable information (PII) and encrypted financial records. The exfiltrated data was staged on an internal web server and transmitted to an external Command and Control (C2) server via an outbound connection.

The breach was detected at 10:30 AM by the network administrator, who identified unusual outbound traffic from the web server. Affected systems were isolated, administrative passwords were changed, and the C2 IP address was blocked at the firewall level. The investigating firm was engaged and arrived on site shortly thereafter.

**Key Findings:**
- Five employee workstations were compromised via phishing payload execution
- Valid credentials were harvested from workstation memory without user interaction
- Customer PII and encrypted financial records were confirmed exfiltrated
- A persistence mechanism (scheduled task) was installed on the web server
- The C2 communication channel has been neutralized but the persistence mechanism required immediate removal

---

## 2. SCOPE OF INVESTIGATION

### 2.1 In Scope

- Five compromised marketing and sales employee workstations
- Primary database server hosting customer PII and financial records
- Web server used as a staging platform for data exfiltration
- Network monitoring console and firewall logs
- All log sources covering the period 09:30 AM to 10:30 AM on the date of incident

### 2.2 Out of Scope

- Systems not connected to the affected network segment
- Employee personal devices
- Cloud infrastructure not directly involved in the breach

### 2.3 Objectives

- Reconstruct the full attack chain from initial compromise to exfiltration
- Identify all affected systems and data categories
- Determine the scope of data exfiltration
- Identify and document any persistence mechanisms
- Prescribe eradication and remediation steps
- Assess compliance implications under applicable data protection legislation

---

## 3. INVESTIGATION METHODOLOGY

This investigation was conducted in accordance with the standard digital forensics process lifecycle:

| Phase | Actions Taken |
|---|---|
| **Identification** | Interviewed IT Manager and network administrator to identify affected systems, evidence sources, and incident timeline |
| **Preservation** | SHA-256 hashes calculated for all log files and forensic disk images immediately upon collection. Write protection applied before examination |
| **Collection** | Log files extracted from network monitoring console, firewall, database server, and web server. Forensic disk images acquired from all five compromised workstations |
| **Examination** | Log files parsed and filtered by timeframe and credential. Disk images examined for malware artifacts, credential dumping tools, and persistence mechanisms |
| **Analysis** | Artifacts correlated across all evidence sources to reconstruct the complete attack chain and confirm exfiltration scope |
| **Reporting** | Findings documented in this report with supporting evidence references, eradication guidance, and compliance assessment |

---

## 4. TIMELINE OF EVENTS

| Time | Event | Evidence Source |
|---|---|---|
| ~09:30 AM | Phishing emails delivered to marketing and sales employees, impersonating internal IT security alerts | Employee reports, email server logs |
| ~09:30–10:00 AM | Five employees click malicious link and execute payload on workstations | Employee reports, workstation forensic images |
| ~09:45 AM | Payload performs credential harvesting via LSASS memory dump on compromised workstations | Workstation forensic images (EVD-007) |
| ~09:45–10:15 AM | Attacker uses stolen credentials to authenticate to database server and execute bulk SELECT queries | Database query logs (EVD-003) |
| ~09:45–10:15 AM | Bulk customer PII and encrypted financial records exfiltrated from database | Database query logs (EVD-003) |
| ~10:00–10:15 AM | Stolen data compressed into .zip archive and uploaded via HTTP POST to web server temporary directory | Web server access logs (EVD-004) |
| ~10:00–10:15 AM | Scheduled task created on web server with elevated privileges to execute script from temporary directory | Web server system logs (EVD-005) |
| ~10:00–10:15 AM | Web server establishes outbound connection to external C2 IP and transmits staged data | Firewall logs (EVD-002), Network monitoring logs (EVD-001) |
| 10:30 AM | Network administrator detects unusual outbound traffic from web server on monitoring console | Network monitoring logs (EVD-001) |
| 10:32 AM | Affected systems isolated from network | IT Manager statement |
| 10:35 AM | Administrative passwords changed across affected systems | IT Manager statement |
| 10:40 AM | External C2 IP address blocked at firewall level | Firewall logs (EVD-002) |
| 10:45 AM | Investigating firm engaged and evidence collection commenced | Chain of custody log |

---

## 5. TECHNICAL FINDINGS

### 5.1 Initial Access — Phishing Campaign

The attacker delivered phishing emails to marketing and sales department employees. The emails were designed to impersonate internal IT communications, incorporating the company logo and a sender address visually similar to the legitimate internal IT support address. The emails instructed recipients to click a link to install an "urgent security update."

Five employees clicked the link prior to a company-wide warning being issued. The link delivered a malicious executable disguised as a software update installer.

**Affected Employees:** 5 (marketing and sales departments)
**Delivery Method:** Email phishing — internal IT alert impersonation
**MITRE ATT&CK Technique:** T1566.002 — Phishing: Spearphishing Link

---

### 5.2 Payload Execution and Credential Harvesting

Upon execution on the victim workstations, the payload performed credential harvesting by reading cached credentials from Windows LSASS (Local Security Authority Subsystem Service) memory. This technique extracts credentials cached in RAM after user login without requiring the user to re-enter their password or interact with any fake login interface.

The database server authentication logs (EVD-006) confirm that access to the database server was made using legitimate employee credentials — no brute-force pattern was detected in the successful access events. Failed login attempts immediately prior to the successful access confirm that the attacker first attempted credential guessing before switching to the harvested credentials.

**Harvesting Technique:** LSASS Memory Dump
**MITRE ATT&CK Technique:** T1003.001 — OS Credential Dumping: LSASS Memory

---

### 5.3 Lateral Movement to Database Server

Using harvested credentials, the attacker authenticated to the primary database server from the compromised workstations using legitimate protocols. The network monitoring console logs (EVD-001) confirm unusual internal connections between marketing workstations and the database server during the 09:45–10:15 AM window.

Because legitimate credentials were used, the access did not trigger brute-force or anomalous authentication alerts — demonstrating the effectiveness of credential-based lateral movement against organizations without behavioral analytics.

**MITRE ATT&CK Technique:** T1078 — Valid Accounts

---

### 5.4 Data Exfiltration from Database Server

Database query logs (EVD-003) filtered for the 09:45–10:15 AM window and scoped to the compromised marketing and sales credentials revealed the following:

- Multiple bulk `SELECT` statements targeting tables containing customer names and contact information
- `SELECT` queries against tables containing encrypted financial records
- Log entries consistent with large-scale data export operations

**Data Categories Confirmed Exfiltrated:**
- Customer personally identifiable information (names, contact details)
- Encrypted financial records

**MITRE ATT&CK Technique:** T1213 — Data from Information Repositories

---

### 5.5 Staging on Web Server

Web server application and access logs (EVD-004) revealed the following activity during the 09:45–10:15 AM window:

- Multiple HTTP POST requests originating from an internal IP address corresponding to a compromised marketing workstation
- Requests directed at the web server's temporary upload directory
- A `.zip` archive file uploaded to the temporary directory — timestamp falls within the critical window

The web server was used as an intermediary staging platform to bypass direct database egress restrictions. Exfiltrating directly from the database server would have triggered data loss prevention alerts. Routing through the web server's temporary directory avoided those controls.

**MITRE ATT&CK Technique:** T1074.001 — Data Staged: Local Data Staging

---

### 5.6 Persistence Mechanism

Web server system and scheduled task logs (EVD-005) revealed the creation of a new scheduled task on the web server during the critical window. The task was configured to:

- Execute a script located in the temporary upload directory
- Run with elevated system privileges
- Execute automatically on a recurring schedule

This scheduled task represents a persistence mechanism designed to survive the blocking of the initial C2 IP address. Even after the firewall block, this task would periodically attempt to re-establish contact with backup C2 infrastructure and re-exfiltrate any newly staged data.

**MITRE ATT&CK Technique:** T1053.005 — Scheduled Task/Job: Scheduled Task

---

### 5.7 Command and Control Communication

Firewall logs (EVD-002) and network monitoring logs (EVD-001) confirm persistent outbound connections from the web server to an external IP address not associated with any known vendor or service used by the organization. This IP is assessed with high confidence to be attacker-controlled C2 infrastructure.

The C2 IP address was blocked at the firewall level at 10:40 AM. No further unauthorized outbound connections to this address have been detected since the block was applied.

**MITRE ATT&CK Technique:** T1071.001 — Application Layer Protocol: Web Protocols

---

## 6. ATTACK CHAIN RECONSTRUCTION

```
[ATTACKER]
    |
    | Phishing Email (Internal IT Alert Impersonation)
    ↓
[MARKETING/SALES WORKSTATIONS] ← Beachhead
    |
    | Payload Execution → LSASS Credential Dump
    |
    | Lateral Movement (Stolen Credentials)
    ↓
[DATABASE SERVER]
    |
    | Bulk SELECT Queries → Customer PII + Financial Records
    |
    | HTTP POST (.zip upload via compromised workstation)
    ↓
[WEB SERVER] ← Staging Ground
    |
    | Scheduled Task (Persistence Mechanism installed)
    |
    | Outbound Connection
    ↓
[EXTERNAL C2 SERVER] ← Data Received by Attacker
```

---

## 7. IMPACT ASSESSMENT

### 7.1 Systems Affected

| System | Role | Status |
|---|---|---|
| 5 x Marketing/Sales Workstations | Beachhead / Credential Source | Compromised — isolated |
| Primary Database Server | Data Source | Accessed — isolated |
| Web Server | Staging Platform | Compromised — isolated |

### 7.2 Data Impact

| Data Category | Status |
|---|---|
| Customer PII (names, contact details) | Confirmed exfiltrated |
| Encrypted financial records | Confirmed exfiltrated |
| Other database tables | Under review |

### 7.3 Severity Assessment

**Overall Severity: CRITICAL**

Confirmed exfiltration of customer PII and financial data, active persistence mechanism installed, attacker demonstrated full network traversal capability from initial access to external exfiltration.

---

## 8. ERADICATION AND REMEDIATION

The following actions were prescribed and confirmed as initiated by the client's IT team:

### Immediate Actions (Completed)

- [x] External C2 IP address blocked at firewall level
- [x] All affected systems isolated from the network
- [x] Administrative passwords changed

### Required Actions (To Be Completed)

**Action 1 — Remove Persistence Mechanism**
Delete the scheduled task identified on the web server immediately. Wipe the entire temporary upload directory to remove all malicious scripts and staged files. Verify deletion via system log review.

**Action 2 — Eradicate Beachhead**
Wipe and re-image all five compromised marketing and sales workstations from a known clean baseline. Antivirus scanning is insufficient — the payload has operating system-level access and re-imaging is the only guarantee of complete eradication.

**Action 3 — Invalidate Compromised Credentials**
Force a global password reset for all accounts with database access — administrative and non-administrative. Any account active on the network during the breach window must be treated as potentially compromised.

**Action 4 — Web Server Integrity Verification**
Conduct a full file integrity check on the web server to identify any additional malicious files, web shells, or configuration changes made by the attacker beyond the identified scheduled task and temporary directory.

**Action 5 — Threat Intelligence Sharing**
Submit the identified C2 IP address to relevant threat intelligence platforms (VirusTotal, AbuseIPDB) and notify the Indian Computer Emergency Response Team (CERT-In) as required under applicable reporting obligations.

---

## 9. COMPLIANCE IMPLICATIONS

### Digital Personal Data Protection Act (DPDPA) 2023

The confirmed exfiltration of customer personally identifiable information triggers obligations under the **Digital Personal Data Protection Act (DPDPA) 2023**:

**Breach Notification Obligation**
The organization is required to notify the Data Protection Board of India of the personal data breach within the timeframe prescribed under the Act. Notification to affected data principals (customers whose data was exfiltrated) is also required.

**Security Obligation Violation**
The Act requires data fiduciaries to implement appropriate technical and organizational measures to protect personal data. The investigation identified that not all personal data at rest was encrypted with AES-256 or equivalent — a gap that contributed to the exposure of customer data.

**Recommended Immediate Compliance Actions:**
- Engage legal counsel to prepare breach notification filings
- Document all remediation steps taken as evidence of good-faith response
- Conduct a full data audit to determine the complete scope of affected data principals
- Implement AES-256 encryption for all personal data stored at rest

---

## 10. RECOMMENDATIONS

### Immediate (0–7 Days)
- Complete all eradication actions listed in Section 8
- File breach notification with the Data Protection Board of India
- Notify affected customers as required under DPDPA

### Short Term (7–30 Days)
- Deploy an Endpoint Detection and Response (EDR) solution across all workstations to detect credential dumping and lateral movement in real time
- Implement network segmentation to prevent direct workstation-to-database server communication
- Enable LSASS protection (Windows Credential Guard) on all workstations to prevent memory-based credential harvesting
- Encrypt all personal data at rest using AES-256

### Medium Term (30–90 Days)
- Deploy a Security Information and Event Management (SIEM) solution for centralized log correlation and anomaly detection
- Conduct mandatory phishing awareness training for all employees, with simulated phishing exercises
- Implement Multi-Factor Authentication (MFA) for all systems — particularly database and administrative access
- Establish a formal Incident Response Plan with defined roles, communication procedures, and escalation paths
- Conduct a full penetration test to identify remaining vulnerabilities across the network

### Long Term (90+ Days)
- Implement a Data Loss Prevention (DLP) solution to monitor and block unauthorized bulk data transfers
- Establish a threat intelligence program to proactively monitor for indicators of compromise associated with known threat actors
- Schedule annual DFIR retainer engagements for proactive threat hunting

---

## 11. CONCLUSION

The investigation determined that the client organization suffered a targeted data breach resulting in the confirmed exfiltration of customer PII and encrypted financial records. The attack exploited a combination of human vulnerability (phishing), inadequate endpoint protection (no LSASS memory protection), insufficient network segmentation (workstation-to-database direct access), and gaps in data-at-rest encryption.

The attacker demonstrated a high level of operational sophistication — using legitimate stolen credentials to avoid brute-force detection, routing exfiltration through the web server to bypass database egress controls, and installing a persistence mechanism to survive initial remediation.

The immediate C2 channel has been neutralized. Full eradication is contingent on completion of the actions prescribed in Section 8. The organization faces potential regulatory consequences under the DPDPA 2023 and is advised to engage legal counsel immediately.

---

## 12. APPENDICES

### Appendix A — MITRE ATT&CK Techniques Identified

| Technique ID | Technique Name | Phase |
|---|---|---|
| T1566.002 | Phishing: Spearphishing Link | Initial Access |
| T1003.001 | OS Credential Dumping: LSASS Memory | Credential Access |
| T1078 | Valid Accounts | Lateral Movement |
| T1213 | Data from Information Repositories | Collection |
| T1074.001 | Data Staged: Local Data Staging | Collection |
| T1053.005 | Scheduled Task/Job: Scheduled Task | Persistence |
| T1071.001 | Application Layer Protocol: Web Protocols | Command and Control |

### Appendix B — Evidence Hash Register

All evidence items were hashed using SHA-256 immediately upon collection and verified after examination. Hash values are maintained in the secure evidence register held by the investigating firm.

### Appendix C — Glossary

**Beachhead:** The initial point of compromise used by an attacker to establish a foothold inside a network.

**C2 (Command and Control):** Attacker-controlled infrastructure used to send instructions to and receive data from compromised systems.

**Lateral Movement:** Techniques used by an attacker to progressively move through a network after initial compromise.

**LSASS:** Local Security Authority Subsystem Service — a Windows process that caches user credentials in memory.

**Payload:** The malicious component of an attack that executes on the victim's system.

**Persistence Mechanism:** A technique used by an attacker to maintain access to a compromised system across reboots or remediation attempts.

**PII:** Personally Identifiable Information — data that can be used to identify an individual.

---

*This report is classified CONFIDENTIAL and intended solely for the use of the client organization and authorized legal counsel. Unauthorized disclosure is prohibited.*

---

**Lead Analyst Signature:** ___________________

**Date:** ___________________

**Reviewing Analyst Signature:** ___________________

**Date:** ___________________
