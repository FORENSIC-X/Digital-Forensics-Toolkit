# Module 01 — Forensic Interview Role Play
## Data Breach Incident Response — DataSafe Solutions

**Course:** Cybersecurity: Digital Forensics — Macquarie University (Coursera)
**Module:** 01 — Introduction to Digital Forensics Processes
**Activity:** Role Play — Forensic Interview for a Data Breach Incident
**Role:** Junior Digital Forensics Analyst at a Cybersecurity Firm
**Scenario:** Active data breach investigation at a client site — DataSafe Solutions

---

## Scenario Brief

A corporate client reported a suspected data breach following a phishing campaign targeting their marketing and sales employees. Several employees clicked malicious links before a warning could be issued. Shortly after, unusual network activity and unauthorized file access were detected by the network administrator at approximately 10:30 AM.

As the responding analyst, the objective was to gather information, reconstruct the attack chain, direct evidence collection, and prescribe immediate eradication steps.

---

## Attack Timeline — Reconstructed from Logs and Interviews

| Time | Event |
|---|---|
| ~09:30 AM | Phishing emails delivered to marketing and sales employees, disguised as internal IT security alerts |
| ~09:30–10:00 AM | Employees click the malicious link and unknowingly execute the payload on their workstations |
| ~09:45 AM | Payload performs credential harvesting via LSASS memory dump on compromised workstations |
| ~09:45–10:15 AM | Attacker uses stolen credentials to laterally move from compromised workstations to the database server |
| ~09:45–10:15 AM | Bulk SELECT statements executed against customer PII and encrypted financial data tables using legitimate but compromised credentials |
| ~10:00–10:15 AM | Stolen database records zipped and uploaded via HTTP POST from compromised workstation into web server temporary upload directory |
| ~10:00–10:15 AM | Scheduled task created on web server with elevated privileges to execute script from temporary directory |
| ~10:00–10:15 AM | Web server establishes outbound connection to external C2 IP and exfiltrates the staged data |
| 10:30 AM | Network administrator Jamie detects unusual outbound traffic from web server on monitoring console |
| 10:30 AM | Affected systems isolated, administrative passwords changed, C2 IP blocked at firewall level |

---

## Full Attack Chain Reconstruction

### Stage 1 — Initial Compromise (The Beachhead)

The attack began with a phishing email campaign targeting marketing and sales employees. The emails were crafted to impersonate internal IT alerts, complete with the company logo and a sender address visually similar to the internal IT support address. Employees were prompted to click a link to install an "urgent security update."

Employees who clicked the link downloaded and executed the **payload** — the actual malicious program disguised as a legitimate update installer. The moment an employee clicked Run, the payload executed on their workstation and the attacker established a foothold inside the corporate network.

**The marketing and sales workstations became the attacker's beachhead — the initial point of entry and the pivot platform for everything that followed.**

---

### Stage 2 — Credential Harvesting (How Passwords Were Stolen Without Being Typed)

A critical question in this investigation was: *if employees never typed their passwords into a fake login page, how did the attacker obtain valid database credentials?*

Once the payload executed locally on a workstation, it had operating system-level access to that machine. It did not need the user to type anything. Three common techniques payloads use to harvest credentials silently:

**LSASS Memory Dumping**
On Windows corporate networks, the Local Security Authority Subsystem Service (`lsasrv.dll`) caches user credentials in RAM after login so employees don't have to re-authenticate to every network resource manually. The payload reads the contents of RAM, locates this specific memory block, and extracts the cached password hashes or plaintext credentials directly.

**Browser and Token Stealing**
Payloads scan local profile folders for credential databases used by browsers (Chrome, Edge) and email clients (Outlook), extracting saved passwords and active session tokens.

**Kerberos Token Manipulation**
In Active Directory environments, once a workstation is compromised, the attacker can steal the Kerberos network tickets assigned to the logged-in user. These tickets can be used to authenticate to other systems across the network — such as the database server — without ever knowing the plaintext password.

In this case, the database query logs showed that access was made using **legitimate credentials** with no brute-force pattern — confirming that valid stolen credentials, not guessing, were used. The failed login attempts seen just prior to the successful queries confirm the attacker first attempted brute-force, failed, then switched to the harvested credentials.

---

### Stage 3 — Lateral Movement (Pivoting to the Database)

Using the stolen credentials harvested from the compromised workstations, the attacker authenticated to the database server using legitimate protocols — making the access appear as normal user activity and bypassing brute-force detection entirely.

The unusual internal network connections observed between marketing workstations and the database server during the 09:45–10:15 AM window in the network monitoring console confirmed this lateral movement.

---

### Stage 4 — Data Exfiltration (The Theft)

With database access established, the attacker executed multiple bulk `SELECT` statements targeting:
- Customer names and contact information (PII)
- Encrypted financial records

The database query logs for the 09:45–10:15 AM window, filtered by the compromised marketing/sales credentials, confirmed large data transfers consistent with bulk export. **Data exfiltration was confirmed as the primary objective.**

---

### Stage 5 — Staging and Exfiltration via Web Server

Rather than exfiltrating data directly from the database server — which would have triggered egress alerts — the attacker used the compromised marketing workstation as a proxy to upload the stolen records to the web server.

The web server access logs revealed:
- Unusual HTTP POST requests from an internal IP corresponding to a compromised workstation
- A `.zip` archive uploaded to the web server's temporary upload directory during the critical window
- A new scheduled task created on the web server, configured to execute a script from that temporary directory with elevated privileges

The web server then established an outbound connection to the external C2 IP address and pushed the staged data out — completing the exfiltration.

**The web server acted as a laundry machine for the stolen data — cleaning the trail between the database and the internet.**

---

### Stage 6 — Persistence Mechanism

The scheduled task created on the web server was not just for the initial exfiltration. It was the attacker's **fallback loop** — designed to survive even if the C2 IP was blocked. The task, running with elevated privileges, would periodically execute the script and attempt to re-establish contact with backup C2 infrastructure.

Blocking the IP at the firewall killed the current C2 channel. But without deleting the scheduled task and wiping the temporary directory, the attacker retained a dormant persistence mechanism inside the network.

---

## Evidence Collected

| Evidence | Source | Forensic Value |
|---|---|---|
| Network monitoring console logs | Main network monitoring system | Confirmed outbound traffic to C2 IP |
| Firewall logs | Perimeter firewall | Identified and confirmed suspicious external IP |
| Database query logs (09:45–10:15 AM) | Compromised database server | Confirmed bulk SELECT exfiltration using stolen credentials |
| Web server application and access logs | Compromised web server | Confirmed HTTP POST upload and .zip staging |
| Web server system and scheduled task logs | Compromised web server | Confirmed persistence mechanism creation |
| Database server authentication logs | Compromised database server | Confirmed failed brute-force followed by successful credential use |
| List of employees who clicked phishing links | IT Manager | Identified the five beachhead workstations |

---

## Eradication Steps Prescribed

Three immediate actions were directed upon concluding the investigation:

**1. Remove the persistence mechanism**
Delete the scheduled task on the web server immediately. Wipe the entire temporary upload directory to eliminate any remaining malicious scripts or staged files.

**2. Eliminate the beachhead**
Completely wipe and re-image all five compromised marketing and sales workstations. The payload on these machines is still present and the attacker retains local access through them. Re-imaging is the only way to guarantee complete eradication — antivirus scanning is insufficient for an active compromise of this nature.

**3. Invalidate all compromised credentials**
Force a global password reset for every user account with database access — not just administrative accounts. Since the attacker used legitimate stolen credentials that appeared as normal traffic, any account that touched the database during or before the breach window must be treated as potentially compromised.

---

## Key Concepts Learned

### What is a Payload?
The payload is the actual malicious component delivered by an attack. In a phishing attack, the delivery mechanism is the email and the link — the payload is the malicious file that executes on the victim's machine. Like a missile: the rocket delivers the warhead. The email delivers the payload.

### What is a C2 (Command and Control) Server?
When a payload infects a machine, it needs instructions. It reaches out over the internet to a server controlled by the attacker — the C2 server. The C2 address is the contact point. The payload is the spy on the inside; the C2 is the handler's phone number at headquarters. Blocking the C2 IP cuts the communication channel but does not remove the spy.

### Why Blocking the C2 IP is Not Enough
Blocking the C2 IP kills the current communication channel only. If a persistence mechanism (like the scheduled task found here) remains on the compromised system, it will attempt to contact backup C2 infrastructure automatically. Full eradication requires removing both the communication channel and the persistence mechanism.

### Credential Theft Without a Fake Login Page
Employees never typed their passwords into a fake page — yet their credentials were stolen. Once a payload executes locally, it can dump credentials directly from Windows memory (LSASS), extract saved passwords from browsers, or steal Kerberos network tokens — all without any user interaction beyond the initial click.

---

## DPDPA Compliance Note

The compromised data included customer PII and financial records. Under the **Digital Personal Data Protection Act (DPDPA) 2023**, organizations processing personal data are required to implement appropriate technical security measures to protect data at rest and in transit. The IT Manager confirmed that not all data at rest was encrypted with AES-256.

This breach constitutes a potential DPDPA violation on two grounds:
- Failure to adequately secure personal data at rest
- A reportable personal data breach that must be notified to the Data Protection Board of India within the prescribed timeframe

Recommendation made to the client: implement AES-256 encryption for all personal data stored in databases, review data minimization practices, and establish a formal breach notification procedure.

---

## Gap Identified — Task 2 Feedback

The course evaluator noted that the forensic investigation process was not explicitly explained to the client before diving into technical questioning.

**Honest assessment:** In an active breach with ongoing exfiltration, stopping the threat takes absolute priority over client briefings. However, the underlying principle is valid — briefly setting expectations with a non-technical client at the outset (what evidence will be collected, how chain of custody will be maintained, what actions they should and should not take) prevents well-intentioned but destructive client actions like wiping systems before forensic imaging can be completed.

In future engagements, a 60-second verbal briefing covering these three points before beginning interviews is the correct professional practice:
1. Do not touch, restart, or wipe any affected system until cleared
2. All evidence will be hashed before examination to ensure integrity
3. Findings will be documented in a formal incident report

---

## Forensic Summary

> *A phishing campaign targeting marketing and sales employees delivered a payload that established a beachhead on five employee workstations. The payload harvested cached credentials from workstation memory via LSASS dump. Using stolen legitimate credentials, the attacker laterally moved to the database server and executed bulk SELECT queries against customer PII and encrypted financial records during a 30-minute window between 09:45 and 10:15 AM. Exfiltrated data was zipped and staged on the web server via HTTP POST from a compromised workstation, then pushed to an external C2 IP. A scheduled task with elevated privileges was created on the web server as a persistence mechanism. The C2 channel was neutralized by firewall block at 10:30 AM. Full eradication requires re-imaging of all five beachhead workstations, deletion of the web server scheduled task and temporary directory, and a global password reset for all database-accessing accounts. A DPDPA breach notification obligation is likely triggered by the confirmed exfiltration of customer personal data.*