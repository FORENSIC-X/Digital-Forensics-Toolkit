# Memory (RAM) Forensics — Theory Notes

> Part of the Digital Forensics Toolkit — Theory documentation for Memory Forensics, covering RAM volatility, memory dump acquisition, Volatility 3 plugins, and the investigation methodology.

---

## What is RAM and Why Does It Matter in Forensics?

When a computer is running, RAM (Random Access Memory) holds everything that is *alive* at that moment — every running process, every active network connection, every decrypted file, every command the user typed. Unlike a hard drive, RAM is **volatile** — the moment the computer is powered off, everything in it is permanently gone.

This makes RAM one of the most valuable and time-sensitive sources of forensic evidence. Things that exist **only in RAM** and nowhere on disk include:

- Running processes — including malware that injected itself into legitimate system processes
- Active network connections — the attacker's C2 server IP, even if the malware deleted its own files
- Decrypted data — malware that is encrypted on disk runs fully decrypted in RAM
- Command history — every command the attacker typed in `cmd.exe` or PowerShell
- Fileless malware — malware that lives entirely in memory and never writes to disk
- Registry hives loaded into memory
- Credentials — NTLM password hashes, and sometimes plaintext passwords

**The first rule of memory forensics:** capture RAM *before* shutting the machine down. Shutdown destroys the evidence.

---

## What is a Memory Dump?

A **memory dump** (also called a memory image) is a byte-for-byte snapshot of a machine's RAM captured at a specific moment in time — frozen and saved to a file.

Common memory dump file extensions:

| Extension | Context |
|---|---|
| `.raw` | Most common — raw binary dump |
| `.mem` | Used by some acquisition tools |
| `.vmem` | VMware virtual machine memory file |
| `.dmp` | Windows crash dump format |

A memory dump from a machine with 8GB RAM produces an ~8GB file. A 16GB machine produces ~16GB. The dump size equals the amount of RAM installed.

---

## Live Memory Capture Tools

In a real investigation the machine is *running* and potentially compromised. RAM must be captured before shutdown. Tools used for live acquisition:

| Tool | Platform | Notes |
|---|---|---|
| **WinPmem** | Windows | Open source, most common for Windows |
| **DumpIt** | Windows | Single executable, very fast |
| **LiME** (Linux Memory Extractor) | Linux | Loadable kernel module, captures to file or network |
| **OSXPmem** | macOS | macOS memory acquisition |

After capture, the dump is immediately hashed with SHA-256 to establish chain of custody — any later modification would change the hash.

---

## Volatility 3 — The Industry Standard

**Volatility 3** is the open source memory forensics framework used by professional DFIR analysts worldwide. It works by running **plugins** against a memory dump file — each plugin extracts one specific category of forensic artifacts.

Volatility never modifies the dump file. It is purely a read-only analysis tool.

Basic syntax:
```bash
python3 vol.py -f /path/to/memory.raw <plugin>
```

---

## Core Volatility 3 Plugins

### Process Analysis

| Plugin | Question it answers |
|---|---|
| `windows.pslist` | What processes were running? (walks the EPROCESS linked list) |
| `windows.pstree` | What spawned what? Shows parent-child relationships as a tree |
| `windows.psscan` | Finds processes by scanning memory directly — catches hidden processes that unlinked themselves from pslist |
| `windows.cmdline` | What command-line arguments did each process run with? |

### Network Analysis

| Plugin | Question it answers |
|---|---|
| `windows.netscan` | What network connections existed? Shows active + recently closed TCP/UDP connections with remote IPs and ports |

### DLL and Module Analysis

| Plugin | Question it answers |
|---|---|
| `windows.dlllist` | What DLLs did each process load? Unusual DLLs = red flag |
| `windows.modules` | What kernel modules (drivers) were loaded? |

### Malware Detection

| Plugin | Question it answers |
|---|---|
| `windows.malfind` | Where does injected or suspicious executable code live in process memory? Flags memory regions with PAGE_EXECUTE_READWRITE permissions that contain code — the classic sign of shellcode injection |
| `windows.vadinfo` | Virtual Address Descriptor analysis — maps the memory layout of a process |

### File and Registry Analysis

| Plugin | Question it answers |
|---|---|
| `windows.filescan` | What file objects were open or mapped in memory? |
| `windows.handles` | What handles (files, registry keys, mutexes) did each process have open? |
| `windows.registry.hivelist` | What registry hives were loaded in memory? |

### Credential Extraction (requires impacket)

| Plugin | Question it answers |
|---|---|
| `windows.hashdump` | What NTLM password hashes are stored in memory? |
| `windows.lsadump` | What LSA secrets are in memory? |

---

## The Investigation Methodology

Memory forensics is not about running every plugin. It is about following a **thread** — each finding leads to the next question.

### Standard Investigation Flow

```
1. windows.pslist / windows.pstree
   → Spot anything suspicious: unusual process name, wrong parent,
     running from a temp directory, duplicate of a system process

2. windows.netscan
   → Is the suspicious process making outbound connections?
     What IP? What port? Is it a known C2 port (4444, 1337, 8080)?

3. windows.cmdline
   → What command did the suspicious process run with?
     Encoded PowerShell? A path to a temp folder?

4. windows.malfind
   → Is the process injecting shellcode into other processes?
     PAGE_EXECUTE_READWRITE regions with MZ headers = injected PE

5. windows.dlllist
   → Is it loading unusual or misspelled DLLs?
     DLL hijacking and side-loading show up here

6. windows.filescan / windows.handles
   → What files was it reading or writing?
```

### Red Flags to Look For

**In pslist / pstree:**
- `svchost.exe` with no parent `services.exe`
- `explorer.exe` spawned by something other than `userinit.exe`
- Process names that look like system processes but are misspelled (`svch0st.exe`, `lsas.exe`)
- Processes running from `%TEMP%`, `%APPDATA%`, or unusual paths
- Two instances of a process that should only have one (e.g. two `lsass.exe`)

**In netscan:**
- Outbound connections on unusual ports (4444, 1337, 8080, 9001)
- Connections from processes that have no business making network calls (`notepad.exe`, `calc.exe`)
- Connections to foreign IPs from system processes

**In malfind:**
- Memory regions flagged with `PAGE_EXECUTE_READWRITE` — normal DLLs don't need write + execute simultaneously
- MZ headers (`4D 5A`) found inside a process that didn't load that DLL

---

## Process Injection — How Malware Hides

**Process injection** is a technique where malware writes its own code into the memory space of a legitimate running process (like `explorer.exe` or `svchost.exe`) and executes it from there. This is done to:
- Hide under a trusted process name
- Inherit the legitimate process's network permissions
- Evade endpoint detection tools

**Process hollowing** goes further — the malware starts a legitimate process in a suspended state, hollows out its memory, writes its own code in, then resumes it. The process looks completely legitimate from the outside.

Both techniques are what `windows.malfind` is designed to detect.

---

## Fileless Malware

Fileless malware never writes an executable to disk. It lives entirely in RAM — often injected via a malicious document macro or a browser exploit — and executes directly in memory. Because there is no file on disk, traditional antivirus that scans files misses it entirely.

Memory forensics is often the **only** way to detect and analyze fileless malware. The evidence exists only in the RAM dump.

---

## Key Forensic Notes

- Always analyze a **copy** of the memory dump — never the original.
- Hash the dump with SHA-256 before and after analysis to confirm it was not altered. *(See File Hasher Tool in this repository.)*
- Memory dump timestamps are in UTC.
- `windows.psscan` is more reliable than `windows.pslist` against sophisticated malware — rootkits can unlink themselves from the EPROCESS list (making pslist miss them) but cannot easily hide from a raw memory scan.
- A process running from `C:\Windows\System32\` is not automatically trustworthy — malware masquerades as system processes using the same names.
- Always cross-reference `netscan` output with the process list — an unknown IP connection attributed to `svchost.exe` is a major red flag.

---

## Tools Reference

| Tool | Purpose |
|---|---|
| Volatility 3 | Memory analysis framework — core investigation tool |
| WinPmem | Live RAM capture on Windows |
| LiME | Live RAM capture on Linux |
| impacket | Enables hashdump/lsadump plugins in Volatility |
| yara-python | Enables YARA rule scanning in Volatility |

---

*These notes are part of the Digital Forensics Toolkit learning documentation.*
