# File Hashing Tool — Concepts & Notes

## Hashing vs Encryption

A common point of confusion when starting out in forensics is whether SHA-256 and AES-256 are interchangeable. They are not — they solve completely different problems.

### Hashing (SHA-256) — The One-Way Street

**Purpose:** To verify that data hasn't been tampered with.

**How it works:** It takes a file, runs it through a complex mathematical algorithm, and produces a unique fixed-length string called a hash — a digital fingerprint of the file's contents.

**The key property:** You cannot reverse the math. Given a SHA-256 hash, it is computationally impossible to reconstruct the original file from it. It is a one-way trip.

**Forensic use:** Before analysis begins, an investigator hashes the evidence file. After analysis, they hash it again. If both hashes match, it is mathematically proven that the file was not altered during the investigation. This is admissible in court.

> *"Here is the evidence, and here is its fingerprint. If you check the fingerprint again later and it matches, nobody altered the evidence."*

### Encryption (AES-256) — The Two-Way Street

**Purpose:** To hide data from unauthorized people.

**How it works:** It takes a file and scrambles it using a secret key (like a password). Anyone with the key can reverse the process and recover the original file.

**The key property:** It is reversible — if you have the key, you can decrypt.

**Forensic use:** Criminals frequently use AES-256 to lock their hard drives (e.g., via BitLocker or VeraCrypt) so investigators cannot access the contents. Breaking AES-256 encryption without the key is currently considered computationally infeasible.

### Which is "Better"?

Neither — they do completely different jobs and are used together in a real investigation:

| Use Case | Tool |
|---|---|
| Prove a file hasn't been tampered with | SHA-256 (Hashing) |
| Lock a file so nobody can read it | AES-256 (Encryption) |

In a real forensic workflow, you hash the evidence first (integrity), then encrypt the stored copy (confidentiality).

---

## Write Blockers

### What is a Write Blocker?

A write blocker is a safeguard that sits between an evidence drive and the investigator's computer. Its sole purpose is to intercept and block any **write** commands (save, delete, modify) while allowing all **read** commands (open, copy) to pass through normally. Without it, simply plugging a drive into a Windows machine causes Windows to write hidden files (like `Thumbs.db` or Recycle Bin entries), instantly altering the hash and tainting the evidence.

### Two Types

**Hardware Write Blockers:** A physical device you plug the suspect's drive into before connecting it to your computer. If the computer tries to write data to the drive, the hardware physically blocks the electrical signal. These are the gold standard in professional forensic labs.

**Software Write Blockers:** A program or OS-level setting that instructs the computer not to write to a specific drive.

---

### Implementing Software Write Blocking in Practice

#### Level 1 — Code Level (built into our script)

When we open a file using Python's `"rb"` (Read Binary) mode:

```python
with open(file_path, "rb") as f:
```

Python strictly enforces read-only access at the code level. If a bug in the script accidentally tried to write data to the file, Python would throw an error and refuse. This is the most basic layer of protection.

---

#### Level 2 — File Attribute Level (`attrib` command)

The `attrib +R` command sets the Read-Only attribute on a file:

```cmd
attrib +R evidence.txt
```

When this attribute is on, Windows tells all applications that the file is locked for writing. If you open `evidence.txt` in Notepad and try to save changes, Notepad will throw an error and refuse to overwrite the file.

**To remove it:**
```cmd
attrib -R evidence.txt
```

**Limitation:** This is a "polite flag." If an application runs with sufficient privileges, it can ask the user for permission to override the flag. Clicking "Yes" on the overwrite prompt removes the attribute and saves the file. It is not a hard security boundary.

---

#### Level 3 — ACL Level (`icacls` command) — The True Fix

Every file in Windows has an **Access Control List (ACL)** — a strict list defining exactly who can do what to the file. A **Deny** rule in the ACL is enforced at the Windows kernel level and cannot be bypassed by any application, regardless of privilege level.

**In PowerShell — deny write access to everyone:**
```powershell
icacls evidence.txt /deny "Everyone:(W)"
```

After this command, any attempt to save changes to `evidence.txt` — from VS Code, Notepad, or any other application — will result in a hard **Access Denied** error. Even clicking "Save as Admin" will fail.

**To remove the deny rule:**
```powershell
icacls evidence.txt /remove:d "Everyone"
```

> ⚠️ Note: When removing, do **not** include `:(W)` at the end — specify only the user/group name. Including the permission suffix causes the command to silently fail.

---

#### Level 4 — Registry Level (USB Drive Write Blocking)

When plugging a suspect's USB drive into a Windows machine for analysis, Windows automatically writes hidden files to it before you can stop it. To prevent this, forensic analysts enable system-wide USB write blocking via the Windows Registry before inserting the drive:

Navigate to:
```
HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\StorageDevicePolicies
```
Set `WriteProtect` to `1`.

This turns the entire Windows machine into a software write blocker for every USB drive plugged into it — simulating the behaviour of a hardware write blocker.

---

### Summary — Which Level to Use?

| Scenario | Recommended Level |
|---|---|
| Protecting a file during script analysis | Level 1 (rb mode) + Level 3 (icacls) |
| Quick protection during manual review | Level 2 (attrib) — acceptable for low-stakes work |
| Analyzing a suspect's USB drive | Level 4 (Registry) before inserting the drive |
| Professional lab investigation | Hardware write blocker (gold standard) |