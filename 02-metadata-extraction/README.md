# 🔍 Metadata Extractor — Digital Forensics Tool

A lightweight, forensics-grade Python tool for extracting hidden metadata from files. Built from scratch as part of a Digital Forensics learning journey, this tool uncovers two critical layers of evidence that are invisible to the naked eye:

1. **MAC Timestamps** — OS-level forensic timestamps (Modified, Accessed, Created) that establish a file's timeline of activity.
2. **EXIF Data** — Hidden camera and device metadata embedded inside image files, including GPS coordinates, device model, software used, and capture time.

---

## 📌 Why Metadata Matters in Digital Forensics

When a file is found during an investigation, its contents are only half the story. The **metadata** — the hidden data *about* the file — can answer the most critical forensic questions:

- **When** was this file last modified? *(MAC Timestamps)*
- **Where** was this photo taken? *(EXIF GPS Data)*
- **What device** took this photo? *(EXIF Camera Model)*
- **Was this image edited** after it was originally captured? *(EXIF Software Tag)*
- **Has someone tampered** with the timestamps to cover their tracks? *(Timestamp Cross-referencing)*

This tool automates the extraction of both layers so investigators don't have to inspect raw hexadecimal data manually.

---

## 🛠️ Features

- ✅ Extracts **MAC Timestamps** (Modified, Accessed, Created) from any file type
- ✅ Extracts **full EXIF metadata** from JPEG/PNG image files
- ✅ Human-readable tag names (e.g., `Make`, `Model`, `GPSInfo`) instead of raw numeric IDs
- ✅ Gracefully handles non-image files (skips EXIF extraction without crashing)
- ✅ Works on any OS: Windows, macOS, Linux
- ✅ Zero external dependencies for MAC extraction (uses Python's built-in `os` module)

---

## 📋 Prerequisites

- Python 3.7 or higher
- [Pillow](https://python-pillow.org/) library for EXIF extraction

Install Pillow using pip:
```bash
pip install Pillow
```

---

## 🚀 Usage

Run the script from your terminal and pass the path to any file as an argument:

```bash
python metadata_extractor.py <path_to_file>
```

### Examples

**Analyzing a text or document file (MAC Timestamps only):**
```bash
python metadata_extractor.py evidence.txt
```

**Analyzing an image file (MAC Timestamps + full EXIF data):**
```bash
python metadata_extractor.py crime_scene_photo.jpg
```

---

## 📤 Sample Output

### Text File (MAC Timestamps Only)
```
--- Basic OS Metadata for: evidence.txt ---
Size: 512 bytes
Created (C):  2024-11-15 10:32:45
Modified (M): 2024-11-17 14:20:11
Accessed (A): 2024-11-18 09:05:33

[Note: File is not a supported image. Skipping EXIF extraction.]
```

### Image File (MAC Timestamps + EXIF Data)
```
--- Basic OS Metadata for: crime_scene_photo.jpg ---
Size: 3,847,291 bytes
Created (C):  2024-11-15 08:14:22
Modified (M): 2024-11-15 08:14:22
Accessed (A): 2024-11-18 09:05:33

--- Hidden Image EXIF Metadata ---
Make                     : Apple
Model                    : iPhone 14 Pro
Software                 : 17.1.1
DateTime                 : 2024:11:15 08:14:22
ExposureTime             : 1/120
FNumber                  : 1.78
GPSInfo                  : {1: 'N', 2: ((28, 1), (36, 1), (5423, 100)), ...}
```

---

## 🔬 Forensic Concepts Covered

### MAC Timestamps
Every file on a system has three hidden OS-level timestamps:

| Timestamp | Meaning | Forensic Significance |
|---|---|---|
| **M** — Modified | When the file's **content** was last changed | Core indicator of tampering |
| **A** — Accessed | When the file was last **opened or read** | Proves a user interacted with the file |
| **C** — Created | When the file was **born** on this specific machine | Helps establish timeline of file arrival |

> ⚠️ **Timestomping Warning:** Sophisticated attackers use tools to manually alter MAC timestamps to cover their tracks. Cross-referencing the OS-level MAC timestamps with the EXIF-embedded `DateTime` tag (which is much harder to fake) can expose this technique.

### EXIF Data
EXIF (Exchangeable Image File Format) is metadata that smartphones and digital cameras secretly embed into every photo at the moment of capture. It is a forensic goldmine when the image is transferred via original file (USB cable, email attachment, cloud backup) rather than social media (which strips EXIF data for privacy).

| EXIF Tag | What It Reveals |
|---|---|
| `Make` / `Model` | The exact device that took the photo |
| `DateTime` | The exact date and time the shutter was pressed |
| `GPSInfo` | The precise latitude/longitude coordinates |
| `Software` | If/how the image was edited after capture |
| `ExifVersion` | The age of the device or software standard |

---

## ⚠️ Known Limitations

- **Social Media Images:** Photos downloaded from WhatsApp, Instagram, Facebook, or Twitter will likely return `No EXIF metadata found`. These platforms automatically strip EXIF data before publishing to protect user privacy.
- **Screenshots & AI-Generated Images:** These are created by software, not a physical camera, so they contain no EXIF data.
- **Single File Processing:** This version processes one file at a time. Batch folder processing is a planned future upgrade.
- **File Format Support:** EXIF extraction currently supports JPEG and PNG formats via Pillow. Support for PDFs, Word documents, and video files is planned.

---

## 🗺️ Roadmap (Planned Upgrades)

- [ ] Batch folder processing — hash and extract metadata for all files in a directory
- [ ] GPS coordinate parser — convert raw EXIF GPS fractions to a Google Maps link
- [ ] Timestamp tampering detector — cross-reference EXIF DateTime vs. OS MAC timestamps
- [ ] Support for PDF and Word document metadata extraction
- [ ] Auto-generate a timestamped forensic evidence report as a `.txt` file

---
---

> **Disclaimer:** This tool is intended strictly for educational purposes and legitimate forensic investigations conducted with proper legal authorization. Unauthorized use against systems or files you do not own or have explicit permission to analyze is illegal.
