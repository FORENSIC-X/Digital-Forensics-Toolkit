# 🌐 SHA-256 File Hasher (Web) — Digital Forensics Tool

A fully client-side, browser-based SHA-256 file hashing tool built with pure HTML, CSS, and JavaScript. Designed for digital forensics use cases where evidence integrity must be verified quickly, securely, and without the risk of the file ever leaving the user's machine.

No backend. No server. No file uploads. The hash is computed entirely inside the user's web browser using the **Web Crypto API** — a cryptographic engine built directly into all modern browsers.

Built from scratch as part of a Digital Forensics learning journey to understand both the forensic importance of cryptographic hashing and the modern browser APIs that make client-side security possible.

---

## 📌 Why a Browser-Based Hasher?

### The Problem with Traditional Web Upload Tools
Most online file hashing tools work by uploading your file to a remote server, computing the hash there, and sending the result back. This approach has two major problems:

1. **Privacy Risk:** Your evidence file — which may contain sensitive personal, medical, legal, or criminal data — is transmitted over the internet to a server you do not control.
2. **Chain of Custody Risk:** The moment a file leaves your machine and travels over a network, you can no longer guarantee it was not intercepted or modified in transit.

### The Solution: Web Crypto API
This tool eliminates both risks entirely. When you drop a file into the browser:
- The browser reads the raw bytes of the file directly into its local memory (RAM)
- The Web Crypto API computes the SHA-256 hash entirely within the browser process
- The hash result is displayed on screen
- **The file never leaves your machine. Not even one byte.**

---

## 🛠️ Features

- ✅ **100% Client-Side** — files are never uploaded to any server
- ✅ **SHA-256 Hashing** via the native browser **Web Crypto API** (`crypto.subtle.digest`)
- ✅ **Drag & Drop** interface for fast, intuitive file selection
- ✅ **Click to Browse** file picker as an alternative to drag & drop
- ✅ Works on **any file type** — images, videos, documents, executables, disk images, and more
- ✅ **Zero dependencies** — no npm, no frameworks, no external libraries
- ✅ **Glassmorphic dark-mode UI** — clean, premium design with animated background and smooth hover effects
- ✅ Works entirely offline — once the page is loaded, no internet connection is required
- ✅ **Chunked hashing via hash-wasm (WebAssembly)** — process files in 64 MB chunks using a streaming WASM hasher so files of any size (1 TB+) can be hashed without RAM constraints. When dealing with 1000 GB files, the bottleneck is usually the Read Speed of the hard drive (SSD vs HDD). Using a WebAssembly (WASM) library like hash-wasm, as we've done here, ensures that the CPU can keep up with the data coming off the disk without the browser tab ever becoming unresponsive. 

---

## 📋 Prerequisites

- Any modern web browser (Chrome, Firefox, Edge, Safari)
- No installation required
- No Python, Node.js, or any runtime needed

---

## 🚀 Usage

**Option 1 — Open Directly:**
Simply download the repository and double-click `index.html` to open it in your browser. No web server required.

**Option 2 — Clone & Open:**
```bash
git clone https://github.com/<your-username>/file-hasher-web.git
cd file-hasher-web
# Then double-click index.html, or open it via your browser
```

Once open:
1. **Drag and drop** any file onto the dashed upload area, or click **Select File** to browse
2. The SHA-256 hash is calculated instantly and displayed on screen
3. Copy the hash and store it in your evidence log

---

## 📤 Sample Output

After uploading `evidence.txt`, the tool displays:

```
SHA-256 HASH
f924ddd79c36dd86837ada1f24f0d4312146c17607a5c682d6aa58ec2fd27e36
```

---

## 🔬 How It Works — Under the Hood

The entire hashing pipeline is three steps handled by the browser's built-in JavaScript engine:

### Step 1 — Read the file as raw bytes
```javascript
const arrayBuffer = await file.arrayBuffer();
```
The `File` object the browser gives us when a user drops a file is a direct reference to the file on the user's hard drive. Calling `.arrayBuffer()` reads the raw bytes of the entire file directly into the browser's local RAM. This happens locally — no network request is made.

### Step 2 — Hash the raw bytes using Web Crypto API
```javascript
const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
```
`crypto.subtle` is the browser's built-in cryptographic engine. It is implemented in native compiled code (not JavaScript), making it extremely fast and cryptographically secure. We pass it the `'SHA-256'` algorithm and the raw bytes from Step 1.

### Step 3 — Convert the result to a hex string
```javascript
const hashArray = Array.from(new Uint8Array(hashBuffer));
const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
```
The Web Crypto API returns the hash as a raw binary `ArrayBuffer`. This step converts it into the standard hexadecimal string format (like `f924ddd7...`) that forensic tools and hash logs use.

---

## 🔑 Key Security Concept: The File Object vs. The File Path

A critical distinction to understand about how this tool works:

When a user drops a file into the browser, JavaScript receives a **`File` object** — not a file path string. For security reasons, modern browsers intentionally hide the true file path from JavaScript entirely. Even if you tried to access it, the browser would return a fake string like `C:\fakepath\evidence.txt`.

More importantly, the `File` object is a direct bridge to the **raw binary contents** of the file. When we call `.arrayBuffer()`, we are not hashing the file's name or its path. We are hashing every single 1 and 0 inside the file itself. This means:

- Two files named completely differently but with identical contents will produce the **same hash**
- Two files with the same name but even one character of difference will produce a completely **different hash**

This is exactly the behavior required for forensic integrity verification.

---

## 🎨 UI Design

The interface is built with a premium dark-mode aesthetic using:
- **Glassmorphism** — a frosted glass card effect using `backdrop-filter: blur()` and semi-transparent backgrounds
- **Animated background orbs** — two large, blurred, floating color orbs that create a dynamic, premium feel using CSS `@keyframes`
- **Smooth micro-animations** — the upload card lifts on hover, the upload icon floats upward, and the button glows on interaction
- **Google Fonts (Outfit)** — a modern, clean typeface instead of a browser default
- **Phosphor Icons** — a lightweight, consistent icon set for the UI elements

---

## ⚠️ Known Limitations

- **SHA-256 Only:** The current version calculates SHA-256 only. MD5 and SHA-1 support is a planned upgrade. *(Note: The Web Crypto API supports MD5 only through third-party WASM libraries, as MD5 is considered cryptographically broken and was intentionally excluded from the Web Crypto API specification.)*
- **Single File Only:** The current version hashes one file at a time. Batch folder hashing is a planned upgrade.
- **No Report Generation:** Results are displayed on screen only. Auto-generating a downloadable evidence report is a planned upgrade.
---

## 🗺️ Roadmap (Planned Upgrades)

- [ ] **MD5 and SHA-1 support** — add legacy algorithm support via hash-wasm for compatibility with older evidence logs
- [ ] **Downloadable evidence report** — generate a `.txt` file containing the filename, file size, hash, and timestamp that the user can save as an official evidence log
- [ ] **Hash comparison tool** — let the user paste a previously recorded hash to instantly verify if the file has been modified
- [ ] **Batch folder hashing** — hash multiple files in one session and export a full hash manifest
---

> **Disclaimer:** This tool is intended strictly for educational purposes and legitimate forensic investigations conducted with proper legal authorization. Unauthorized use against systems or files you do not own or have explicit permission to analyze is illegal.
