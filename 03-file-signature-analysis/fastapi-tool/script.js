        const uploadCard = document.getElementById('uploadCard');
        const uploadCardOne = document.getElementById('uploadCardOne');
        const uploadCardTwo = document.getElementById('uploadCardTwo');
        const fileInput = document.getElementById('fileInput');
        const fileInfoStrip = document.getElementById('fileInfoStrip');
        const btnWrapper = document.getElementById('btnWrapper');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const resultPanel = document.getElementById('resultPanel');
 
        let selectedFile = null;
 
        // Click on card opens file picker
        uploadCard.addEventListener('click', () => fileInput.click());
 
        // Drag & Drop
        uploadCard.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadCard.classList.add('drag-over');
        });
        uploadCard.addEventListener('dragleave', () => {
            uploadCard.classList.remove('drag-over');
        });
        uploadCard.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadCard.classList.remove('drag-over');

            // Check if files exist in the dataTransfer object

            // 1. The e (Event Object)

            // When a user drops a file, the browser creates a "Drop Event" (represented here by e). This object contains everything the browser knows about that action—where the mouse was, what elements were involved, and, most importantly, what data was carried.

            // 2. dataTransfer

            // This is a specific property of drag-and-drop events. It acts as a "container" for the data being moved. Since you are dragging files from your computer's file explorer into the browser, the browser populates this dataTransfer object with a list of those files.

            // 3. files (The FileList)

            // The files property is a FileList object. It is an "array-like" collection. Even if a user drops only one file, the browser always puts it into this list.

            // 4. Why the [0]?

            // This is the index. Since your current tool is designed to analyze one file at a time, you are telling the script: "I don't care if the user highlighted ten files and dropped them; just take the very first one in the list and process that."

            // [0] = The first file dropped.
            // [1] = The second file (if applicable), and so on.

            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                const file = e.dataTransfer.files[0];
                handleFileSelected(file);
            }
        });
 
        fileInput.addEventListener('change', () => {
            if (fileInput.files[0]) handleFileSelected(fileInput.files[0]);
        });
 
        function handleFileSelected(file) {
            selectedFile = file;
            const ext = file.name.includes('.') ? '.' + file.name.split('.').pop().toLowerCase() : 'none';
            const size = file.size > 1024 * 1024
                ? (file.size / (1024 * 1024)).toFixed(2) + ' MB'
                : (file.size / 1024).toFixed(1) + ' KB';
 
            document.getElementById('infoFileName').textContent = file.name;
            document.getElementById('infoFileSize').textContent = size;
            document.getElementById('infoFileExt').textContent = ext;
            document.getElementById('infoStatus').textContent = 'READY';
            document.getElementById('infoStatus').className = 'info-value status-ready';
 
            fileInfoStrip.classList.add('visible'); // .file-info-strip.visible CSS code written in styles.css
            btnWrapper.classList.add('visible');
            resultPanel.classList.remove('visible');
            uploadCardOne.style.display = 'block';
        }
 
        analyzeBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
 
            analyzeBtn.classList.add('loading');
            analyzeBtn.querySelector('.btn-text').textContent = 'SCANNING...';
            document.getElementById('infoStatus').textContent = 'SCANNING';
            document.getElementById('infoStatus').className = 'info-value status-scanning';
 
            // These two lines below are responsible for "packaging" the binary file so it can be transmitted from the browser to our FastAPI backend.

            const formData = new FormData(); // This creates a new instance of the FormData object. Think of this as a digital envelope. While a standard JSON object is great for sending text, FormData is the specialized standard for sending multipart/form-data. This is the specific format required by web servers to handle binary data like images, documents, or executables.

            formData.append('file', selectedFile); // This line "labels" the data inside the envelope. The first argument, 'file', is the key or field name. This is critical because it must exactly match the parameter name your FastAPI backend expects (in your Python code, you defined async def analyze_file(file: UploadFile), so the key must be 'file').

            // The second argument, selectedFile, is the actual File object (the blob of data) that you want to send.
 
            // One major benefit of using FormData with the fetch API is that the browser is smart enough to automatically set the correct Content-Type header, including the necessary "boundary" string that tells the server where one part of the data ends and the next begins. You should avoid setting the Content-Type header manually when using FormData, as it often leads to server-side parsing errors.

            try {
                const response = await fetch('http://localhost:8000/analyze_file/', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                showResult(result);
            } catch (err) {
                // Show a demo result if backend not running (for UI testing)
                showResult({
                    file_name: selectedFile.name,
                    true_type: "Demo Mode — Start FastAPI backend",
                    extension: '.' + selectedFile.name.split('.').pop(),
                    match: null,
                    message: "Could not reach http://localhost:8000 — run: uvicorn file_signature_analyzer:app --reload"
                });
            }
 
            analyzeBtn.classList.remove('loading');
            analyzeBtn.querySelector('.btn-text').textContent = 'ANALYZE SIGNATURE';
        });
 
        function showResult(result) {
            // Hide all result bodies
            document.getElementById('resultMatch').style.display = 'none';
            document.getElementById('resultAlert').style.display = 'none';
            document.getElementById('resultUnknown').style.display = 'none';

            uploadCardTwo.style.display = 'block';
 
            if (result.match === true) {
                document.getElementById('resultMatch').style.display = 'flex';
                document.getElementById('infoStatus').textContent = 'VERIFIED';
                document.getElementById('infoStatus').className = 'info-value status-safe';
            } else if (result.match === false) {
                document.getElementById('resultAlert').style.display = 'flex';
                document.getElementById('infoStatus').textContent = 'ALERT';
                document.getElementById('infoStatus').className = 'info-value status-alert';
            } else {
                document.getElementById('resultUnknown').style.display = 'flex';
                document.getElementById('infoStatus').textContent = 'UNKNOWN';
                document.getElementById('infoStatus').className = 'info-value status-warn';
            }
 
            document.getElementById('detailFileName').textContent = result.file_name || selectedFile.name;
            document.getElementById('detailTrueType').textContent = result.true_type || '—';
            document.getElementById('detailExtension').textContent = result.extension || '—';
            document.getElementById('detailMessage').textContent = result.message || '—';
            document.getElementById('resultDetails').style.display = result.true_type ? 'block' : 'none';
            document.getElementById('resultTimestamp').textContent = new Date().toLocaleTimeString();
 
            resultPanel.classList.add('visible');
        }