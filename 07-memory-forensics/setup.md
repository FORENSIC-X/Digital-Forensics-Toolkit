# Memory Forensics — Volatility 3 Setup Guide

Installation guide for Volatility 3 on Ubuntu 26.04 LTS inside a VirtualBox VM.

---

## Prerequisites

- Ubuntu 26.04 LTS VM running in VirtualBox
- Snapshot taken before starting (recommended: "Forensics-Ready")
- Internet connection inside the VM

---

## Step 1 — Update the System

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 2 — Install System Dependencies

```bash
sudo apt install -y python3 python3-pip python3-dev git libssl-dev
```

---

## Step 3 — Clone Volatility 3

```bash
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
```

---

## Step 4 — Install the venv Package

Ubuntu 26.04 ships with Python 3.14, which requires a separate venv package:

```bash
sudo apt install python3.14-venv
```

> If you're on a different Ubuntu version, replace `3.14` with your Python version.
> Check your version with: `python3 --version`

---

## Step 5 — Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal prompt will change to show `(venv)` — confirming the virtual environment is active.

> **Every time you open a new terminal session**, reactivate the venv before using Volatility:
> ```bash
> cd volatility3
> source venv/bin/activate
> ```

---

## Step 6 — Install Volatility 3

Volatility 3 uses `pyproject.toml` instead of `requirements.txt`. Install with:

```bash
pip install -e .
```

The `-e` flag means editable install — Volatility is installed directly from the cloned source folder into your venv.

Expected output ends with:
```
Successfully installed pefile-2024.8.26 volatility3-2.28.3
```

---

## Step 7 — Verify Installation

```bash
python3 vol.py -h
```

You should see the Volatility help menu listing all available plugins.

Quick check — confirm core plugins are loaded:

```bash
python3 vol.py -h | grep windows.ps
```

Expected output:
```
volatility3.plugins.windows.pslist
volatility3.plugins.windows.pstree
volatility3.plugins.windows.psscan
```

---

## Optional — Install Additional Plugin Dependencies

Some plugins require extra libraries. Install them when needed:

```bash
pip install impacket        # Enables: hashdump, lsadump, cachedump
pip install yara-python     # Enables: yarascan, vadyarascan
```

These are advanced plugins not needed for initial investigations. The warning
`"The following plugins could not be loaded"` on startup is normal without them.

---

## Volatility Version Installed

| Component | Version |
|---|---|
| Volatility | 3.28.3 |
| pefile | 2024.8.26 |
| Python | 3.14.x |
| OS | Ubuntu 26.04 LTS |

---

## Running Volatility Against a Memory Dump

Basic syntax:

```bash
python3 vol.py -f /path/to/memory.raw <plugin>
```

Example:

```bash
python3 vol.py -f memory.raw windows.pslist
```

---

## Part of

[Digital Forensics Toolkit](../../) — Memory Forensics section.
