/**
 * SkillGap AI Pro - Dashboard Module
 */

// ============================================================
// Initialize Dashboard
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    // Dashboard is loaded by script.js
    // This file contains additional dashboard utilities
});

// ============================================================
// Refresh Dashboard
// ============================================================
function refreshDashboard() {
    loadDashboard();
    showToast('Dashboard refreshed', 'info');
}

// ============================================================
// Export Dashboard Data
// ============================================================
function exportDashboardData() {
    // Collect dashboard data for export
    const stats = {
        totalAnalyses: document.getElementById('totalAnalyses').textContent,
        avgMatchScore: document.getElementById('avgMatchScore').textContent,
        highestScore: document.getElementById('highestScore').textContent,
        avgATSScore: document.getElementById('avgATSScore').textContent,
        totalResumes: document.getElementById('totalResumes').textContent,
        mostSelectedJob: document.getElementById('mostSelectedJob').textContent
    };
    
    const dataStr = JSON.stringify(stats, null, 2);
    const blob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `dashboard-stats-${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showToast('Dashboard data exported!', 'success');
}

// Make functions globally accessible
window.refreshDashboard = refreshDashboard;
window.exportDashboardData = exportDashboardData;