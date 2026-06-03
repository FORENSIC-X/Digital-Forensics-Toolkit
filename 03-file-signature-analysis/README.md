# File Signature Analyzer — CLI Script

A command-line forensic tool that detects the **true identity of any file** by reading its raw Magic Number bytes — regardless of what its extension claims to be.

---

## What is a Magic Number?

Every file format embeds a unique sequence of bytes at the very beginning of its raw binary data. This is called a **Magic Number** (or File Signature). It acts as the file's true identity card — independent of its name or extension.

A common attacker technique called **file masquerading** involves renaming a malicious executable (e.g. `malware.exe`) to something innocent-looking (e.g. `photo.jpg`) to bypass security checks. This tool exposes that deception instantly.

---

## How It Works

1. Opens the target file in **Read Binary (`rb`) mode** — treating every file as raw bytes regardless of type.
2. Reads only the **first 8 bytes** of the file — fast enough to work on files of any size including 1TB+ disk images.
3. Matches those bytes against a dictionary of **25+ known Magic Number signatures**.
4. Compares the detected true type against the file's declared extension.
5. Raises a **FORENSIC ALERT** if they don't match.

---

## Supported Signatures (25+)

| Category | File Types |
|---|---|
| Images | JPEG, PNG, GIF, BMP, TIFF, WebP |
| Documents | PDF, DOC/XLS/PPT (Legacy), DOCX/XLSX/PPTX/APK (Modern) |
| Executables | Windows EXE/DLL, Linux ELF, Java Class |
| Archives | ZIP, RAR, GZIP, XZ, 7-Zip |
| Audio/Video | MP3, MP4/MOV, MKV/WebM, AVI/WAV |
| Databases | SQLite, EWF Forensic Image, VMware VMDK |
| Scripts | Python/Bash (Shebang) |

---

## Usage

```bash
python file_signature_analyzer.py <path_to_file>
```

**Examples:**

```bash
# Analyze a file by name (if in same directory)
python file_signature_analyzer.py evidence.jpg

# Analyze a file by full path
python file_signature_analyzer.py "D:\Evidence\suspicious_file.txt"
```

---

## Sample Output

**When the signature matches the extension:**
```
----------------------------------------
Analyzing file:  photo.jpg
----------------------------------------
It is a :  JPEG Image

FILE SIGNATURE MATCHES WITH ITS EXTENSION !
```

**When a masquerading attempt is detected:**
```
----------------------------------------
Analyzing file:  photo.jpg
----------------------------------------
It is a :  Windows Executable / DLL

FORENSIC ALERT ! FILE SIGNATURE DOES NOT MATCH WITH ITS EXTENSION !
```

**When the signature is unknown:**
```
----------------------------------------
Analyzing file:  unknown.bin
----------------------------------------
FILE SIGNATURE DOESN'T MATCH WITH ANY KNOWN SIGNATURE IN OUR DICTIONARY!
```

---

## Requirements

- Python 3.x
- No external libraries required — uses only Python's built-in `os` and `sys` modules.

---

## Security Note

This script opens files exclusively in **Read Binary (`rb`) mode**. It reads exactly 8 bytes into memory, performs a dictionary comparison, and discards everything. The file is never saved, executed, or interpreted — making it completely safe to run against suspicious or potentially malicious files.

---
> **Disclaimer:** This tool is intended strictly for educational purposes and legitimate forensic investigations conducted with proper legal authorization. Unauthorized use against systems or files you do not own or have explicit permission to analyze is illegal.
