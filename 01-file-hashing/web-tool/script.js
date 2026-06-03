// This script is a clean, modern implementation of a client-side file hashing tool using the browser's native Web Crypto API.

// The beauty of this code is that it processes everything locally in the user's browser, meaning the file is never uploaded to a server, making it fast and private.

// When dealing with 1000 GB files, the bottleneck is usually the Read Speed of the hard drive (SSD vs HDD). Using WebAssembly as we've done here ensures that the CPU can keep up with the data coming off the disk without the browser tab ever becoming unresponsive.

document.addEventListener('DOMContentLoaded', () => { // This wraps the entire script in an event listener that waits for the HTML document to be fully loaded and parsed. This ensures that when we try to find elements like file-input, they actually exist in the DOM.

    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const resultContainer = document.getElementById('result-container');
    const hashOutput = document.getElementById('hash-output');

    // Handle file selection via button
    //  This listens for when a user selects a file via the standard file picker. If a file is selected (length > 0), it passes the first file to the processFile function. It uses async/await because hashing is an asynchronous operation.

    fileInput.addEventListener('change', async (event) => {
        if (event.target.files.length > 0) {
            await processFile(event.target.files[0]);
        }
    });
    
    // Handle Drag & Drop visuals and drops

    // When a file is hovered over the dropZone, we call preventDefault() to stop the browser's default behavior (which is often trying to open the file). We also update the CSS styles to give the user visual feedback.
    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault(); // Prevents the browser from opening the file in a new tab
        dropZone.style.borderColor = 'var(--primary)';
        dropZone.style.background = 'rgba(99, 102, 241, 0.05)';
    });

    // If the user moves the mouse away without dropping, we reset the styles to the original state.
    dropZone.addEventListener('dragleave', (event) => {
        event.preventDefault();
        dropZone.style.borderColor = 'var(--card-border)';
        dropZone.style.background = 'rgba(255, 255, 255, 0.01)';
    });

    // When the file is released (dropped), we reset the styles and grab the file from event.dataTransfer.files, passing it to processFile. 
    dropZone.addEventListener('drop', async (event) => {
        event.preventDefault();
        dropZone.style.borderColor = 'var(--card-border)';
        dropZone.style.background = 'rgba(255, 255, 255, 0.01)';
        
        if (event.dataTransfer.files.length > 0) {
            await processFile(event.dataTransfer.files[0]);
        }
    });

    // --- The Core Web Crypto API Function ---
    async function processFile(file) {
        if (!file) return;
        // 1. Update UI to show processing state. This prepares the UI. It reveals the result section and shows a "Calculating..." message so the user knows the app hasn't frozen.
        resultContainer.style.display = 'block';
        hashOutput.style.color = 'var(--text-muted)';
        hashOutput.textContent = `Calculating SHA-256 for "${file.name}"...`;
        
        // The problem is that crypto.subtle.digest is an "all-or-nothing" API. It requires the entire file to be loaded into a single ArrayBuffer in your system's RAM. For a 1,000 GB (1 TB) file, even the most powerful workstations would run out of memory and crash the browser tab.

        // To handle massive files, we need to implement Incremental Hashing (or Streaming). This involves:        

        // Chunking: Reading the file in small, manageable pieces (e.g., 64MB at a time) using file.slice().
        // Streaming Hashing: Using a hashing engine that supports an .update() method to process these pieces one by one without keeping the previous pieces in memory.
        // Unfortunately, the native Web Crypto API does not yet support streaming for digests. To solve this while maintaining high performance, the industry standard is to use a WebAssembly (WASM) library like hash-wasm. It provides near-native speeds and allows for incremental updates.

        try {
            // 2. Initialize the incremental hasher (using hash-wasm)
            // Since Web Crypto API doesn't support streaming, we use WASM for high-performance chunked hashing.
            const hasher = await hashwasm.createSHA256(); // This line initializes the WebAssembly (WASM) hashing engine. Unlike the native Web Crypto API, which requires the whole file at once, hash-wasm creates an object (hasher) that can stay "open" and receive data in small pieces.

            const chunkSize = 64 * 1024 * 1024; // 64MB chunks. We define how much of the file to read at a single time. 64MB is a "sweet spot"—it's large enough for high-speed disk I/O but small enough that it won't lag the browser's UI or consume too much RAM.

            let offset = 0; //  This is a pointer. It starts at 0 (the beginning of the file) and tracks our progress as we move through the file.

            // 3. Read and process the file in chunks
            while (offset < file.size) { // This loop will keep running as long as our offset (where we are) is less than the total file.size (the end of the file).

                const slice = file.slice(offset, offset + chunkSize); // This is the most important part for performance. file.slice() does not read the file into memory. It simply creates a "pointer" or a reference to a specific segment of the file on the user's hard drive.

                const buffer = await slice.arrayBuffer(); // Now we actually perform the disk read. This line pulls only that 64MB "slice" from the hard drive into the computer's RAM.

                hasher.update(new Uint8Array(buffer)); // We feed that 64MB chunk of data into the WASM hasher. The hasher processes the math for this chunk and updates its internal state. Immediately after this line, the buffer is no longer needed and the browser can clear that memory.
                
                offset += chunkSize; // We move our pointer forward by 64MB so that the next iteration of the loop picks up exactly where the last one left off.
                
                // Update UI with progress (helpful for massive 1TB files). Since hashing 1000 GB will take time, these lines calculate the percentage completed and update the text on the screen. Math.min(100, ...) ensures that even if our last chunk goes slightly over the file size, we never display "101%".
                const progress = Math.min(100, Math.round((offset / file.size) * 100));
                hashOutput.textContent = `Calculating SHA-256: ${progress}%...`;
            }
            
            // 4. Finalize the hash calculation
            const hashHex = hasher.digest(); // Once the while loop finishes (meaning the entire file has been read), we call .digest(). This tells the hasher: "I'm done sending data; give me the final result." It returns the completed SHA-256 string in hexadecimal format.
            
            // 5. Display the final hash. The final hash string is displayed in the UI. Finally, we update the UI to show the calculated hash and change the text color (likely to a success color like green or blue) to signal that the process is complete.

            hashOutput.style.color = 'var(--secondary)';
            hashOutput.textContent = hashHex;
        // If anything goes wrong (e.g., file permissions or memory errors), the catch block catches the error, updates the UI to show red text, and logs the error to the console for debugging.
        } catch (error) {
            hashOutput.style.color = '#ef4444'; // Red error color
            hashOutput.textContent = 'Error calculating hash.';
            console.error("Hashing failed:", error);
        }
    }
});