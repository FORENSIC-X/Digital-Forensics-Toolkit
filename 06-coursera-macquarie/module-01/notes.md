# Module 01 — Notes
## Introduction to Digital Forensics Processes

**Course:** Cybersecurity: Digital Forensics — Macquarie University (Coursera)
**Module:** 01 — Introduction to Digital Forensics Processes

---

## 1. What is Digital Forensics?

Digital forensics involves obtaining and analysing digital information for use as evidence in civil, criminal, or administrative cases.

More precisely — it is the application of computer science and investigative procedures for a legal purpose, involving:

- Analysis of digital evidence (information of probative value stored or transmitted in binary form)
- Proper search authority
- Chain of custody documentation
- Validation with mathematics (hash functions)
- Use of validated tools
- Repeatability and reproducibility
- Reporting
- Possible expert testimony

---

## 2. The Digital Forensics Process

### The Eight Steps

| Step | Description |
|---|---|
| **Obtain Search Authority** | Legal authority is required before any search or seizure of digital evidence |
| **Document Chain of Custody** | Chronological documentation of all evidence handling to prevent allegations of tampering |
| **Image and Hash** | Acquired data must be duplicated and hashed to ensure integrity — work is always done on the copy, never the original |
| **Validate Tools** | Forensic tools must be validated for reliability and correctness before use |
| **Analyse** | Apply investigative and analytical techniques to examine the evidence |
| **Repeat and Reproduce** | Results must be repeatable and reproducible by the same or other analysts — quality assurance |
| **Report** | Document all procedures and conclusions for use by others |
| **Present Expert Testimony** | In some cases, the analyst presents findings to a court or other audience |

> **Note:** These steps may differ depending on the nature of the investigation — civil vs criminal cases hold evidence to different standards and have very different consequences.

---

## 3. Types of Digital Forensics Investigations

Digital forensics investigations are categorised two ways:
- **Scope of the investigation**
- **Laws applied to the actors under test**

### Criminal Investigations

- Governed by criminal law
- Deal with offenses against the state or an enterprise — burglary, murder, fraud, cyberstalking, harassment
- Can result in imprisonment
- Evidence standard is **high** — strict procedural compliance required

Key questions an investigator asks:
- What tool was used to commit the crime?
- Was it a simple trespass, theft, or vandalism?
- Did the perpetrator infringe on someone's rights (cyberstalking, email harassment)?

### Civil Investigations

- Involve violations of contracts and lawsuits between parties
- Loser typically pays compensation, property, or services — no imprisonment
- Evidence standard is **lower** than criminal cases
- Less strict procedural requirements but documentation still essential

---

## 4. Conducting a Digital Forensics Investigation

### Investigation Plan — Required Resources

| Resource | Purpose |
|---|---|
| Evidence custody form | Documents chain of custody from point of collection |
| Original storage media + container | Physical evidence preservation |
| Bit-stream imaging tool (e.g. FTK Imager Lite) | Creates forensic image of the original media |
| Forensic workstation | Used to copy and examine evidence |
| Secure evidence locker / cabinet / safe | Physical security of evidence |

### Step-by-Step Investigation Workflow

```
Step 1 — Meet the IT manager, conduct interview, collect storage media
Step 2 — Fill out evidence custody form, get IT manager's signature, sign it yourself
Step 3 — Store media in evidence bag, transport to forensic facility
Step 4 — Transfer evidence to secure container (locker, cabinet, or safe)
Step 5 — Complete evidence custody form — store with evidence, limit access to reduce tampering risk
Step 6 — Lock the secure container
```

---

## 5. Analysing Digital Evidence

### Key Principle — File Deletion Does Not Mean Data is Gone

When a file is deleted on a disk, the actual file content is not necessarily removed from the physical location. The file system simply marks that space as available. The original content can often still be recovered and analysed using forensic tools.

Forensic tools typically create segments of large acquisition files for efficient storage and analysis.

---

## 6. NIST Guidelines for Digital Evidence Acquisition

NIST's Computer Forensics Tools Testing (CFTT) guidelines define subfunctions for the acquisition step:

| Subfunction | Description |
|---|---|
| **Physical Data Copy** | Copying the entire drive — bit for bit |
| **Logical Data Copy** | Copy of a specific disk partition only |
| **Data Acquisition Format** | Raw data to vendor-specific proprietary formats — for cross-platform analysis |
| **CLI and GUI Acquisition** | Command-line and graphical interfaces for efficiency and usability |
| **Remote, Live, and Memory Access** | Physical and remote acquisition using tools like AccessData and EnCase with `dd` command |

---

## 7. Autopsy — Practical Walkthrough

**Tool:** Autopsy 4.17.0 (open-source digital forensics platform)
**Evidence file used:** `Topic_1_2_1.dd` (forensic disk image)

### Case Setup in Autopsy

1. Launch Autopsy → Create New Case
2. Case Name: `Topic_1_2_1` → Select work folder as Base Directory → Single-user Case Type
3. Additional Information: Case Number `Topic_1_2_1`, Examiner name → Finish
4. Add Data Source → Select `Disk Image or VM file` → Browse to `Topic_1_2_1.dd` → Open → Next
5. Keep default Ingest Module settings → Next → Finish

### Navigating Evidence in Autopsy

**Tree Viewer (left pane):** Hierarchical view of the evidence
- `Views → File Types → By Extension → Documents → Office` — shows recovered Office files
- `Views → File Types → By Extension → Documents → Plain Text` — shows recovered text files
- `Deleted Files` — shows files marked as deleted but recoverable
- `Results → Extracted Content → Metadata` — shows metadata artifacts extracted during ingest

**Result Viewer (upper right pane):** Lists files within the selected category

**Content Viewer (lower right pane):** Displays file content — tabs include Hex, Text, Application, File Metadata

### Files Recovered in This Exercise

| File | Status | Notes |
|---|---|---|
| `Billing Letter.doc` | Allocated | Modified: 2005-12-09 |
| `Income.xls` | Allocated | Modified: 2005-12-09 |
| `Regrets.doc` | Unallocated | Deleted but recovered |
| `f0000000_13_October_2003.doc` | Unallocated | Carved file — recovered from unallocated space |
| `f0000049_02_November_2003.doc` | Unallocated | Carved file — recovered from unallocated space |

> **Allocated vs Unallocated:** Allocated files are actively tracked by the file system. Unallocated files have been deleted — the file system no longer tracks them but the data remains on disk until overwritten.

> **Carved Files (f0000000, f0000049):** Files with no filename — recovered by Autopsy by scanning raw disk sectors for known file signatures (Magic Numbers). The `f` prefix and byte offset in the name indicate where on the disk the file was found.

### Tagging Evidence in Autopsy

Autopsy allows investigators to tag files for case organization:

- **Right-click file → Tag File → Tag and Comment** — tag individual files
- **Ctrl+click multiple files → Right-click → Tag File → Quick Tag** — batch tag multiple files

Pre-existing tag categories include: `Bookmark`, `Follow Up`, `Notable Item`, `Non-pertinent`

Custom tags can be created — in this exercise: `Recovered Office File` was created as a custom tag and applied to all recovered Office documents.

### Keyword Search in Autopsy

Autopsy's keyword search scans all indexed content for character strings or hexadecimal values.

**Search performed:** `George` (Exact Match)
**Results:** 9 files containing the name George — including `letter1.txt`, recovered `.doc` files, `Income.xls`, `Client Info.mdb`, and unallocated space fragments

**Key find:** `letter1.txt` contained:

```
Earl,
We need to meet on the 18th of August to confirm the work
I am doing for you. Please contact me ASAP.

George
```

This establishes a communication between George and a person named Earl — relevant to the investigation.

**Email address search** was also performed using the built-in Email Addresses keyword list — surfacing all email addresses found across the entire disk image.

---

## 8. Reporting

The final report answers the investigative questions raised by the case:

1. How did the actor acquire the disk?
2. Did the actor perform work on his own laptop — and if so, during personal time or work hours?
3. At what times of day was the actor using non-work-related files — and how was this determined?
4. Which company policies apply?
5. Are there any other items to consider?

Reporting consolidates all analysis findings into a structured document suitable for legal or administrative proceedings.

---

## 9. Key Concepts — Quick Reference

| Concept | Definition |
|---|---|
| **Digital Evidence** | Information of probative value stored or transmitted in binary form |
| **Chain of Custody** | Chronological documentation of who handled evidence, when, and how |
| **Bit-stream Image** | Exact bit-for-bit copy of a storage device including deleted and unallocated space |
| **Hash Function** | Mathematical algorithm that produces a unique fingerprint of a file — used to verify integrity |
| **Allocated Space** | Disk space actively tracked and used by the file system |
| **Unallocated Space** | Disk space marked as available — may contain deleted file remnants |
| **File Carving** | Recovering files from unallocated space using file signature (Magic Number) detection |
| **Keyword Search** | Scanning indexed disk content for specific character strings or hex values |
| **Ingest Modules** | Autopsy plugins that automatically extract and analyse specific artifact types during data source processing |

---

## 10. Summary

Module 01 covered the complete digital forensics process from legal authority through to reporting, the distinction between criminal and civil investigations, the practical workflow for evidence acquisition and handling, NIST guidelines for acquisition, and hands-on use of Autopsy for disk image analysis including file recovery, tagging, and keyword search.

**Core principle that runs through everything:**
> *Never work on original evidence. Always image it, hash it, and work on the verified copy.*