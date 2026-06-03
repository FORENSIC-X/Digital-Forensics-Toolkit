# File Signature Analyzer Tool — Concepts & Notes

## The Core Concept — Magic Numbers

Every file format in the world has a secret identity card hidden inside its first few bytes of raw data. This is called a **Magic Number** (also known as a File Signature).

When a file is created, the program that creates it writes a specific sequence of hexadecimal bytes at the very beginning of the file — before any actual content. Think of it as a stamp that says "I am a PDF" or "I am an EXE", regardless of what name or extension someone gives the file.

### Famous Magic Numbers

| File Type | Magic Bytes (Hex) | Human Readable |
|---|---|---|
| JPEG Image | `FF D8 FF` | ÿØÿ |
| PNG Image | `89 50 4E 47` | .PNG |
| PDF Document | `25 50 44 46` | %PDF |
| ZIP Archive | `50 4B 03 04` | PK.. |
| Windows EXE | `4D 5A` | MZ |
| MP4 Video | `66 74 79 70` | ftyp |

The key insight: **the file extension is just a label**. The Magic Number is the truth.

---

## Why This Matters in Forensics — File Masquerading

A common attacker technique is **file masquerading** — renaming `malware.exe` to `cute_cat.jpg` and emailing it to a victim. The operating system sees `.jpg` and treats it as an image. The email gateway may not flag it. But the Magic Number at the start of the file still reads `4D 5A` — the unmistakable signature of a Windows Executable.

This script exposes that lie instantly, before the file is ever executed.

---

## Why Use This When Kaspersky Exists?

This is a fair question. Here is the precise distinction:

### What Kaspersky Does

Kaspersky scans a file and compares it against a **database of known malware signatures**. It asks: *"Have I seen this specific threat before?"*

- Uses Magic Numbers internally, but only as one small step in a much larger pipeline
- Requires constant internet-connected updates to stay relevant
- Is a black box — you get a result with no visibility into the detection mechanism
- **Can be fooled by zero-day malware** — brand new malware not yet in any database will pass a Kaspersky scan as "Clean"

### What Our Script Does

Our script asks a completely different question: *"Is this file lying about what it is?"*

- Works 100% offline — no updates, no database, no internet connection needed
- Fully transparent — the detection mechanism is readable line by line
- **Catches file masquerading even if the malware is brand new and completely unknown to any AV**
- Produces forensic-grade, documentable evidence: *"The file extension was `.jpg` but the first two bytes `4D 5A` confirm this is a Windows Executable"*

### The Real-World Scenario

A hacker sends a file named `invoice.pdf`. Kaspersky scans it and returns **Clean** — because this is a never-before-seen piece of malware with no known signature in any database yet.

Our script reads the first 2 bytes, sees `4D 5A`, and immediately flags:

```
FORENSIC ALERT! FILE SIGNATURE DOES NOT MATCH WITH ITS EXTENSION!
Detected type : Windows Executable / DLL
Actual extension : .pdf
```

This is the gap between signature-based detection and structural analysis. Both are necessary — they catch different things.

---

## How to Test the Script

**Test 1 — Normal match (expected clean result):**
Run the script on any `.jpg` image with its original name. Expected output:
```
FILE SIGNATURE MATCHES WITH ITS EXTENSION!
```

**Test 2 — Forensic Alert trigger (masquerading simulation):**
Rename that same `.jpg` file to `suspicious_file.txt` and run the script on it. Expected output:
```
FORENSIC ALERT! FILE SIGNATURE DOES NOT MATCH WITH ITS EXTENSION!
```

This simulates exactly what an investigator would do when they encounter a suspiciously named file on a seized device.