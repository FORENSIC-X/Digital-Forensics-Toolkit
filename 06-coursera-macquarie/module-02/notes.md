# Module 02 — Notes
## Data Acquisition

**Course:** Cybersecurity: Digital Forensics — Macquarie University (Coursera)
**Module:** 02 — Data Acquisition

---

## Learning Outcomes

- Explain ways to determine the best acquisition method
- Describe contingency planning for data acquisitions
- Explain how to use acquisition tools and apply data-hiding and validation methods
- Determine what data to analyse in a digital forensics investigation

---

## 1. What is Data Acquisition?

Data acquisition is the process of copying or collecting data from electronic media for forensic investigation. Electronic media can be either:

- **Live/running devices** — workstations, mobile phones, servers with active RAM
- **Switched-off devices** — USB drives (flash), HDDs (magnetic), SSDs

Acquisition tasks are categorised into two major classes based on the state of the device: **Static Acquisition** and **Live Acquisition**.

---

## 2. Types of Acquisition

### Static Acquisition

Collecting data from **switched-off** flash, magnetic, and solid-state devices.

- **Efficient** — fast data collection
- **Ineffective** when whole-disk encryption is in use — the drive contents are unreadable without the decryption key
- Typically performed on devices seized during raids by law enforcement

### Live Acquisition

Collecting data from **live, running** devices — particularly important for capturing volatile data in RAM (running processes, open network connections, cached credentials, encryption keys).

- **Effective** — captures volatile data that disappears on shutdown
- **Inefficient** — requires the device to remain running throughout acquisition
- Critical in modern investigations where RAM forensics is increasingly important

> **Key principle for both types:** The integrity of acquired data must be verified — acquisition tools or device state may change during the process. Always hash before and after.

---

## 3. Storage Formats for Digital Evidence

Data can be acquired and stored in three main formats:

### Raw Format

Bit-by-bit copy from source disk to target disk of equal or larger size. Unix/Linux `dd` command is the standard utility for raw acquisition.

| Advantages | Disadvantages |
|---|---|
| Fast data transfers | Resource inefficient — requires as much storage as the source drive |
| Can ignore minor data read errors on source drive | Forensic tools may struggle with bad sectors on source drive |
| Portable and readable — most forensic tools can read this format | No built-in integrity check — hash validation must be stored in a separate file |

### Proprietary Format

Commercial forensic tools use their own formats (e.g. EnCase's `.E01` Expert Witness Format) to complement tool features and provide enhanced functionality.

| Advantages | Disadvantages |
|---|---|
| Provides compression to save space on target drive | Does not facilitate sharing images between different forensic tools |
| Splits large files into segments for storage (typically 650 MB or 2 GB per segment) | File size restriction per segmented volume |
| Integrates metadata into the image file along with integrity checks | Unofficial standards — Expert Witness format is not universally adopted |

### Advanced Forensics Format (AFF)

An open-source acquisition format offering:

- Compressed or uncompressed image files
- No size limitation for disk-to-image files
- Space in image file or segmented files for metadata
- Internal consistency checks for self-authentication

---

## 4. Acquisition Methods

### Disk-to-Image File
The most common method. Copies data bit-by-bit from source to target. Supported by ProDiscover, EnCase, FTK, SMART, Sleuth Kit, X-Ways, iLook. May not be feasible due to hardware legacy issues or software incompatibilities.

### Disk-to-Disk Copy
Adjusts the target disk's geometry (cylinder, head, and track configuration) to match the suspect's drive — facilitates accurate acquisition when disk-to-image is not viable.

### Logical Disk-to-Disk/File
Copies only the logical file system rather than the entire physical disk. More efficient in terms of time and storage space but does not capture deleted files or unallocated space.

### Sparse Copy
Collects only some data from the source drive for rapid investigation. Used when speed is prioritized over completeness — not appropriate for full forensic investigations.

---

## 5. Choosing the Best Acquisition Method

The best method depends entirely on the investigation scenario:

| Scenario | Recommended Method |
|---|---|
| Standard seized device — no encryption | Disk-to-image file |
| Legacy hardware with geometry issues | Disk-to-disk copy |
| Time-sensitive investigation, partial data needed | Sparse copy |
| Only active files needed, speed prioritized | Logical disk-to-file |
| Live running device with volatile RAM data | Live acquisition |

---

## 6. Contingency and Validation Planning

### Why Contingency Planning Matters

Forensic tools — both software and hardware — can have bugs and faults. If an acquisition fails midway, repeating it on a suspect device is time-consuming and may not always be possible. Planning ahead prevents critical failures.

**Best practice:** Create at least **two copies or images** of the evidence using **at least two different tools** — for example, one image with FTK Imager Lite and another with X-Ways Forensics. If one tool fails or produces a corrupt image, the second copy from the independent tool serves as backup.

### Host Protected Area (HPA)

Some acquisition tools do not copy data in the **Host Protected Area (HPA)** — a hidden region of a disk drive not accessible through normal OS interfaces. Always check vendor documentation to confirm whether your tool can access the HPA. Tools capable of reading HPA include Belkasoft, ILookIX IXImager, Image MASSter Solo, and X-Ways Replica (used with a write-blocker).

### Validation via Hashing

Every acquired image must be validated by hashing. Modern forensic tools provide built-in hashing utilities that produce a binary or hexadecimal string representing the uniqueness of the acquired data set — the **digital fingerprint**.

**How it works:**

```
Input File → Hash Function → Output: c83c10073a1cf5cfc2570 (unique hexadecimal string)
```

Any alteration to the file — even changing a single letter from uppercase to lowercase — produces a completely different hash value. If the hash of the acquired image matches the hash of the original source, the acquisition is validated as an exact copy.

---

## 7. Data-Hiding Techniques

Data hiding involves changing or manipulating a file to conceal information. Investigators must be aware of these techniques because suspects actively use them to hide evidence.

### Common Data-Hiding Techniques

| Technique | Description |
|---|---|
| Hiding entire partitions | Creating hidden disk partitions not visible to the OS |
| Changing file extensions | Renaming `.exe` to `.jpg` — detected by magic number analysis |
| Setting file attributes to hidden | Using OS-level hidden attribute flags |
| Encryption | AES-256, BitLocker, VeraCrypt — renders data unreadable without key |
| Password protection | Document-level password locks |
| Bit-shifting | Shifting all bits in a file left or right — transforms readable content into binary-looking noise |

### Bit-Shifting in Detail

Bit-shifting is one of the more subtle hiding techniques — it doesn't encrypt data but makes it look like meaningless binary noise by shifting every bit in the file one position left or right.

**Tool used:** WinHex (hex editor)

**Practical demonstration — what happens during bit-shifting:**

Original file `Bit_shift.txt` contains readable text. When viewed in WinHex before shifting, the hex values and their ASCII equivalents are clearly readable:

```
Offset    Hex Values                          ANSI ASCII
00000000  44 69 67 69 74 61 6C 20...          Digital Forensic...
```

After applying **Left shift by 1 bit** in WinHex (Edit → Modify Data → Left shift by 1 bit), the same file's content transforms into unreadable binary noise:

```
Offset    Hex Values
00000000  88 D2 CE D2 E8 C2 D8 40 8C DE...
```

The ANSI ASCII column shows only dots and symbols — no readable text. The data appears to be random binary executable content to anyone without knowledge of the bit-shift operation.

**Recovery:** Applying a **Right shift by 1 bit** to the shifted file perfectly restores the original content.

**Validation:** Computing MD5 hashes of all three files confirms:
- `Bit_shift.txt` (original) and `Bit_shift_right.txt` (restored) → **identical MD5 hash** ✅
- `Bit_shift_left.txt` (shifted) → **completely different MD5 hash** ✅

This proves the bit-shift operation altered the file, and the reverse operation perfectly recovered the original — verified mathematically.

> **Forensic significance:** If an investigator encounters a file that appears to be random binary data but has no recognizable file signature (magic number), bit-shifting is one of the first data-hiding techniques to test. The file size will be identical to what the original should be, which is a clue that the content was transformed rather than encrypted.

---

## 8. Remote Network Acquisitions

Most modern forensic tools support remote acquisition — connecting to a suspect computer or device over a network to acquire disk data or fragments without physical access.

**Two approaches:**

**Manual intervention required:** The tool connects remotely but requires someone on-site at the suspect machine to initiate the data copy.

**Surreptitious acquisition:** The tool acquires data through an encrypted link by pushing a remote access program to the suspect's computer — no on-site intervention required.

**Advantages of remote acquisition:**
- Saves travel time for the forensic team
- Minimizes risk of the forensic team being exposed to suspects
- Enables rapid response in geographically distributed investigations

---

## 9. Key Concepts — Quick Reference

| Concept | Definition |
|---|---|
| **Static Acquisition** | Data collection from switched-off devices |
| **Live Acquisition** | Data collection from running devices — captures volatile RAM data |
| **Raw Format** | Bit-by-bit copy — portable, no built-in integrity check |
| **Proprietary Format** | Vendor-specific format with compression and integrity checks (e.g. `.E01`) |
| **AFF** | Open-source format with no size limits and built-in self-authentication |
| **Sparse Acquisition** | Partial data collection — fast but incomplete |
| **HPA** | Host Protected Area — hidden disk region not accessible by standard OS tools |
| **Digital Fingerprint** | Hash value uniquely identifying a file or disk image |
| **Bit-shifting** | Data-hiding technique that shifts all bits left or right — makes readable content appear as binary noise |
| **Validation** | Confirming acquired image integrity by comparing source and image hash values |

---

## 10. Summary

Module 02 covered the complete data acquisition process — the distinction between static and live acquisition, the three storage formats (Raw, Proprietary, AFF) with their trade-offs, the four acquisition methods and when to use each, contingency planning including the two-tool redundancy principle and HPA awareness, hash-based validation, data-hiding techniques with particular focus on bit-shifting, and remote network acquisition capabilities.

**Core principle:**
> *The acquisition method must match the investigation scenario. No single method works for all cases — choosing wrong means either missing volatile evidence (static on a live machine) or getting an incomplete image (sparse when full recovery is needed).*