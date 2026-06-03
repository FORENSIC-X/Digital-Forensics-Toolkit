# This is a Metadata Extraction Tool designed for digital forensics. It retrieves "hidden" data about a file from two sources: the Operating System (MAC times) and the file itself (EXIF data from images).

# These import standard Python libraries. os is for interacting with the file system, sys is for handling command-line arguments, and datetime is for converting raw timestamps into human-readable dates.
import os
import sys
from datetime import datetime

# We use the Pillow library to easily extract hidden EXIF data from images

# This block checks if the Pillow (PIL) library is installed. Pillow is the industry standard for image processing in Python. If it's missing, the script sets HAS_PIL to False so it can fail gracefully later rather than crashing.
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    
    # This part acts as our "OS Metadata" analyzer. It asks our Windows operating system for the file's MAC Times (Modified, Accessed, Created timestamps) and its size in bytes. It uses the built-in 
    # os.stat() function to grab this hidden data.
    
    # This function focuses on metadata held by the File System (like NTFS or APFS). os.stat() is a powerful command that asks the OS for the file's status record.
def get_basic_metadata(file_path): 
    """Extracts basic Operating System Metadata (MAC Times)"""
    print(f"\n--- Basic OS Metadata for: {file_path} ---")
    
    # os.stat asks the operating system for the file's hidden properties
    stat_info = os.stat(file_path)
    
    # st_size: The file size.
    print(f"Size: {stat_info.st_size} bytes")
    
    # Convert the raw timestamps into human-readable dates. 
    # These extract the MAC times:
    # st_birthtime: When the file was Created (Note: This is platform-dependent; on Windows, it is the creation time).
    # st_mtime: When the file was last Modified.
    # st_atime: When the file was last Accessed.
    # The datetime.fromtimestamp() method converts the raw Unix seconds (e.g., 1717227600) into a readable format like 2024-06-01 10:00:00
    created = datetime.fromtimestamp(stat_info.st_birthtime)
    modified = datetime.fromtimestamp(stat_info.st_mtime)
    accessed = datetime.fromtimestamp(stat_info.st_atime)
    
    print(f"Created (C):  {created}")
    print(f"Modified (M): {modified}")
    print(f"Accessed (A): {accessed}")
    
    # EXIF (Exchangeable Image File Format) is metadata that smartphones and digital cameras secretly embed directly into the picture file itself when you take a photo.
    
    # It can contain the exact GPS coordinates where the photo was taken, the make and model of the camera (e.g., iPhone 14), the software used to edit it, and the date/time the shutter was pressed.
    
    # If you feed a text file or a video into this script, it will gracefully skip this part. But if you feed it a JPEG from your phone, it will extract all the hidden tags.
    
    # This function looks for metadata inside image files (like JPEGs). If Pillow isn't installed, it prints a helpful instruction and stops.
def get_exif_metadata(file_path):
    """Extracts hidden EXIF metadata from Image files"""
    if not HAS_PIL:
        print("\nPillow library not installed. Run 'pip install Pillow' to extract image metadata.")
        return
    
    # It attempts to open the file as an image. _getexif() is a method that pulls the "Exchangeable Image File Format" data, which includes camera settings, GPS, and timestamps embedded by the camera hardware.   
    try:
        # Try to open the file as an image. 
        image = Image.open(file_path)
        
        # ._getexif() extracts the raw metadata dictionary
        # In newer Pillow versions, .getexif() is preferred, but _getexif() often grabs more deep data
        exif_data = image._getexif()
        
        #  If the image exists but has no EXIF data (common if the image was downloaded from social media, which often strips metadata for privacy), it informs the user.
        if not exif_data:
            print("\nNo EXIF metadata found in this image. (It may have been stripped).")
            return
        
        print("\n--- Hidden Image EXIF Metadata ---")
        
        # EXIF data is stored as a dictionary where the keys are numeric IDs (e.g., 271). TAGS.get(tag_id) converts that number into a human word like "Make".
        
        # Loop through all the raw metadata tags
        for tag_id in exif_data:
            # Convert the raw numeric ID (e.g., 271) into a human-readable name (e.g., 'Make')
            tag_name = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            
            # Some metadata is stored as raw binary (bytes). This ensures it's converted to a string so it can be printed clearly.
            # Sometimes data is stored as raw bytes, so we clean it up for printing
            if isinstance(data, bytes):
                data = data.decode(errors="replace")
                
            print(f"{tag_name:25}: {data}")
            
    except Exception:
        # If the file isn't a picture (like a text file), it will jump here and skip it
        print("\n[Note: File is not a supported image. Skipping EXIF extraction.]")

# This ensures the script only runs if executed directly. It checks if the user provided a filename in the command line (e.g., python metadata_extractor.py photo.jpg).
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python metadata_extractor.py <path_to_file>")
        
    # If a file was provided, it checks if it actually exists. If it does, it runs both the OS metadata scan and the Image EXIF scan.
    else:
        target_file = sys.argv[1]
        if os.path.isfile(target_file):
            get_basic_metadata(target_file)
            get_exif_metadata(target_file)
        else:
            print(f"Error: The file '{target_file}' does not exist.")
