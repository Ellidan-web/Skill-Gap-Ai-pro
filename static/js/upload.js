/**
 * SkillGap AI Pro - Resume Upload Module
 */

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');
    const uploadStatus = document.getElementById('uploadStatus');
    const resultDiv = document.getElementById('uploadResult');
    
    // Click to upload
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            handleFileUpload(this.files[0]);
        }
    });
});

async function handleFileUpload(file) {
    // Validate file
    const validExtensions = ['pdf', 'docx', 'txt'];
    const extension = file.name.split('.').pop().toLowerCase();
    
    if (!validExtensions.includes(extension)) {
        showToast('Invalid file type. Please upload PDF, DOCX, or TXT.', 'error');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        showToast('File too large. Maximum size is 16MB.', 'error');
        return;
    }
    
    // Show progress
    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');
    const uploadStatus = document.getElementById('uploadStatus');
    const resultDiv = document.getElementById('uploadResult');
    
    progressDiv.style.display = 'block';
    resultDiv.style.display = 'none';
    uploadStatus.textContent = 'Uploading...';
    progressFill.style.width = '0%';
    
    try {
        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 10;
            if (progress <= 90) {
                progressFill.style.width = progress + '%';
            }
        }, 200);
        
        // Upload file
        const result = await uploadResume(file);
        
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        uploadStatus.textContent = 'Processing...';
        
        // Wait a moment for processing
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Show result
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="upload-success">
                <i class="fas fa-check-circle" style="color: var(--success); font-size: 2rem;"></i>
                <h3>Resume Uploaded Successfully!</h3>
                <p><strong>File:</strong> ${result.data.filename}</p>
                <p><strong>Candidate:</strong> ${result.data.candidate_name || 'N/A'}</p>
                <p><strong>Email:</strong> ${result.data.email || 'N/A'}</p>
                <p><strong>Skills Found:</strong> ${result.data.skills.length}</p>
                <div class="skill-tags" style="margin-top:0.5rem;">
                    ${result.data.skills.slice(0, 10).map(s => 
                        `<span class="skill-tag">${s}</span>`
                    ).join('')}
                    ${result.data.skills.length > 10 ? `<span class="skill-tag">+${result.data.skills.length - 10} more</span>` : ''}
                </div>
                <div style="margin-top:1rem;">
                    <button class="btn btn-primary" onclick="navigateTo('analyzer')">
                        <i class="fas fa-search"></i> Analyze Resume
                    </button>
                </div>
            </div>
        `;
        
        // Store resume ID for analysis
        APP.currentResumeId = result.resume_id;
        
        // Add to resume list
        const resumeName = result.data.candidate_name || `Resume #${result.resume_id}`;
        APP.resumes.push({
            id: result.resume_id,
            name: resumeName,
            filename: result.data.filename,
            skills: result.data.skills || []
        });
        
        // Update ALL resume dropdowns - THIS IS THE FIX
        populateResumeSelects();
        populateCareerResumeSelect();  // ← ADD THIS LINE
        populateReportResumeSelect();
        
        showToast(`Resume "${resumeName}" uploaded successfully!`, 'success');
        
    } catch (error) {
        console.error('Upload failed:', error);
        const progressFill = document.getElementById('progressFill');
        const uploadStatus = document.getElementById('uploadStatus');
        const resultDiv = document.getElementById('uploadResult');
        
        progressFill.style.width = '0%';
        uploadStatus.textContent = 'Upload failed';
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="upload-error">
                <i class="fas fa-exclamation-circle" style="color: var(--danger); font-size: 2rem;"></i>
                <h3>Upload Failed</h3>
                <p>${error.message || 'An error occurred during upload.'}</p>
                <button class="btn btn-primary" onclick="location.reload()">Try Again</button>
            </div>
        `;
        showToast('Upload failed: ' + error.message, 'error');
    }
}