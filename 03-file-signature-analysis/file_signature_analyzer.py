import os
import sys

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

def file_signature_detector(file_path):
    print('-'*40)
    file_name = os.path.basename(file_path)  # Handles both / and \ correctly to extract the file name. 
    
    # What if we used file_name = file_path[file_path.rfind('/')+1:] 
    # because finding file name which is usually the string following the last '\' of the file path. If user enters only file name, then also, rfind() will return -1 and -1+1=0 so file_name=file_path[0:] which will give the full name of the file ? 
    
    # On Windows, paths use backslash → D:\Evidence\file.exe
    # rfind('/') returns -1, so file_name becomes the full path instead of just the name. That's why we used os.path.basename() here
    print("Analyzing file: ", file_name)
    print('-'*40)
    
    with open(file_path,"rb") as f: # Opening the File in Read Binary Mode
        header=f.read(8) # Reading only the first 8 bytes of the file 
    
    flag=1
    for magic_bytes in MAGIC_NUMBERS:
        if header.startswith(magic_bytes): 
            flag=0
            break
        else:
            flag=1
            
    if(flag==1):
        print("FILE SIGNATURE DOESN'T MATCH WITH ANY KNOWN SIGNATURE IN OUR DICTIONARY!")
    else:
        print("It is a : ", MAGIC_NUMBERS[magic_bytes][0])    
        actual_extension = os.path.splitext(file_name)[1].lower() # Finding the actual extension of the file as per its filename entered by user
        if actual_extension == (MAGIC_NUMBERS[magic_bytes][1]) or actual_extension in MAGIC_NUMBERS[magic_bytes][1]:
            print("\nFILE SIGNATURE MATCHES WITH ITS EXTENSION !")   
        else:
            print("\nFORENSIC ALERT ! FILE SIGNATURE DOES NOT MATCH WITH ITS EXTENSION !")       

if __name__ == "__main__":
    # This block allows us to run the script from the command line
    # e.g., python file_hasher.py image.jpeg
    if len(sys.argv) < 2:
        print("Usage: python file_signature_analyzer.py <path_to_file>")
    else:
        target_file = sys.argv[1]
        file_signature_detector(target_file)