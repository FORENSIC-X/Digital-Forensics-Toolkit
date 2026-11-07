# Digital Forensics & Incident Response — Complete Learning Plan

A structured, end-to-end learning plan for the full DFIR Learning Stack. Built from scratch through self-study, hands-on tool usage, guided platforms, and unguided case simulations.

---

## Progress Legend

- ✅ Complete
- 🔄 In Progress
- 🔲 Pending

---

## Phase 1 — Foundations & Core Concepts ✅

### 1.1 Digital Forensics Overview ✅
- ✅ The four phases of forensic investigation: Identification, Preservation, Analysis, Reporting
- ✅ Chain of custody — what it is and why it matters
- ✅ Evidence integrity — SHA-256 hashing before and after analysis
- ✅ Write blocking — preventing modification of evidence files
- ✅ The difference between SHA-256 (hashing) and AES-256 (encryption)
- ✅ MAC Times — Modified, Accessed, Created timestamps and their forensic significance

### 1.2 File Hashing Tool ✅
- ✅ How hashlib works in Python (MD5, SHA-1, SHA-256)
- ✅ Reading files in `rb` mode as a software write blocker
- ✅ Chunk-based reading for large files (4096-byte blocks)
- ✅ Built: `file_hasher.py`

### 1.3 Metadata Extraction ✅
- ✅ MAC times via `os.stat()` — what each timestamp actually records
- ✅ EXIF metadata in images — GPS, camera model, software, timestamps
- ✅ When EXIF is stripped (WhatsApp, cropping, screenshots) and why it matters
- ✅ EXIF extraction using Pillow (PIL)
- ✅ Built: `metadata_extractor.py`

### 1.4 File Signature Analysis (Magic Numbers) ✅
- ✅ What magic numbers are and why extensions can be faked
- ✅ File masquerading — renaming `.exe` to `.jpg` to bypass detection
- ✅ Reading raw bytes in `rb` mode
- ✅ Building a magic number dictionary (25+ signatures)
- ✅ Extension vs. true type comparison and FORENSIC ALERT logic
- ✅ Built: `file_signature_analyzer.py` (CLI + FastAPI backend + browser UI)

### 1.5 Log Analysis & Parsing ✅
- ✅ Apache Combined Log Format structure
- ✅ Regex-based log parsing with named capture groups
- ✅ Brute force detection via failed attempt thresholds
- ✅ Identifying suspicious IPs and 401/403 sequences
- ✅ Built: `log_analyzer.py` with `basic-access.log` sample

---

## Phase 2 — Virtual Environment & Lab Setup ✅

- ✅ VM isolation principles — why malware analysis must happen in a VM
- ✅ VM escape risks, shared folder risks, network bridging risks
- ✅ VirtualBox setup on Windows host
- ✅ Ubuntu 26.04 LTS VM installation (Forensics-Lab)
- ✅ RAM and CPU allocation strategy for dual-VM setup
- ✅ Snapshot strategy — "Clean-Install" and "Forensics-Ready" snapshots
- ✅ Two-VM architecture: Forensics-Lab (DFIR work) + WebDev-Lab (web projects)
- ✅ Documented: `Forensic-Virtual-Env-Setup.md`

---

## Phase 3 — Industry Tool: ExifTool ✅

- ✅ ExifTool installation and basic usage
- ✅ Extracting metadata from images, documents, and other file types
- ✅ Comparing ExifTool output to Python's Pillow-based extraction
- 🔄 Case investigations: CF-2026-001, CF-2026-002, CF-2026-003, ...

---

## Phase 4 — Coursera: Macquarie University Introduction to DFIR 🔄

- ✅ Module 1: Incident response lifecycle, roles, DFIR methodology
- ✅ Module 1: Data breach roleplay exercise
- ✅ Module 1: Incident response dialogue exercise
- ✅ Module 2: Evidence handling, forensic principles, legal considerations

---

## Phase 5 — Windows Event Log Theory ✅

- ✅ Windows Event Log structure — Security.evtx, System.evtx, Application.evtx
- ✅ Location: `C:\Windows\System32\winevt\Logs\`
- ✅ Forensically significant Event IDs: 4624, 4625, 4634, 4648, 4672, 4698, 4720, 4726, 7034, 7045
- ✅ Logon Types: 2 (Interactive), 3 (Network), 4 (Batch), 5 (Service), 7 (Unlock), 10 (RDP), 11 (Cached)
- ✅ The `.evtx` binary format problem and XML export solution
- ✅ XML namespace handling in Python's `xml.etree.ElementTree`
- ✅ Core XML parsing logic with namespace-aware `find()` calls
- ✅ Brute force detection logic for Event ID 4625
- ✅ Event IDs 1102 / 104 — log clearing as a forensic red flag
- ✅ Documented: `windows-event-logs-analysis-notes.md`

---

## Phase 6 — Memory (RAM) Forensics 🔄

### 6.1 Theory 🔄
- 🔄 What a memory dump is and why RAM evidence is volatile
- 🔲 Live memory capture tools: WinPmem (Windows), LiME — Linux Memory Extractor
- 🔲 Memory dump formats: `.raw`, `.mem`, `.vmem`
- 🔲 What lives only in RAM: decrypted malware, active connections, command history, credentials
- 🔲 Process injection and hollowing — how malware hides in legitimate processes
- 🔲 Fileless malware — living entirely in memory, never touching disk

### 6.2 Volatility 3 Setup 🔄
- 🔄 Installing Volatility 3 in Ubuntu VM
- 🔲 Understanding the plugin architecture
- 🔲 Symbol tables — why Volatility needs them for different OS versions

### 6.3 Core Volatility 3 Plugins 🔲
- 🔲 `windows.pslist` — enumerate all running processes
- 🔲 `windows.pstree` — visualize parent-child process relationships
- 🔲 `windows.netscan` — enumerate active and recently closed network connections
- 🔲 `windows.cmdline` — extract command-line arguments for each process
- 🔲 `windows.dlllist` — list DLLs loaded by each process
- 🔲 `windows.malfind` — detect injected/shellcode regions in process memory
- 🔲 `windows.hashdump` — extract NTLM password hashes from memory
- 🔲 `windows.filescan` — find file objects mapped into memory
- 🔲 `windows.handles` — enumerate open handles per process
- 🔲 `windows.vadinfo` — virtual address descriptor analysis

### 6.4 Investigation Practice 🔲
- 🔲 Download practice memory dump (CTF/DFIR challenge image)
- 🔲 Conduct full investigation following the thread: pslist → netscan → cmdline → malfind
- 🔲 Identify malicious process, C2 connection, injected shellcode
- 🔲 Write Investigation Report: CF-2026-004
- 🔲 Complete 2-3 additional memory forensics cases
- 🔲 Documented: `memory-forensics-notes.md`

---

## Phase 7 — Windows Event Log Analysis with Industry Tools 🔲

### 7.1 Chainsaw
- 🔲 What Chainsaw is and how it differs from manual analysis
- 🔲 Installation in Ubuntu VM
- 🔲 Running Chainsaw against `.evtx` files
- 🔲 SIGMA rule detection — understanding the rule format
- 🔲 Detecting: brute force, lateral movement, persistence mechanisms
- 🔲 `chainsaw-cheatsheet.md`

### 7.2 Hayabusa
- 🔲 What Hayabusa is — fast forensics and threat hunting on Windows logs
- 🔲 Installation in Ubuntu VM
- 🔲 Running Hayabusa in timeline mode
- 🔲 Comparing Hayabusa output to Chainsaw
- 🔲 `hayabusa-cheatsheet.md`

### 7.3 Python Tool (Self-Written)
- 🔲 Write `windows_event_log_analyzer.py`
- 🔲 Create `sample-security.xml` test file

### 7.4 Investigation Practice 🔲
- 🔲 Investigate a sample `.evtx` file with Chainsaw and Hayabusa
- 🔲 Cross-reference findings with manual Event ID lookup
- 🔲 Write Investigation Reports: CF-2026-007, CF-2026-008

---

## Phase 8 — Disk / File System Forensics 🔲

### 8.1 Theory
- 🔲 Disk image formats: `.dd`, `.E01` (Expert Witness), `.AFF`
- 🔲 File system structure: MFT (NTFS Master File Table), FAT, ext4
- 🔲 File carving — recovering deleted files from unallocated space
- 🔲 Slack space — data remnants in partially used disk sectors
- 🔲 Inode structure on Linux filesystems
- 🔲 Windows artifacts: Prefetch, LNK files, Jump Lists, Recycle Bin (`$I`, `$R`)
- 🔲 Registry forensics preview (full coverage in Coursera module)

### 8.2 Tools
- 🔲 `dd` — creating forensic disk images from physical drives
- 🔲 Autopsy — installation and full GUI walkthrough
- 🔲 Autopsy modules: hash lookup, keyword search, file type identification, timeline
- 🔲 FTK Imager (Windows) — alternative imaging tool
- 🔲 `autopsy-cheatsheet.md`

### 8.3 Investigation Practice
- 🔲 Download practice disk image from DFIR challenge
- 🔲 Load into Autopsy and run full analysis
- 🔲 Recover deleted files, build timeline, identify artifacts
- 🔲 Write Investigation Reports: CF-2026-009, CF-2026-010
- 🔲 Documented: `disk-forensics-notes.md`

---

## Phase 9 — Network Forensics 🔲

### 9.1 Theory
- 🔲 PCAP format — what packet captures contain
- 🔲 TCP/IP layer review for forensics context
- 🔲 C2 (Command & Control) traffic patterns
- 🔲 DNS tunneling — data exfiltration via DNS queries
- 🔲 Beaconing — malware checking in with its C2 at regular intervals
- 🔲 Data exfiltration over HTTP/HTTPS
- 🔲 Port scan signatures in packet captures

### 9.2 Tools
- 🔲 Wireshark — installation, filters, stream following
- 🔲 Wireshark display filters: `ip.addr`, `tcp.port`, `http.request`, `dns`
- 🔲 tshark — CLI equivalent for scripted analysis
- 🔲 NetworkMiner — passive network forensics
- 🔲 `wireshark-cheatsheet.md`
- 🔲 `tshark-cheatsheet.md`

### 9.3 Investigation Practice
- 🔲 Analyze a sample `.pcap` from a CTF/DFIR challenge
- 🔲 Identify C2 traffic, data exfiltration, credential theft over network
- 🔲 Write Investigation Reports: CF-2026-011, CF-2026-012
- 🔲 Documented: `network-forensics-notes.md`

---

## Phase 10 — TryHackMe DFIR Learning Paths 🔲

- 🔲 Complete **SOC Level 1** path (foundational blue team skills)
- 🔲 Complete **DFIR: An Introduction** room
- 🔲 Complete **Volatility** room (guided memory forensics)
- 🔲 Complete **Autopsy** room (guided disk forensics)
- 🔲 Complete **Wireshark** rooms
- 🔲 Complete **Windows Event Logs** room
- 🔲 Complete **Windows Forensics 1 & 2** rooms
- 🔲 Complete **DFIR Learning Path** (full path)
- 🔲 Write room writeups for each → commit to `11-tryhackme-dfir/writeups/`

---

## Phase 11 — Coursera: Windows Forensics 🔲

- 🔲 Windows Registry structure — hives, keys, values
- 🔲 Registry forensics artifacts: UserAssist, ShimCache, MUICache, RecentDocs
- 🔲 Prefetch files — execution evidence (`C:\Windows\Prefetch\`)
- 🔲 Shellbags — folder browsing history
- 🔲 LNK files — shortcut files as evidence of file access
- 🔲 Jump Lists — recent files per application
- 🔲 Recycle Bin forensics (`$I` and `$R` files)
- 🔲 Browser artifacts — history, cache, cookies, downloads
- 🔲 Documented: `windows-os-forensics-notes.md`

---

## Phase 12 — Coursera: Mobile Forensics 🔲

- 🔲 iOS vs Android acquisition methods
- 🔲 Logical, file system, and physical acquisition
- 🔲 iOS artifacts: SQLite databases, plist files, iCloud backups
- 🔲 Android artifacts: call logs, SMS, app data, location history
- 🔲 GPS and location data forensics
- 🔲 Anti-forensics on mobile: encryption, remote wipe
- 🔲 Tools: Cellebrite UFED (theory), open-source alternatives
- 🔲 Documented: `mobile-forensics-notes.md`

---

## Phase 13 — Full Incident Response Simulations 🔲

### Platforms
- 🔲 **CyberDefenders** — multi-artifact IR challenges (memory + disk + network + logs combined)
- 🔲 **BlueTeamLabs Online** — real-world inspired blue team scenarios
- 🔲 **DFIR.training** — curated challenge images

### Deliverables per case
- 🔲 Investigation notes (running log of findings)
- 🔲 Final IR Report including:
  - Executive Summary
  - Timeline of attacker activity
  - Indicators of Compromise (IOCs) — IPs, hashes, filenames, registry keys
  - MITRE ATT&CK technique mapping
  - Recommendations

### Target: Complete at least 4 full multi-tool IR simulations

---

## Phase 14 — Portfolio & GitHub Repo Polish 🔲

- 🔲 Write top-level `README.md` tying the entire repo together
- 🔲 Add a **Tools Used** section distinguishing self-built vs industry tools
- 🔲 Add **Completed Cases** index linking to all IR reports
- 🔲 Ensure all `docs/` theory notes are complete and committed
- 🔲 Add TryHackMe completion badges to README
- 🔲 Add Coursera certificates to README
- 🔲 Pin the repository on GitHub profile

---

## Summary Timeline

| Phase | Topic | Status |
|---|---|---|
| 1 | Foundations + Python Tools | ✅ Complete |
| 2 | VM Lab Setup | ✅ Complete |
| 3 | ExifTool | 🔄 In Progress |
| 4 | Coursera Macquarie | 🔄 In Progress |
| 5 | Windows Event Log Theory | ✅ Complete |
| 6 | Memory Forensics (Volatility 3) | 🔄 In Progress |
| 7 | Windows Event Logs (Chainsaw/Hayabusa) | 🔲 Pending |
| 8 | Disk Forensics (Autopsy + dd) | 🔲 Pending |
| 9 | Network Forensics (Wireshark + tshark) | 🔲 Pending |
| 10 | TryHackMe DFIR Paths | 🔲 Pending |
| 11 | Coursera Windows Forensics | 🔲 Pending |
| 12 | Coursera Mobile Forensics | 🔲 Pending |
| 13 | Full IR Simulations (CyberDefenders) | 🔲 Pending |
| 14 | Portfolio & Repo Polish | 🔲 Pending |

---

*This plan is a living document — update it as each section is completed.*
