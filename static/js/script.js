/**
 * SkillGap AI Pro - Main Application Script
 */

// ============================================================
// Configuration
// ============================================================
const API_BASE = '/api';
const APP = {
    currentPage: 'dashboard',
    resumes: [],
    jobs: [],
    analyses: [],
    favorites: [],
    currentResumeId: null,
    currentAnalysisId: null
};

// ============================================================
// Utility Functions
// ============================================================
function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toastContainer');
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span>${message}</span>
    `;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('hide');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function showLoading(show = true) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatPercentage(value) {
    return Math.round(value || 0) + '%';
}

function getStatusColor(score) {
    if (score >= 80) return 'success';
    if (score >= 60) return 'info';
    if (score >= 40) return 'warning';
    return 'danger';
}

// ============================================================
// API Calls
// ============================================================
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json'
        },
        ...options
    };
    
    try {
        showLoading(true);
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API request failed');
        }
        
        return data;
    } catch (error) {
        showToast(error.message, 'error');
        throw error;
    } finally {
        showLoading(false);
    }
}

async function fetchJobs() {
    const data = await apiCall('/jobs');
    APP.jobs = data;
    return data;
}

async function fetchResumes() {
    return APP.resumes;
}

async function fetchHistory() {
    const data = await apiCall('/history');
    APP.analyses = data;
    return data;
}

async function fetchFavorites() {
    const data = await apiCall('/favorites');
    APP.favorites = data;
    return data;
}

async function fetchStats() {
    return await apiCall('/stats');
}

async function fetchChartData() {
    return await apiCall('/charts');
}

async function uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE}/upload-resume`, {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Upload failed');
    }
    
    return await response.json();
}

async function analyzeResume(resumeId, jobTitle) {
    return await apiCall('/analyze', {
        method: 'POST',
        body: JSON.stringify({ resume_id: resumeId, desired_job: jobTitle })
    });
}

async function getRecommendations(resumeId) {
    return await apiCall('/job-ranking', {
        method: 'POST',
        body: JSON.stringify({ resume_id: resumeId })
    });
}

async function getRoadmap(jobTitle) {
    return await apiCall(`/roadmap/${encodeURIComponent(jobTitle)}`);
}

async function generateRoadmap(resumeId, jobTitle) {
    return await apiCall('/roadmap/generate', {
        method: 'POST',
        body: JSON.stringify({ resume_id: resumeId, job_title: jobTitle })
    });
}

async function getSkillGap(resumeId, jobTitle) {
    return await apiCall(`/skill-gap/${resumeId}?job=${encodeURIComponent(jobTitle)}`);
}

async function addFavorite(jobTitle, jobId) {
    return await apiCall('/favorites', {
        method: 'POST',
        body: JSON.stringify({ job_title: jobTitle, job_id: jobId })
    });
}

async function deleteFavorite(id) {
    return await apiCall(`/favorites/${id}`, {
        method: 'DELETE'
    });
}

async function deleteHistory(id) {
    return await apiCall(`/history/${id}`, {
        method: 'DELETE'
    });
}

async function generateReport(resumeId, jobTitle) {
    return await apiCall('/generate-report', {
        method: 'POST',
        body: JSON.stringify({ resume_id: resumeId, job_title: jobTitle })
    });
}

// ============================================================
// Navigation
// ============================================================
function navigateTo(page) {
    // Update sidebar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.dataset.page === page);
    });
    
    // Update page sections
    document.querySelectorAll('.page-section').forEach(section => {
        section.classList.toggle('active', section.id === `page-${page}`);
    });
    
    // Update page title
    const titles = {
        dashboard: 'Dashboard',
        upload: 'Upload Resume',
        analyzer: 'Skill Analyzer',
        career: 'Career Path',
        history: 'History',
        favorites: 'Favorites',
        reports: 'Reports'
    };
    document.getElementById('pageTitle').textContent = titles[page] || page;
    
    APP.currentPage = page;
    
    // Load page-specific data
    switch(page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'history':
            loadHistory();
            break;
        case 'favorites':
            loadFavorites();
            break;
        case 'analyzer':
            populateJobSelects();
            populateResumeSelects();
            break;
        case 'career':
            populateCareerJobSelect();
            populateCareerResumeSelect();  // ← ADDED
            break;
        case 'reports':
            populateReportResumeSelect();
            break;
    }
}

// ============================================================
// Event Listeners
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            navigateTo(this.dataset.page);
        });
    });
    
    // Menu toggle for mobile
    document.getElementById('menuToggle').addEventListener('click', function() {
        document.getElementById('sidebar').classList.toggle('open');
    });
    
    // Theme toggle
    document.getElementById('themeToggle').addEventListener('click', function() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        html.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');
        this.innerHTML = currentTheme === 'dark' ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
        showToast(`Switched to ${currentTheme === 'dark' ? 'Light' : 'Dark'} mode`, 'info');
    });
    
    // Set current date
    document.getElementById('currentDate').textContent = new Date().toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    // Initialize
    loadDashboard();
    fetchJobs().then(() => {
        populateJobSelects();
        populateCareerJobSelect();
        populateCareerResumeSelect();  // ← ADDED
        populateReportResumeSelect();
    });
});

// ============================================================
// Dashboard Functions
// ============================================================
async function loadDashboard() {
    try {
        const [stats, chartData] = await Promise.all([
            fetchStats(),
            fetchChartData()
        ]);
        
        // Update stats
        document.getElementById('totalAnalyses').textContent = stats.total_analyses || 0;
        document.getElementById('avgMatchScore').textContent = formatPercentage(stats.avg_match_score);
        document.getElementById('highestScore').textContent = formatPercentage(stats.highest_score);
        document.getElementById('avgATSScore').textContent = Math.round(stats.avg_ats_score || 0);
        document.getElementById('totalResumes').textContent = stats.total_resumes || 0;
        document.getElementById('mostSelectedJob').textContent = stats.most_selected_job || 'N/A';
        
        // Update recent analyses
        if (stats.recent_analyses && stats.recent_analyses.length > 0) {
            const tbody = document.getElementById('recentTableBody');
            tbody.innerHTML = stats.recent_analyses.map(a => `
                <tr>
                    <td>${formatDate(a.created_at)}</td>
                    <td>${a.desired_job || 'N/A'}</td>
                    <td><span class="badge ${getStatusColor(a.match_score)}">${formatPercentage(a.match_score)}</span></td>
                    <td>${Math.round(a.ats_score || 0)}</td>
                </tr>
            `).join('');
        }
        
        // Render charts
        if (typeof renderCharts === 'function') {
            renderCharts(chartData);
        }
        
    } catch (error) {
        console.error('Failed to load dashboard:', error);
        showToast('Failed to load dashboard data', 'error');
    }
}

// ============================================================
// History Functions
// ============================================================
async function loadHistory() {
    try {
        const history = await fetchHistory();
        const tbody = document.getElementById('historyTableBody');
        
        if (history.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No history found</td></tr>';
            return;
        }
        
        tbody.innerHTML = history.map(h => `
            <tr>
                <td>${formatDate(h.created_at)}</td>
                <td>${h.desired_job || 'N/A'}</td>
                <td><span class="badge ${getStatusColor(h.match_score)}">${formatPercentage(h.match_score)}</span></td>
                <td>${Math.round(h.ats_score || 0)}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="deleteHistoryItem(${h.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
        
        // Setup search
        document.getElementById('historySearch').addEventListener('input', function() {
            const search = this.value.toLowerCase();
            const rows = tbody.querySelectorAll('tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(search) ? '' : 'none';
            });
        });
        
    } catch (error) {
        console.error('Failed to load history:', error);
        showToast('Failed to load history', 'error');
    }
}

async function deleteHistoryItem(id) {
    if (!confirm('Delete this analysis?')) return;
    try {
        await deleteHistory(id);
        showToast('Analysis deleted', 'success');
        loadHistory();
        loadDashboard();
    } catch (error) {
        console.error('Failed to delete:', error);
        showToast('Failed to delete analysis', 'error');
    }
}

// ============================================================
// Favorites Functions
// ============================================================
async function loadFavorites() {
    try {
        const favorites = await fetchFavorites();
        const grid = document.getElementById('favoritesGrid');
        
        if (favorites.length === 0) {
            grid.innerHTML = '<p class="text-center">No favorites yet</p>';
            return;
        }
        
        grid.innerHTML = favorites.map(f => `
            <div class="favorite-card">
                <div>
                    <div class="job-title">${f.job_title}</div>
                    <div class="fav-date">Added: ${formatDate(f.created_at)}</div>
                </div>
                <div class="fav-actions">
                    <button onclick="removeFavorite(${f.id})" title="Remove">
                        <i class="fas fa-star" style="color: #F59E0B;"></i>
                    </button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Failed to load favorites:', error);
        showToast('Failed to load favorites', 'error');
    }
}

async function removeFavorite(id) {
    try {
        await deleteFavorite(id);
        showToast('Removed from favorites', 'success');
        loadFavorites();
    } catch (error) {
        console.error('Failed to remove:', error);
        showToast('Failed to remove favorite', 'error');
    }
}

// ============================================================
// Upload Functions
// ============================================================
// Upload is handled in upload.js

// ============================================================
// Analyzer Functions
// ============================================================
function populateJobSelects() {
    const selects = ['jobSelect', 'careerJobSelect'];
    selects.forEach(id => {
        const select = document.getElementById(id);
        if (!select) return;
        
        const currentValue = select.value;
        select.innerHTML = '<option value="">Choose a job...</option>';
        
        APP.jobs.forEach(job => {
            const option = document.createElement('option');
            option.value = job.title;
            option.textContent = job.title;
            select.appendChild(option);
        });
        
        if (currentValue) select.value = currentValue;
    });
}

function populateResumeSelects() {
    const select = document.getElementById('resumeSelect');
    if (!select) return;
    
    const currentValue = select.value;
    select.innerHTML = '<option value="">Choose a resume...</option>';
    
    if (APP.resumes && APP.resumes.length > 0) {
        APP.resumes.forEach(resume => {
            const option = document.createElement('option');
            option.value = resume.id;
            option.textContent = resume.name || `Resume #${resume.id}`;
            select.appendChild(option);
        });
    }
    
    if (currentValue) select.value = currentValue;
}

// ============================================================
// Career Path Functions
// ============================================================
function populateCareerResumeSelect() {
    const select = document.getElementById('careerResumeSelect');
    if (!select) return;
    
    const currentValue = select.value;
    select.innerHTML = '<option value="">Choose a resume...</option>';
    
    if (APP.resumes && APP.resumes.length > 0) {
        APP.resumes.forEach(resume => {
            const option = document.createElement('option');
            option.value = resume.id;
            option.textContent = resume.name || `Resume #${resume.id}`;
            select.appendChild(option);
        });
    }
    
    if (currentValue) select.value = currentValue;
}

function populateCareerJobSelect() {
    const select = document.getElementById('careerJobSelect');
    if (!select) return;
    
    const currentValue = select.value;
    select.innerHTML = '<option value="">Choose a job...</option>';
    
    APP.jobs.forEach(job => {
        const option = document.createElement('option');
        option.value = job.title;
        option.textContent = job.title;
        select.appendChild(option);
    });
    
    if (currentValue) select.value = currentValue;
}

async function showCareerRoadmap() {
    const jobTitle = document.getElementById('careerJobSelect').value;
    const resumeId = document.getElementById('careerResumeSelect').value;
    
    if (!jobTitle) {
        showToast('Please select a job', 'warning');
        return;
    }
    
    if (!resumeId) {
        showToast('Please select a resume', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        // Use the generate endpoint
        const roadmap = await generateRoadmap(resumeId, jobTitle);
        
        const resultsDiv = document.getElementById('careerResults');
        resultsDiv.style.display = 'block';
        
        // Update summary
        document.getElementById('careerGap').textContent = formatPercentage(roadmap.gap_percentage || 0);
        document.getElementById('careerSkillsCount').textContent = (roadmap.skill_gaps || []).length;
        document.getElementById('careerWeeks').textContent = roadmap.estimated_total_weeks || 0;
        
        // Render roadmap
        const roadmapDiv = document.getElementById('roadmapContent');
        if (roadmap.weeks && roadmap.weeks.length > 0) {
            roadmapDiv.innerHTML = roadmap.weeks.map(week => `
                <div class="roadmap-item">
                    <div class="week">${week.week}</div>
                    <div class="focus">${week.focus} - ${week.description || ''}</div>
                    ${(week.topics || []).map(t => `
                        <div class="topic">
                            <i class="fas fa-check-circle"></i>
                            <span><strong>${t.skill || 'Skill'}:</strong> ${t.topic}</span>
                            ${t.priority ? `<span class="badge ${t.priority === 'High' ? 'danger' : 'info'}">${t.priority}</span>` : ''}
                        </div>
                    `).join('')}
                </div>
            `).join('');
        } else {
            roadmapDiv.innerHTML = '<p>No roadmap items available. Great job on your skills!</p>';
        }
        
        // Get skill gaps
        const gapData = await getSkillGap(resumeId, jobTitle);
        const gapList = document.getElementById('skillGapList');
        
        if (gapData.missing_skills && gapData.missing_skills.length > 0) {
            const recommendations = gapData.skill_recommendations || [];
            gapList.innerHTML = recommendations.map(rec => `
                <div class="skill-gap-item">
                    <span class="skill-name">${rec.skill}</span>
                    <span class="skill-difficulty">${rec.difficulty} · ${rec.estimated_hours}h</span>
                    <span class="skill-priority ${rec.priority.toLowerCase()}">${rec.priority}</span>
                </div>
            `).join('');
        } else {
            gapList.innerHTML = '<p class="text-muted">No skill gaps found!</p>';
        }
        
        showToast('Roadmap generated!', 'success');
        
    } catch (error) {
        console.error('Failed to get roadmap:', error);
        showToast('Failed to generate roadmap: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// ============================================================
// Reports Functions
// ============================================================
function populateReportResumeSelect() {
    const select = document.getElementById('reportResumeSelect');
    if (!select) return;
    
    const currentValue = select.value;
    select.innerHTML = '<option value="">Choose a resume...</option>';
    
    if (APP.resumes && APP.resumes.length > 0) {
        APP.resumes.forEach(resume => {
            const option = document.createElement('option');
            option.value = resume.id;
            option.textContent = resume.name || `Resume #${resume.id}`;
            select.appendChild(option);
        });
    }
    
    if (currentValue) select.value = currentValue;
}

async function generateReportAction() {
    const resumeId = document.getElementById('reportResumeSelect').value;
    const jobTitle = document.getElementById('jobSelect')?.value || '';
    
    if (!resumeId) {
        showToast('Please select a resume', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        const result = await generateReport(resumeId, jobTitle);
        
        const resultDiv = document.getElementById('reportResult');
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="alert success">
                <i class="fas fa-check-circle"></i>
                <div>
                    <strong>Report Generated!</strong>
                    <p><a href="${result.report_url}" target="_blank" class="btn btn-primary" style="margin-top:0.5rem;">
                        <i class="fas fa-download"></i> Download Report
                    </a></p>
                </div>
            </div>
        `;
        
        showToast('Report generated successfully!', 'success');
        
    } catch (error) {
        console.error('Failed to generate report:', error);
        showToast('Failed to generate report', 'error');
    } finally {
        showLoading(false);
    }
}

// ============================================================
// Analyzer Analysis Function (moved after career functions)
// ============================================================
async function performAnalysis() {
    const resumeId = document.getElementById('resumeSelect').value;
    const jobTitle = document.getElementById('jobSelect').value;
    
    if (!resumeId) {
        showToast('Please select a resume', 'warning');
        return;
    }
    
    if (!jobTitle) {
        showToast('Please select a job', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        const result = await analyzeResume(resumeId, jobTitle);
        
        // Show results
        const resultsDiv = document.getElementById('analysisResults');
        resultsDiv.style.display = 'block';
        
        // Update match percentage
        document.getElementById('matchPercentage').textContent = formatPercentage(result.match_percentage);
        document.getElementById('matchProgressFill').style.width = `${result.match_percentage}%`;
        
        // Update ATS score
        document.getElementById('atsScore').textContent = Math.round(result.ats_score || 0);
        document.getElementById('atsProgressFill').style.width = `${result.ats_score || 0}%`;
        
        // Update confidence
        document.getElementById('confidenceScore').textContent = formatPercentage(result.confidence_score);
        document.getElementById('confidenceProgressFill').style.width = `${result.confidence_score}%`;
        
        // Update similarity
        document.getElementById('similarityScore').textContent = formatPercentage(result.similarity_score);
        document.getElementById('similarityProgressFill').style.width = `${result.similarity_score}%`;
        
        // Update skills
        const matched = result.matched_skills || [];
        const missing = result.missing_skills || [];
        const extra = result.extra_skills || [];
        
        document.getElementById('matchedCount').textContent = matched.length;
        document.getElementById('missingCount').textContent = missing.length;
        document.getElementById('extraCount').textContent = extra.length;
        
        document.getElementById('matchedSkills').innerHTML = matched.map(s => 
            `<span class="skill-tag matched">${s}</span>`
        ).join('') || '<span class="text-muted">No matched skills</span>';
        
        document.getElementById('missingSkills').innerHTML = missing.map(s => 
            `<span class="skill-tag missing">${s}</span>`
        ).join('') || '<span class="text-muted">No missing skills</span>';
        
        document.getElementById('extraSkills').innerHTML = extra.map(s => 
            `<span class="skill-tag extra">${s}</span>`
        ).join('') || '<span class="text-muted">No extra skills</span>';
        
        showToast('Analysis complete!', 'success');
        
    } catch (error) {
        console.error('Analysis failed:', error);
        showToast('Analysis failed: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// ============================================================
// Global Event Bindings
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    // Analyze button
    document.getElementById('analyzeBtn')?.addEventListener('click', performAnalysis);
    
    // Career analyze button
    document.getElementById('careerAnalyzeBtn')?.addEventListener('click', showCareerRoadmap);
    
    // Generate report button
    document.getElementById('generateReportBtn')?.addEventListener('click', generateReportAction);
    
    // Clear history button
    document.getElementById('clearHistoryBtn')?.addEventListener('click', async function() {
        if (!confirm('Delete all analysis history?')) return;
        showToast('History cleared', 'success');
        loadHistory();
        loadDashboard();
    });
});

// Expose functions to global scope
window.deleteHistoryItem = deleteHistoryItem;
window.removeFavorite = removeFavorite;
window.navigateTo = navigateTo;
window.performAnalysis = performAnalysis;
window.showCareerRoadmap = showCareerRoadmap;
window.generateReportAction = generateReportAction;