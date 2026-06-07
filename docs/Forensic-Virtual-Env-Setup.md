Install Oracle VirtualBox before reading this setup guide.

---

### Step 1 — Download Ubuntu ISO

Download **Ubuntu 26.04 LTS** from: https://ubuntu.com/download/desktop

Get the `.iso` file — it is approximately 6GB.

> **Note:** Ubuntu follows a strict YY.MM naming convention. LTS versions 
> are always released in April (month 04) of even-numbered years — so the 
> versions go 22.04 → 24.04 → 26.04. 

---

### Step 2 — Create a New VM in VirtualBox

**Before creating the VM**, manually create the destination folder on your 
C or D drive first [whichever you want, if C Drive has very less space, you can install in D Drive] — otherwise VirtualBox may fail to create the virtual disk:

Open PowerShell and run:
```powershell
New-Item -ItemType Directory -Path "D:\Ubuntu VM"
```

Then open VirtualBox, click **New**, and fill in:

| Setting | Value |
|---|---|
| Name | `Forensics-Lab` |
| Type | `Linux` |
| Version | `Ubuntu (64-bit)` |

On the next screens:

**Hardware:**
| Setting | Value | Notes |
|---|---|---|
| Base Memory (RAM) | `6144 MB` | Based on 16GB laptop — never exceed half your total RAM |
| Processors (CPUs) | `4` | Based on 10-core laptop |

**Hard Disk:**
| Setting | Value |
|---|---|
| Create a New Virtual Hard Disk | ✅ Selected |
| Location | `D:\Ubuntu VM\Forensics-Lab\Forensics-Lab.vdi` |
| Disk Size | `50 GB` |
| File Type | VDI (VirtualBox Disk Image) |
| Pre-allocate Full Size | ❌ Unticked (dynamically allocated) |
| Split Disk Into 2 GB Parts | ❌ Unticked |

> **Important settings to leave as default:**
> - Unattended Installation → **Untick** this. Do the installation manually 
>   for full control.
> - EFI → **Leave unticked.** Enabling EFI can cause boot issues in 
>   VirtualBox with Ubuntu.

Click **Finish.**

---

### Step 3 — Install Ubuntu

Start the VM. It will boot from the ISO and launch the Ubuntu installer.
Go through each screen as follows:

**Boot menu:**
Select **Try or Install Ubuntu.**
(Choose "Ubuntu Safe Graphics" only if you experience display glitches.)

**Internet Connection:**
Select **Use wired connection.** VirtualBox automatically provides a 
virtual wired connection through your laptop's internet.

**What do you want to do:**
Select **Install Ubuntu.**

**How would you like to install:**
Select **Interactive installation.**

**What apps would you like to install:**
Select **Default selection** — just the essentials.
(Keeps the installation lean; you will install forensic tools manually.)

**Install recommended proprietary software:**
Tick **both** checkboxes:
- ✅ Install third-party software for graphics and Wi-Fi hardware
- ✅ Download and install support for additional media formats

> These are officially curated and verified by Canonical (Ubuntu's parent 
> company). They are safe to install. The reason Ubuntu doesn't include 
> them by default is purely legal/licensing — some codecs are patented 
> in certain countries.

**How do you want to install Ubuntu:**
Select **Erase disk and install Ubuntu.**

> ⚠️ The warning sounds alarming but is completely safe. The "disk" 
> it refers to is your 50GB virtual hard disk (Forensics-Lab.vdi), 
> not your real Windows drives. Your actual C and D drives are 
> never touched.

**Encryption and file system:**
Select **No encryption.**

> Snapshot compatibility is the reason. VirtualBox snapshots — your 
> most critical safety feature for forensics work — work best with 
> unencrypted disks. Since the VM lives on your personal machine, 
> your Windows login is already the security boundary.

**Create your account:**

| Field | Recommended value |
|---|---|
| Your name | `Arko` (or any name) |
| Computer's name | `forensics-lab` (lowercase, no spaces) |
| Username | `arko` (lowercase, no spaces) |
| Password | Something memorable — write it down |

> ⚠️ Write down your username and password. You will need them every 
> time you log in and every time you run a `sudo` command to install 
> tools like Python, FastAPI, Wireshark, Autopsy, and Volatility.

**Checkboxes on account screen:**
- ✅ Require my password to log in — leave ticked
- ❌ Use Active Directory — leave unticked (corporate environments only)

**Review your choices:**
Verify the summary screen shows:
- Type of installation: Erase disk and install Ubuntu
- Installation disk: VBOX HARDDISK (confirms virtual disk, not real drive)
- Disk encryption: None
- Proprietary software: Codecs & drivers

Click **Install** and wait. The "Setting Up the System" phase is the 
longest step — it typically takes 15 to 30 minutes depending on your 
internet speed. The SATA indicator flickering at the bottom of the 
VirtualBox window confirms installation is actively progressing. 
Do not close or restart the VM during this phase.

When installation finishes, click **Restart Now.**

If prompted with "Please remove the installation medium then press ENTER", 
press Enter. The VM will reboot into your installed Ubuntu.

> **Note:** Ubuntu automatically ejects the ISO during restart. You do 
> not need to manually detach it from VirtualBox Storage settings. 
> After installation you can safely delete the `.iso` file from your 
> Downloads folder to recover ~6GB of space on your C drive.

**After first boot:**
If asked about Location Services — turn it **Off.** A forensics VM 
has no use for location data.

---

### Step 4 — Take a Clean Snapshot (Critical Step)

Once Ubuntu has booted to the desktop for the first time and before 
installing anything:

In VirtualBox menu → **Machine → Take Snapshot**

| Field | Value |
|---|---|
| Name | `Clean-Install` |
| Description | `Fresh Ubuntu 26.04 installation, nothing added yet` |

This is your permanent restore point. Any time you analyze dangerous 
malware and something goes wrong inside the VM, restore to this snapshot 
and the VM returns to exactly this state in about 30 seconds — your 
Windows host and real files are never affected.

> **Snapshot strategy going forward:**
> After completing the Python + FastAPI setup in Step 5, take a second 
> snapshot named `FastAPI-Ready`. This gives you two restore points — 
> a completely clean OS, and a ready-to-work forensics environment.


### Step 5 — Install Python and FastAPI inside the VM

Open a Terminal inside Ubuntu and run these one by one:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install fastapi uvicorn python-multipart
```

---

### Step 6 — Transfer your script into the VM

Two easy options:

**Option A — Shared Folder (Recommended):**
- VirtualBox → **Settings → Shared Folders → Add**
- Point it to your `D:\CODING\DIGITAL FORENSICS` folder on Windows
- Inside the VM it appears as a mounted drive — you can directly access your Python scripts from there

**Option B — Just copy-paste:**
- Open a text editor inside Ubuntu
- Paste your `file_signature_analyzer.py` code
- Save it

---

### Step 7 — Run the Backend inside the VM

Inside the Ubuntu terminal:

```bash
cd /path/to/your/script
uvicorn file_signature_analyzer:app --reload --host 0.0.0.0
```

Note the `--host 0.0.0.0` — this is important. By default uvicorn only listens on `127.0.0.1` which is only accessible from inside the VM itself. `0.0.0.0` makes it accessible from your host machine's browser too.

---

### Step 8 — Access it from your Windows browser

In VirtualBox → **Settings → Network**, set the adapter to **Bridged Adapter**. This gives your VM its own IP address on your local network.

Inside the VM, find its IP:

```bash
ip addr show
```

Look for something like `192.168.1.105`. Then on your **Windows browser**, open:

```
http://192.168.1.105:8000/analyze_file/
```

Your `index.html` frontend on Windows talks to the FastAPI backend running safely inside the VM.

---

### The Complete Architecture

```
Your Windows Laptop (Host)
├── Browser opens index.html
├── JS sends file to http://192.168.x.x:8000/analyze_file/
│
└── VirtualBox VM (Forensics-Lab)
    ├── Ubuntu running uvicorn
    ├── FastAPI reads 8 bytes
    ├── Returns JSON verdict
    └── If anything goes wrong → Restore Clean-Install snapshot
```

---

### One Last Thing — Take a Second Snapshot

After completing Steps 5 and 6 (Python + FastAPI installed, script ready), take another snapshot:

```
Snapshot 2: "FastAPI-Ready"
```

Now you have two restore points — a completely clean OS, and a ready-to-work forensics environment. Restoring takes about 30 seconds in VirtualBox.


### What is guaranteed
- **The VM is the blast radius.** Malware executing inside Ubuntu cannot touch your Windows files, your Windows registry, your real documents, or your actual hard drive. The virtual hard disk is just a file sitting on your Windows machine — the malware inside has no idea Windows even exists underneath it.
- **Snapshot restoration is instant and complete.** Restoring to `Clean-Install` or `FastAPI-Ready` rolls back every single file, every config change, every malware dropper — as if nothing ever happened. It takes about 30 seconds.

---

### The rare exceptions worth knowing (so you're never blindsided)

**1. VM Escape (Extremely Rare)**
A highly sophisticated, nation-state level exploit can sometimes break out of the VM and reach the host. These are called **hypervisor vulnerabilities** and are worth tens of thousands of dollars on exploit markets. You will essentially never encounter this in a normal forensics workflow — but it is why professional malware labs use **dedicated physical machines** with no network connection for the most dangerous samples.

**2. Shared Folders are a bridge**
If you set up a Shared Folder between Windows and the VM (Step 6 Option A), malware running inside the VM **can see and write to that shared folder**. This means it could potentially drop files onto your real Windows filesystem through that bridge.

The fix is simple:

```
Never mount a Shared Folder when analyzing
untrusted or potentially malicious files.
Transfer your scripts once, then disable
the shared folder before doing any analysis.
```

**3. Network is a two-way street**
If your VM is on Bridged Adapter mode, the malware could potentially scan and attack other devices on your home network (your router, your phone, other laptops). The fix:

```
Switch Network Adapter to "Host-Only" mode
during malware analysis. This lets your
Windows browser still reach the VM but
completely cuts the VM off from the internet
and your home network.
```

---

### Your Safe Analysis Checklist

Before dropping any suspicious file into your VM for analysis:

```
☐ Shared Folders → Disabled
☐ Network Adapter → Host-Only
☐ Snapshot taken → "FastAPI-Ready"
☐ Then analyze freely
☐ After analysis → Restore snapshot
```

Follow that checklist every single time and your host machine will never be at risk. This is almost exactly the same workflow professional malware analysts use at cybersecurity firms.
