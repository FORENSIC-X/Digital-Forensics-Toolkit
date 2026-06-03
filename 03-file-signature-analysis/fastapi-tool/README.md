# File Signature Analyzer — Full Tool

A full-stack forensic web application that detects the **true identity of any file** via Magic Number analysis. Built with a **FastAPI Python backend** and a **browser-based frontend** 

---

## What is a Magic Number?

Every file format embeds a unique sequence of bytes at the very beginning of its raw binary data. This is called a **Magic Number** (or File Signature). It acts as the file's true identity card — independent of its name or extension.

A common attacker technique called **file masquerading** involves renaming a malicious executable (e.g. `malware.exe`) to something innocent-looking (e.g. `photo.jpg`). This tool exposes that deception instantly by reading what the file actually *is* at the binary level.

---

## Architecture

```
Browser (index.html + script.js + styles.css)
        │
        │  POST /analyze_file/  (FormData)
        ▼
FastAPI Backend (file_signature_analyzer.py)
        │
        │  Reads first 8 bytes → matches Magic Number → returns JSON verdict
        ▼
Browser displays result: VERIFIED / FORENSIC ALERT / UNKNOWN
```

The uploaded file is **never saved to disk**. The backend reads exactly 8 bytes into memory, performs the analysis, and discards everything. The file never leaves your machine.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| File Handling | FastAPI `UploadFile`, `python-multipart` |
| Cross-Origin | FastAPI `CORSMiddleware` |

---

## How It Works

1. User drops or selects a file in the browser UI.
2. JavaScript packages it as `FormData` and sends a `POST` request to `http://localhost:8000/analyze_file/`.
3. FastAPI receives the file as an `UploadFile` object and reads the first **8 bytes** asynchronously (`await file.read(8)`).
4. The 8-byte header is matched against a dictionary of **25+ known Magic Number signatures**.
5. The detected true type is compared against the file's declared extension.
6. A JSON response is returned with the verdict, which the frontend renders as one of three states — **Verified**, **Forensic Alert**, or **Unknown**.

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

## Setup & Usage

### 1. Install dependencies

```bash
pip install fastapi uvicorn python-multipart
```

### 2. Start the FastAPI backend

```bash
uvicorn file_signature_analyzer:app --reload
```

The server starts at `http://127.0.0.1:8000`.

### 3. Open the frontend

Open `index.html` directly in your browser. Drop any file into the upload zone and click **Analyze Signature**.

---

## API Endpoint

### `POST /analyze_file/`

**Request:** `multipart/form-data` with a `file` field.

**Response (match):**
```json
{
  "file_name"  : "photo.jpg",
  "true_type"  : "JPEG Image",
  "extension"  : ".jpg",
  "match"      : true,
  "message"    : "FILE SIGNATURE MATCHES WITH ITS EXTENSION !"
}
```

**Response (alert):**
```json
{
  "file_name"  : "photo.jpg",
  "true_type"  : "Windows Executable / DLL",
  "extension"  : ".jpg",
  "match"      : false,
  "message"    : "FILE SIGNATURE DOES NOT MATCH WITH ITS EXTENSION !"
}
```

**Response (unknown):**
```json
{
  "message": "FILE SIGNATURE DOESN'T MATCH WITH ANY KNOWN SIGNATURE IN OUR DICTIONARY!"
}
```

---

## Security Note

This tool is designed for **local forensic use only**. The backend reads exactly 8 bytes into memory and discards the rest — the file is never saved, executed, or interpreted. For analyzing genuinely malicious files, it is best practice to run this tool inside an **isolated Virtual Machine (VM)** with a clean snapshot ready for restoration after each investigation.

---

> **Disclaimer:** This tool is intended strictly for educational purposes and legitimate forensic investigations conducted with proper legal authorization. Unauthorized use against systems or files you do not own or have explicit permission to analyze is illegal.
