Great, VirtualBox is the perfect free tool for this! Here is the complete setup guide.

---

### Step 1 — Download a Linux ISO

You need an operating system image to install inside VirtualBox. For forensics, **Ubuntu 22.04 LTS** is the standard choice.

Download it from: **https://ubuntu.com/download/desktop**

Get the `.iso` file — it is about 5GB.

---

### Step 2 — Create a New VM in VirtualBox

Open VirtualBox and click **New**, then fill in:

| Setting | Value |
|---|---|
| Name | `Forensics-Lab` |
| Type | `Linux` |
| Version | `Ubuntu (64-bit)` |
| RAM | `4096 MB` (4GB minimum) |
| CPU cores | `2` |
| Hard Disk | `25 GB` (dynamically allocated) |

---

### Step 3 — Attach the ISO and Install Ubuntu

- Go to **Settings → Storage → Empty optical drive**
- Click the disc icon and choose your downloaded `.iso` file
- Start the VM
- Follow Ubuntu's installer — choose **"Erase disk and install Ubuntu"** (this only erases the virtual disk, not your real laptop)
- Set a username and password you'll remember

---

### Step 4 — Take a Clean Snapshot (Critical Step)

Once Ubuntu is installed and booted, **before doing anything else**:

- In VirtualBox menu → **Machine → Take Snapshot**
- Name it `Clean-Install`

This is your **restore point**. Any time you analyze dangerous malware and want to wipe the slate clean, you restore to this snapshot and the VM is back to day one — your host laptop is completely untouched.

---

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