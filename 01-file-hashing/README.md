# 🔐 SHA-256 File Hasher (CLI) — Digital Forensics Tool

A forensics-grade command-line tool built in Python that calculates **MD5**, **SHA-1**, and **SHA-256** cryptographic hashes for any file. Designed from the ground up with evidence integrity as the top priority — the file is opened strictly in binary read-only mode, ensuring the tool itself can never accidentally alter the evidence it is analyzing.

Built from scratch as part of a Digital Forensics learning journey to deeply understand the mathematical foundation behind evidence preservation and chain of custody.

---

## 📌 Why File Hashing Matters in Digital Forensics

Before an investigator can analyze a single byte of evidence, they must first prove that the evidence has not been tampered with — not during transport, not during storage, and not during analysis. This is done through **cryptographic hashing**.

A hash is a unique digital fingerprint for a file:
- The same file will always produce the exact same hash, no matter when or where it is calculated.
- If even a **single character** inside a file is changed, the resulting hash changes completely and dramatically.
- This makes it mathematically impossible to secretly alter evidence without detection.

This tool establishes that fingerprint the moment evidence is seized, creating a baseline that can be verified at any point in the future to prove the evidence is still intact.

---

## 🛠️ Features

- ✅ Calculates **MD5**, **SHA-1**, and **SHA-256** hashes simultaneously in a single run
- ✅ Opens files strictly in **binary read-only mode** (`rb`) — the tool itself acts as a software write blocker
- ✅ Reads files in **4096-byte chunks** — safely handles massive files (hard drive images, videos, databases) without crashing
- ✅ Works on **any file type** — `.txt`, `.jpg`, `.mp4`, `.exe`, `.pdf`, `.dd`, `.E01`, and more
- ✅ Zero external dependencies — uses only Python's built-in `hashlib` library
- ✅ Works on any OS: Windows, macOS, Linux

---

## 🔒 The Software Write Blocker

In professional digital forensics, a **Write Blocker** is a device or mechanism that prevents any write commands from reaching the evidence drive. Without one, simply plugging a USB drive into a Windows laptop causes Windows to write hidden files to it (like `Thumbs.db`), instantly changing the hash and contaminating the evidence.

This tool implements **software-level write blocking** at the code level. Every file is opened using:

```python
with open(file_path, "rb") as f:
```

The `"rb"` flag stands for **Read Binary**. Python physically cannot write data to a file opened with this flag. Even if a bug existed in the code that attempted to write data, the OS would reject it. The evidence is safe.

---

## 📋 Prerequisites

- Python 3.7 or higher
- No external libraries required

---

## 🚀 Usage

Run the script from your terminal and pass the path to any file as an argument:

```bash
python file_hasher.py <path_to_file>
```

### Examples

**Hashing a text evidence file:**
```bash
python file_hasher.py evidence.txt
```

**Hashing an image:**
```bash
python file_hasher.py crime_scene_photo.jpg
```

**Hashing a large disk image:**
```bash
python file_hasher.py seized_drive.dd
```

---

## 📤 Sample Output

```
Calculating hashes for: evidence.txt
----------------------------------------
MD5:    d8e8fca2dc0f896fd7cb4cb0031ba249
SHA-1:  4e1243bd22c66e76c2ba9eddc1f91394e57f9f83
SHA-256:f924ddd79c36dd86837ada1f24f0d4312146c17607a5c682d6aa58ec2fd27e36
```

---

## 🔬 Forensic Concepts Covered

### The Three Hashing Algorithms

| Algorithm | Output Length | Status in Forensics | Use Case |
|---|---|---|---|
| **MD5** | 128-bit / 32 hex chars | Legacy — considered weak (collisions possible) | Still used for quick file identification |
| **SHA-1** | 160-bit / 40 hex chars | Deprecated — broken in 2017 | Historical case compatibility |
| **SHA-256** | 256-bit / 64 hex chars | ✅ Current industry gold standard | All modern forensic evidence logging |

> ⚠️ **Why calculate all three?** Older case files and legacy tools may have only logged an MD5 or SHA-1 hash. By generating all three simultaneously, this tool ensures compatibility with evidence logs from any era.

### Chain of Custody & Hash Verification
The hash serves as the cornerstone of the legal **Chain of Custody**:

1. **Seizure:** The investigator hashes the original evidence the moment the device is seized.
2. **Imaging:** A bit-for-bit copy (forensic image) is made. The copy is hashed and compared to the original — they must match.
3. **Analysis:** All analysis is done on the copy, never the original.
4. **Court:** At any point, the evidence can be re-hashed to prove it has not been altered since seizure.

If the hash does not match at any step, the **Chain of Custody is broken** and the evidence may be inadmissible in court.

### Chunked File Reading
```python
for byte_block in iter(lambda: f.read(4096), b""):
    md5_hash.update(byte_block)
    sha1_hash.update(byte_block)
    sha256_hash.update(byte_block)
```
Instead of loading the entire file into RAM at once (which would crash the program on a 500 GB disk image), the file is fed into the hasher in small 4096-byte chunks. The hasher continuously updates its internal state with each chunk until the entire file has been processed, then produces the final hash. This means a 1 TB disk image uses no more RAM than a 1 KB text file.

---

## 🔐 Securing Evidence Files (Recommended Workflow)

After hashing your evidence file, you should immediately lock it against accidental modification:

**Step 1 — Write Block at the OS level (Windows PowerShell):**
```powershell
icacls evidence.txt /deny "Everyone:(W)"
```
This adds a hard ACL Deny rule, meaning no application (Notepad, VS Code, Python scripts) can write to the file — even if run as Administrator.

**Step 2 — Encrypt the file (AES-256):**
Use VeraCrypt, BitLocker, or a Python AES-256 encryption library to lock the file inside an encrypted container, ensuring confidentiality during storage and transport.

To remove the write lock later when needed:
```powershell
icacls evidence.txt /remove:d "Everyone"
```

---

## ⚠️ Known Limitations

- **Single File Processing:** This version hashes one file at a time. Batch folder hashing is a planned future upgrade.
- **No Auto-Verification Loop:** The tool calculates hashes but does not yet automatically compare them against a previously stored baseline hash.
- **No Report Generation:** Output is printed to the terminal only. Automatic logging to a timestamped `.txt` evidence report is a planned upgrade.
- **No Hash Set Matching:** The tool does not yet compare hashes against known-bad (malware) or known-good (NSRL) hash databases.

---

## 🗺️ Roadmap (Planned Upgrades)

- [ ] Batch folder hashing — recursively hash every file in a directory and output a hash manifest
- [ ] Auto hash verification — re-hash a file and automatically compare it against a stored baseline
- [ ] Evidence report generation — save results to a timestamped, structured `.txt` log file
- [ ] Hash set matching — compare hashes against a local known-bad or NSRL database
- [ ] Support for raw disk image formats (`.dd`, `.E01`)

---

> **Disclaimer:** This tool is intended strictly for educational purposes and legitimate forensic investigations conducted with proper legal authorization. Unauthorized use against systems or files you do not own or have explicit permission to analyze is illegal.
