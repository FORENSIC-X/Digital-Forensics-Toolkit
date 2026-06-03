# What is a "Hash"? (The Foundation of Disk Forensics)
# In forensics, you must prove that the evidence you are analyzing in court is exactly the same as it was when you found it on the suspect's computer.

# A Hash is like a digital fingerprint for a file. It's a mathematical algorithm that reads every single 1 and 0 in a file and spits out a unique string of characters.

# If you have a 10 GB movie file and a tiny text file, they both get their own unique, fixed-length hash.
# If you change even a single comma in a text document, the resulting hash will change completely. This proves the file was tampered with!

import hashlib # This brings in Python's built-in library for calculating hashes (like MD5 or SHA-256). We don't have to write the complex math ourselves!

import sys # This allows the script to read arguments passed from the command line (like the name of the file you want to analyze).

import os # This gives us tools to interact with the operating system, like checking if a file actually exists.

def calculate_hashes(file_path): # We define a reusable "function" that takes the path to a file as its input.
    
    # Check if the file actually exists. We use the os library to check if the file the user provided actually exists on the hard drive. If it doesn't, we print an error and stop.
    
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    
    # We use these specific algorithms because they are standard in forensics. Here, we create three "empty" hasher objects using the hashlib library. MD5, SHA-1, and SHA-256 are three different types of hashing algorithms. SHA-256 is currently the industry standard for forensics because it is extremely secure.
    md5_hash = hashlib.md5()
    sha1_hash = hashlib.sha1()
    sha256_hash = hashlib.sha256()
    print(f"Calculating hashes for: {file_path}")
    print("-" * 40)
    try:
        
        # Open the file in binary mode ('rb') to read raw bytes.
        
        # This is important because hashing looks at the exact 1s and 0s of the file, not the text. This is the most crucial part. We are opening the file in "rb" mode, which stands for Read Binary. We don't care if the file is a picture, a word document, or a virus. We just want to read the raw 1s and 0s (bytes) that make up the file.
        
        with open(file_path, "rb") as f:
            # Read the file in chunks (e.g., 4096 bytes at a time)
            # This prevents our program from crashing if we try to hash a massive file (like a 100GB hard drive image).
            
            #  In forensics, you might have to hash a 1,000 GB hard drive image. If you try to load 1,000 GB into your RAM all at once, your computer will crash. Instead, this loop reads the file in small, 4096-byte chunks.
            
            for byte_block in iter(lambda: f.read(4096), b""):
                
                # As we read each small chunk of the file, we feed it into our empty hasher objects. They continuously update their internal math until the whole file is read.
                
                md5_hash.update(byte_block)
                sha1_hash.update(byte_block)
                sha256_hash.update(byte_block)
                
        # Print the final calculated hashes in hexadecimal format. Once the entire file has been fed into the hashers, this .hexdigest() command asks them to spit out the final result in a human-readable format (hexadecimal string).
        
        print(f"MD5:    {md5_hash.hexdigest()}")
        print(f"SHA-1:  {sha1_hash.hexdigest()}")
        print(f"SHA-256:{sha256_hash.hexdigest()}")
        
    except Exception as e1:
        print(f"An error occurred while reading the file: {e1}")
        
# This last part written below just makes the script usable from the command prompt. sys.argv is a list of words you typed in the terminal. If you type python file_hasher.py evidence.txt, sys.argv[1] grabs the word evidence.txt and passes it to our function.

if __name__ == "__main__":
    # This block allows us to run the script from the command line
    # e.g., python file_hasher.py my_evidence_file.txt
    if len(sys.argv) < 2:
        print("Usage: python file_hasher.py <path_to_file>")
    else:
        target_file = sys.argv[1]
        calculate_hashes(target_file)