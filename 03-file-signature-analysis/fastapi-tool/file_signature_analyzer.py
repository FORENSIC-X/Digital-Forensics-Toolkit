import os
import platform
from contextlib import asynccontextmanager
# NEW: These imports turn it into a FastAPI app
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

MAGIC_NUMBERS = {
    # --- IMAGES ---
    bytes([0xFF, 0xD8, 0xFF])          : ("JPEG Image",    [".jpg", ".jpeg"]),
    bytes([0x89, 0x50, 0x4E, 0x47])    : ("PNG Image",     [".png"]),
    bytes([0x47, 0x49, 0x46, 0x38])    : ("GIF Image",     [".gif"]),
    bytes([0x42, 0x4D])                : ("BMP Image",     [".bmp"]),
    bytes([0x49, 0x49, 0x2A, 0x00])    : ("TIFF Image",    [".tif", ".tiff"]),
    bytes([0x57, 0x45, 0x42, 0x50])    : ("WebP Image",    [".webp"]),

    # --- DOCUMENTS ---
    bytes([0x25, 0x50, 0x44, 0x46])    : ("PDF Document",  [".pdf"]),
    bytes([0xD0, 0xCF, 0x11, 0xE0])    : ("MS Office (Old) — DOC/XLS/PPT", [".doc", ".xls", ".ppt"]),
    bytes([0x50, 0x4B, 0x03, 0x04])    : ("ZIP / Modern Office (DOCX/XLSX/PPTX/JAR/APK)", [".zip", ".docx", ".xlsx", ".pptx", ".jar", ".apk"]),

    # --- EXECUTABLES & BINARIES ---
    bytes([0x4D, 0x5A])                : ("Windows Executable / DLL", [".exe", ".dll"]),
    bytes([0x7F, 0x45, 0x4C, 0x46])    : ("Linux ELF Executable",     [".elf", ".so"]),
    bytes([0xCA, 0xFE, 0xBA, 0xBE])    : ("Java Class File",          [".class"]),

    # --- ARCHIVES ---
    bytes([0x52, 0x61, 0x72, 0x21])    : ("RAR Archive",   [".rar"]),
    bytes([0x1F, 0x8B])                : ("GZIP Archive",  [".gz", ".tar.gz"]),
    bytes([0xFD, 0x37, 0x7A, 0x58])    : ("XZ Archive",    [".xz"]),

    # --- AUDIO / VIDEO ---
    bytes([0x49, 0x44, 0x33])          : ("MP3 Audio",     [".mp3"]),
    bytes([0x66, 0x74, 0x79, 0x70])    : ("MP4 Video",     [".mp4", ".m4v", ".mov"]),
    bytes([0x1A, 0x45, 0xDF, 0xA3])    : ("MKV / WebM Video", [".mkv", ".webm"]),
    bytes([0x52, 0x49, 0x46, 0x46])    : ("AVI Video / WAV Audio", [".avi", ".wav"]),

    # --- DATABASES & FORENSIC IMAGES ---
    bytes([0x53, 0x51, 0x4C, 0x69])    : ("SQLite Database", [".db", ".sqlite", ".sqlite3"]),
    bytes([0x45, 0x57, 0x46, 0x32])    : ("EWF Forensic Disk Image (Expert Witness)", [".e01"]),
    bytes([0x4D, 0x52, 0x56, 0x4E])    : ("VMware VMDK Disk Image", [".vmdk"]),

    # --- SCRIPTS & MISCELLANEOUS ---
    bytes([0x23, 0x21])                : ("Script / Shebang (Python, Bash, etc.)", [".py", ".sh"]),
    bytes([0x37, 0x7A, 0xBC, 0xAF])    : ("7-Zip Archive",  [".7z"]),
    bytes([0x50, 0x4B, 0x05, 0x06])    : ("Empty ZIP Archive", [".zip"]),
}

# @app.post("/analyze_file/") : 
# This is a decorator — it is a special instruction written above a function that modifies how that function behaves.

# app is our FastAPI application object (created by app = FastAPI()). We are telling it: "Whenever someone sends an HTTP POST request to the URL /analyze_file, run the function written directly below me."

# Why POST and not GET?
# GET = you are only asking for information (like opening a webpage).
# POST = you are sending data to the server (like submitting a form or uploading a file).

# Since the user is uploading a file, we use POST.


# async def analyze_file(file: UploadFile): 
# This has three parts: 

# a) async def instead of just def =>

# The async keyword means this function is asynchronous. In a normal Python function, if one task takes time (like waiting for a 2GB file to finish uploading), the entire program freezes and cannot handle any other request until that task finishes.
# async tells Python: "While you are waiting for this slow task, go ahead and handle other incoming requests in the meantime. Come back to this one when it's ready." This is what makes FastAPI fast enough for real-world web servers.

# b) file: =>

# This is the parameter name. FastAPI automatically intercepts the file the user uploaded from the browser and passes it into this function as this parameter.
 
# c) UploadFile =>

# This is a type hint. It tells FastAPI exactly what kind of data to expect — specifically a file upload. FastAPI uses this hint to automatically validate the incoming request. If someone sends plain text instead of a file, FastAPI rejects it before our code even runs.   

'''header = await file.read(8) => Reads the first 8 bytes of the uploaded file to determine its true type via magic numbers and compares it against the provided file extension.
    It also has three parts:
    a) file.read(8):
    Just like f.read(8) in our original script, this reads the first 8 bytes of the uploaded file. 

    b) await:
    Remember how async def told Python "this function might have to wait for slow tasks"? The await keyword is how you mark exactly which line is the slow task.
    When Python hits await file.read(8), it says: "Reading this file from the network might take a moment. I'll start it, but while I wait for those 8 bytes to arrive, I'll go handle other incoming requests. The moment those 8 bytes are ready, I'll come straight back to this exact line and continue."
    Without await, your async function would block just like a regular function — defeating the entire purpose of making it asynchronous in the first place.
    
    c) header =:
    Once the 8 bytes have fully arrived and await brings execution back to this line, those 8 bytes get stored in header — and from this point on, your original script logic runs completely unchanged.
'''

# ── VM Environment Check ──────────────────────────────────────
def check_environment():
    """
    Warns the investigator if the tool is NOT running inside a VM.
    Analyzing untrusted/malicious files on a host machine is against
    forensic best practices. Always run inside a snapshot-capable VM.
    """
    vm_indicators = ["vmware", "virtualbox", "vbox", "virtual", "qemu", "hyperv"]
    system_info = platform.node().lower() + platform.version().lower()
    is_vm = any(indicator in system_info for indicator in vm_indicators)

    if not is_vm:
        print("=" * 60)
        print("  ⚠  SECURITY WARNING")
        print("  This tool does not appear to be running inside a VM.")
        print("  Analyzing untrusted files on a host machine is")
        print("  against forensic best practices.")
        print("  Recommended: Run inside VMware / VirtualBox snapshot.")
        print("=" * 60)
    else:
        print("✓ VM environment detected. Safe to proceed.")

# ── FastAPI Lifespan (runs check before server accepts requests) ──
@asynccontextmanager
async def lifespan(app: FastAPI):
    check_environment()   # Fires automatically on every uvicorn startup
    yield                 # Server runs here — handling all requests
                          # Any cleanup code goes after yield (on shutdown)

# ── App Initialization ────────────────────────────────────────
app = FastAPI(lifespan=lifespan)

# Our frontend is calling: http://localhost:8000/analyze_file/
# But we may hit a CORS error in the browser once the frontend tries to talk to the backend. This is because the browser blocks requests from one origin (our HTML file) to another (the FastAPI server) by default.
# This below block tells FastAPI: "Accept requests from any origin" — which is safe for a local forensics tool. Without this, our browser will refuse to send the file even though uvicorn is running perfectly.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Endpoint ──────────────────────────────────────────────────
@app.post("/analyze_file/") 
async def analyze_file(file: UploadFile):    
    # Reading from the network stream is an async operation
    header = await file.read(8) 
    
    file_name = file.filename
    
    flag = 1
    for magic_bytes in MAGIC_NUMBERS:
        if header.startswith(magic_bytes): 
            flag = 0
            break
        
    if flag == 1:
        return JSONResponse(content={"message": "FILE SIGNATURE DOESN'T MATCH WITH ANY KNOWN SIGNATURE IN OUR DICTIONARY!"})
    else:   
        actual_extension = os.path.splitext(file_name)[1].lower() # Finding the actual extension of the file as per its filename entered by user
        if actual_extension in MAGIC_NUMBERS[magic_bytes][1]:
            return JSONResponse({
                "file_name"  : file_name,
                "true_type"  : MAGIC_NUMBERS[magic_bytes][0],
                "extension"  : actual_extension,
                "match"      : True,
                "message"    : "FILE SIGNATURE MATCHES WITH ITS EXTENSION !"
            })  
        else:
            return JSONResponse({
                "file_name"  : file_name,
                "true_type"  : MAGIC_NUMBERS[magic_bytes][0],
                "extension"  : actual_extension,
                "match"      : False,
                "message"    : "FILE SIGNATURE DOES NOT MATCH WITH ITS EXTENSION !"
            })  

# Step-1 :
# [If not already installed] Install fastapi using the following command in your terminal : 
# pip install fastapi
                  
# Step-2 :
# [If not already installed] Install python-multipart using the following command in your terminal : 
# pip install python-multipart
# FastAPI requires this library to handle file uploads

# Step-3 :
# Go to the appropriate directory in which the file_signature_analyzer.py file is present and Run the Python Fast API script in file_signature_analyzer.py with: 
# uvicorn file_signature_analyzer:app --reload