/**
 * SkillGap AI Pro - Charts Module
 * Uses Chart.js for data visualization
 */

// Chart instances
let chartInstances = {};

// Color palette
const COLORS = {
    primary: '#4F46E5',
    primaryLight: '#818CF8',
    success: '#22C55E',
    danger: '#EF4444',
    warning: '#F59E0B',
    info: '#3B82F6',
    purple: '#8B5CF6',
    gray: '#94A3B8',
    
    palette: [
        '#4F46E5', '#22C55E', '#F59E0B', '#EF4444', '#3B82F6',
        '#8B5CF6', '#EC4899', '#14B8A6', '#F97316', '#6366F1'
    ]
};

// ============================================================
// Render Charts
// ============================================================
// ============================================================
// Render Charts - FIXED
// ============================================================
function renderCharts(data) {
    if (!data) {
        console.warn('No chart data provided');
        return;
    }
    
    console.log('Rendering charts with data:', data);
    
    // Destroy all existing charts first
    Object.keys(chartInstances).forEach(key => {
        if (chartInstances[key]) {
            try {
                chartInstances[key].destroy();
            } catch (e) {
                console.warn('Error destroying chart:', key, e);
            }
            delete chartInstances[key];
        }
    });
    
    // Render each chart
    try {
        if (data.match_history && data.match_history.length > 0) {
            renderMatchHistory(data.match_history);
        }
        
        if (data.resume_score_trend && data.resume_score_trend.length > 0) {
            renderResumeTrend(data.resume_score_trend);
        }
        
        if (data.job_popularity && data.job_popularity.length > 0) {
            renderJobPopularity(data.job_popularity);
        }
        
        if (data.skill_distribution && data.skill_distribution.length > 0) {
            renderSkillDistribution(data.skill_distribution);
        }
        
        if (data.missing_skills && data.missing_skills.length > 0) {
            renderMissingSkills(data.missing_skills);
        }
        
        if (data.ats_distribution && data.ats_distribution.length > 0) {
            renderATSDistribution(data.ats_distribution);
        }
        
        console.log('All charts rendered successfully!');
    } catch (error) {
        console.error('Error rendering charts:', error);
    }
}

// ============================================================
// Match History Chart
// ============================================================
// ============================================================
// Match History Chart - FIXED
// ============================================================
function renderMatchHistory(data) {
    const canvas = document.getElementById('matchHistoryChart');
    if (!canvas) return;
    
    // Destroy existing chart
    if (chartInstances.matchHistory) {
        chartInstances.matchHistory.destroy();
        delete chartInstances.matchHistory;
    }
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => new Date(d.date).toLocaleDateString());
    const matchScores = data.map(d => d.match_score);
    const atsScores = data.map(d => d.ats_score);
    
    chartInstances.matchHistory = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Match Score',
                    data: matchScores,
                    borderColor: COLORS.primary,
                    backgroundColor: COLORS.primaryLight + '33',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3
                },
                {
                    label: 'ATS Score',
                    data: atsScores,
                    borderColor: COLORS.info,
                    backgroundColor: COLORS.info + '33',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        font: { size: 11 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// ============================================================
// Resume Score Trend Chart - FIXED
// ============================================================
function renderResumeTrend(data) {
    const canvas = document.getElementById('resumeTrendChart');
    if (!canvas) return;
    
    if (chartInstances.resumeTrend) {
        chartInstances.resumeTrend.destroy();
        delete chartInstances.resumeTrend;
    }
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => new Date(d.date).toLocaleDateString());
    const matchScores = data.map(d => d.avg_match_score);
    const atsScores = data.map(d => d.avg_ats_score);
    
    chartInstances.resumeTrend = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Avg Match Score',
                    data: matchScores,
                    backgroundColor: COLORS.primary,
                    borderRadius: 4
                },
                {
                    label: 'Avg ATS Score',
                    data: atsScores,
                    backgroundColor: COLORS.info,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        font: { size: 11 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// ============================================================
// Job Popularity Chart - FIXED
// ============================================================
function renderJobPopularity(data) {
    const canvas = document.getElementById('jobPopularityChart');
    if (!canvas) return;
    
    if (chartInstances.jobPopularity) {
        chartInstances.jobPopularity.destroy();
        delete chartInstances.jobPopularity;
    }
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => d.job);
    const counts = data.map(d => d.count);
    
    chartInstances.jobPopularity = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: COLORS.palette.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 12,
                        padding: 10,
                        font: { size: 10 }
                    }
                }
            }
        }
    });
}

// ============================================================
// Missing Skills Chart - FIXED
// ============================================================
function renderMissingSkills(data) {
    const canvas = document.getElementById('missingSkillsChart');
    if (!canvas) return;
    
    if (chartInstances.missingSkills) {
        chartInstances.missingSkills.destroy();
        delete chartInstances.missingSkills;
    }
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => d.skill);
    const counts = data.map(d => d.count);
    
    chartInstances.missingSkills = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Missing Skills',
                data: counts,
                backgroundColor: COLORS.danger,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// ============================================================
// ATS Distribution Chart - FIXED
// ============================================================
function renderATSDistribution(data) {
    const canvas = document.getElementById('atsDistributionChart');
    if (!canvas) return;
    
    if (chartInstances.atsDistribution) {
        chartInstances.atsDistribution.destroy();
        delete chartInstances.atsDistribution;
    }
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => d.range);
    const counts = data.map(d => d.count);
    
    const colors = {
        'Excellent (80-100)': COLORS.success,
        'Good (60-79)': COLORS.info,
        'Fair (40-59)': COLORS.warning,
        'Poor (0-39)': COLORS.danger
    };
    
    chartInstances.atsDistribution = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: labels.map(l => colors[l] || COLORS.gray),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 10,
                        font: { size: 10 }
                    }
                }
            }
        }
    });
}
// ============================================================
// Resume Score Trend Chart
// ============================================================
function renderResumeTrend(data) {
    const canvas = document.getElementById('resumeTrendChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => new Date(d.date).toLocaleDateString());
    const matchScores = data.map(d => d.avg_match_score);
    const atsScores = data.map(d => d.avg_ats_score);
    
    chartInstances.resumeTrend = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Avg Match Score',
                    data: matchScores,
                    backgroundColor: COLORS.primary,
                    borderRadius: 4
                },
                {
                    label: 'Avg ATS Score',
                    data: atsScores,
                    backgroundColor: COLORS.info,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        font: { size: 11 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// ============================================================
// Job Popularity Chart
// ============================================================
function renderJobPopularity(data) {
    const canvas = document.getElementById('jobPopularityChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => d.job);
    const counts = data.map(d => d.count);
    
    chartInstances.jobPopularity = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: COLORS.palette.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 12,
                        padding: 10,
                        font: { size: 10 }
                    }
                }
            }
        }
    });
}

// ============================================================
// Skill Distribution Chart
// ============================================================
// ============================================================
// Skill Distribution Chart - FIXED for Chart.js v4
// ============================================================
function renderSkillDistribution(data) {
    const canvas = document.getElementById('skillDistributionChart');
    if (!canvas) return;
    
    // Destroy existing chart instance
    if (chartInstances.skillDistribution) {
        chartInstances.skillDistribution.destroy();
        delete chartInstances.skillDistribution;
    }
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => d.skill);
    const counts = data.map(d => d.count);
    
    // Use 'bar' with indexAxis: 'y' instead of 'horizontalBar'
    chartInstances.skillDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Skill Count',
                data: counts,
                backgroundColor: COLORS.purple,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',  // This makes it horizontal in Chart.js v4
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    grid: { display: false }
                },
                x: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                }
            }
        }
    });
}

// ============================================================
// Missing Skills Chart
// ============================================================
function renderMissingSkills(data) {
    const canvas = document.getElementById('missingSkillsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => d.skill);
    const counts = data.map(d => d.count);
    
    chartInstances.missingSkills = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Missing Skills',
                data: counts,
                backgroundColor: COLORS.danger,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// ============================================================
// ATS Distribution Chart
// ============================================================
function renderATSDistribution(data) {
    const canvas = document.getElementById('atsDistributionChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const labels = data.map(d => d.range);
    const counts = data.map(d => d.count);
    
    const colors = {
        'Excellent (80-100)': COLORS.success,
        'Good (60-79)': COLORS.info,
        'Fair (40-59)': COLORS.warning,
        'Poor (0-39)': COLORS.danger
    };
    
    chartInstances.atsDistribution = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: labels.map(l => colors[l] || COLORS.gray),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 10,
                        font: { size: 10 }
                    }
                }
            }
        }
    });
}

// ============================================================
// Chart Utility Functions
// ============================================================
function getChartColors(count) {
    const colors = [];
    const palette = COLORS.palette;
    for (let i = 0; i < count; i++) {
        colors.push(palette[i % palette.length]);
    }
    return colors;
}

function updateChart(chartId, newData) {
    if (chartInstances[chartId]) {
        chartInstances[chartId].data = newData;
        chartInstances[chartId].update();
    }
}

// Make chart functions globally accessible
window.renderCharts = renderCharts;
window.updateChart = updateChart;
window.getChartColors = getChartColors;