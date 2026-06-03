# ExifTool — Setup Guide (Windows)

> **Tool:** ExifTool by Phil Harvey
> **Version Documented:** 13.59 (Released May 27, 2026)
> **Platform:** Windows 64-bit
> **Official Site:** https://exiftool.org

---

## What is ExifTool?

ExifTool is a free, open-source, platform-independent command-line tool for reading, writing, and editing metadata in a wide variety of file formats. It is the industry-standard metadata extraction tool used by digital forensics labs, law enforcement agencies, investigative journalists, and security researchers worldwide.

It supports metadata formats including EXIF, GPS, IPTC, XMP, JFIF, GeoTIFF, ICC Profile, Photoshop IRB, ID3, and many more — across hundreds of file types.

---

## Why ExifTool Over a Custom Script?

| Feature | Custom `metadata_extractor.py` | ExifTool |
|---|---|---|
| Supported formats | JPEG only (via Pillow) | 100+ file formats |
| Metadata tags extracted | ~10 basic EXIF tags | 10,000+ tags |
| GPS extraction | Basic | Full GPS track + altitude |
| Maker notes (camera internals) | No | Yes (Canon, Nikon, Sony, DJI, etc.) |
| Batch processing | Manual loop | Built-in `-r` recursive flag |
| CSV export | Manual | Built-in `-csv` flag |
| Court-admissible output | No | Yes (used in real investigations) |

---

## Download

Downloads now point to **SourceForge** (officially stated on exiftool.org to reduce server load — this is intentional and safe).

**Download link:** https://exiftool.org (Windows section)

Select the appropriate version:
- **64-bit systems (modern Windows):** `exiftool-13.59_64.zip` (11.2 MB)
- **32-bit systems (older hardware):** `exiftool-13.59_32.zip` (11.4 MB)

> ℹ️ The Windows executable bundles Perl internally. It does not require a separate Perl installation.

---

## Security Verification (Best Practice)

Before installing any forensic tool, verify it hasn't been tampered with:

**Step 1 — Check the official checksums:**
The official checksums for all distribution packages are listed at:
`https://exiftool.org` → *"Click here for the checksums of all distribution packages"*

**Step 2 — Antivirus scan:**
Run a full scan of the extracted folder using your AV software (e.g., Kaspersky, Windows Defender).

**Step 3 — VirusTotal verification:**
Upload `exiftool(-k).exe` to https://virustotal.com and verify no genuine threats are detected.

> ⚠️ Some antivirus engines may flag ExifTool as a false positive because it reads and writes file metadata. This is expected and not a genuine threat. A clean VirusTotal result from reputable engines (Kaspersky, Microsoft, Google) confirms the file is safe.

---

## Installation

**Step 1 — Extract the ZIP:**
Extract `exiftool-13.59_64.zip`. You will find two items inside:
```
exiftool(-k).exe
exiftool_files/        ← this folder is required
```

**Step 2 — Rename the executable:**
Rename `exiftool(-k).exe` → `exiftool.exe`

The `(-k)` suffix means the window pauses after output when double-clicked. Renaming removes this behaviour and enables proper command-line use.

**Step 3 — Move both items to `C:\Windows\`:**
Move **both** `exiftool.exe` **and** the `exiftool_files` folder to `C:\Windows\`.

```
C:\Windows\
├── exiftool.exe
└── exiftool_files\
```

> ⚠️ Critical: The `exiftool_files` folder must always be in the same directory as `exiftool.exe`. Moving the `.exe` without the folder will break the tool.

**Step 4 — Verify installation:**
Open CMD or PowerShell from any directory and run:
```
exiftool -ver
```
Expected output:
```
13.59
```

---

## Why `C:\Windows\`?

`C:\Windows\` is included in the Windows system `PATH` environment variable by default. Placing `exiftool.exe` there makes it accessible from **any directory** in CMD or PowerShell without specifying the full path to the executable.

This means you can run:
```
exiftool "D:\Evidence\photo.jpg"
```
from any terminal window, regardless of your current working directory.

---

## Uninstallation

To completely remove ExifTool:
1. Delete `C:\Windows\exiftool.exe`
2. Delete `C:\Windows\exiftool_files\`

No registry entries. No background services. No other footprint.

---

## Key Forensic Commands

```bash
# Full metadata dump on a single file
exiftool <filename>

# Extract only the most forensically critical tags
exiftool -Make -Model -DateTimeOriginal -GPSLatitude -GPSLongitude -Software <filename>

# Recursively scan an entire folder
exiftool -r <foldername>

# Export full metadata of all files in a folder to CSV (for documentation)
exiftool -csv <foldername> > results.csv
```

---

## Notes for Forensic Use

- ExifTool is **read-only by default**. Running `exiftool <file>` never modifies the file.
- Always run ExifTool on a **verified copy** of the evidence, not the original.
- Verify the SHA-256 hash of the evidence file before and after analysis to confirm it was not altered.
- ExifTool makes **no network calls**. It operates entirely offline — a hard requirement when working on air-gapped forensic investigation machines.
- The `-w` (write) flag enables metadata editing. Never use write flags during evidence analysis.

---

*Documented as part of the Digital Forensics learning repository.*