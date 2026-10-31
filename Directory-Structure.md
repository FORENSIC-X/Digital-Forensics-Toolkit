# Digital Forensics Toolkit — Repository Directory Structure

Complete directory structure for the full DFIR Learning Stack. Completed sections are marked ✅. Pending sections are marked 🔲.

---

```
Digital-Forensics-Toolkit/
│
├── README.md                          # Top-level repo overview
│
│
├── 01-file-hashing/                   ✅ COMPLETE
│   ├── README.md
│   ├── evidence.txt
│   └── file_hasher.py
│
│
├── 02-metadata-extraction/            ✅ COMPLETE
│   ├── README.md
│   └── metadata_extractor.py
│
│
├── 03-file-signature-analysis/        ✅ COMPLETE
│   ├── README.md
│   └── file_signature_analyzer.py
│
│
├── 04-log-analysis/                   ✅ COMPLETE
│   |── apache-web-server-logs/
│   |    ├── README.md
│   |    ├── basic-access.log
│   |    └── log_analyzer.py
|   └── windows-event-logs/
│
│
├── 05-exiftool-forensics/             ✅ COMPLETE
│   ├── setup.md
│   └── case-investigations/
│       ├── CF-2026-001.md
│       ├── CF-2026-002.md
│       └── CF-2026-003.md
│
│
├── 06-coursera-macquarie/             ✅ COMPLETE
│   ├── module-01/
│   │   ├── notes.md
│   │   ├── data-breach-roleplay.md
│   │   └── incident-response-dialogue.md
│   └── module-02/
│       └── notes.md
│
│
├── 07-memory-forensics/               🔲 PENDING
│   ├── README.md
│   ├── setup.md                       # Volatility 3 installation guide
│   ├── volatility-cheatsheet.md       # Plugin reference sheet
│   ├── memory-dumps/                  # Practice .raw / .mem dump files
│   │   └── .gitkeep
│   └── case-investigations/
│       ├── CF-2026-004.md             # First memory forensics case
│       ├── CF-2026-005.md
│       └── CF-2026-006.md
│
│
├── 08-windows-event-log-analysis/     🔲 PENDING
│   ├── README.md
│   ├── setup.md                       # Chainsaw + Hayabusa installation
│   ├── chainsaw-cheatsheet.md
│   ├── hayabusa-cheatsheet.md
│   ├── sample-logs/                   # Sample .evtx and exported XML files
│   │   ├── sample-security.evtx
│   │   └── sample-security.xml
│   ├── windows_event_log_analyzer.py  # Python CLI tool (self-written)
│   └── case-investigations/
│       ├── CF-2026-007.md
│       └── CF-2026-008.md
│
│
├── 09-disk-forensics/                 🔲 PENDING
│   ├── README.md
│   ├── setup.md                       # Autopsy + dd installation guide
│   ├── autopsy-cheatsheet.md
│   ├── disk-images/                   # Practice disk image files
│   │   └── .gitkeep
│   └── case-investigations/
│       ├── CF-2026-009.md
│       └── CF-2026-010.md
│
│
├── 10-network-forensics/              🔲 PENDING
│   ├── README.md
│   ├── setup.md                       # Wireshark + tshark installation
│   ├── wireshark-cheatsheet.md
│   ├── tshark-cheatsheet.md
│   ├── pcap-samples/                  # Practice .pcap files
│   │   └── .gitkeep
│   └── case-investigations/
│       ├── CF-2026-011.md
│       └── CF-2026-012.md
│
│
├── 11-tryhackme-dfir/                 🔲 PENDING
│   ├── README.md
│   └── writeups/
│       ├── room-01.md
│       ├── room-02.md
│       └── room-03.md
│
│
├── 12-coursera-windows-forensics/     🔲 PENDING
│   ├── module-01/
│   │   └── notes.md
│   ├── module-02/
│   │   └── notes.md
│   └── module-03/
│       └── notes.md
│
│
├── 13-coursera-mobile-forensics/      🔲 PENDING
│   ├── module-01/
│   │   └── notes.md
│   ├── module-02/
│   │   └── notes.md
│   └── module-03/
│       └── notes.md
│
│
├── 14-full-ir-simulations/            🔲 PENDING
│   ├── README.md
│   └── cyberdefenders/
│       ├── case-01/
│       │   ├── investigation-notes.md
│       │   └── ir-report.md           # Final Incident Response Report
│       ├── case-02/
│       │   ├── investigation-notes.md
│       │   └── ir-report.md
│       └── blueteamlabs/
│           ├── case-01/
│           │   └── ir-report.md
│           └── case-02/
│               └── ir-report.md
│
│
└── docs/                              ✅ PARTIALLY COMPLETE
    ├── Forensic-Virtual-Env-Setup.md  ✅
    ├── file-hashing-notes.md          ✅
    ├── metadata-extraction-notes.md   ✅
    ├── file-signature-analysis-notes.md ✅
    ├── log-analysis-notes.md          ✅
    ├── windows-event-logs-analysis-notes.md ✅
    ├── memory-forensics-notes.md      🔲
    ├── disk-forensics-notes.md        🔲
    ├── network-forensics-notes.md     🔲
    ├── windows-os-forensics-notes.md  🔲
    └── mobile-forensics-notes.md      🔲
```

---

## Case Investigation Naming Convention

All case investigation files follow the format `CF-YYYY-NNN.md` where:
- `CF` = Case File
- `YYYY` = Year
- `NNN` = Sequential case number (001, 002, 003...)

Each case file documents: objective, tools used, investigation steps, findings, IOCs, and conclusion.

---

## Tool vs. Industry Tool Distinction

| Folder | Type |
|---|---|
| 01 → 04 | Self-built Python tools |
| 05 | ExifTool (industry) |
| 07 | Volatility 3 (industry) |
| 08 | Chainsaw + Hayabusa (industry) |
| 09 | Autopsy + dd (industry) |
| 10 | Wireshark + tshark (industry) |
| 14 | Multi-tool IR simulations |
