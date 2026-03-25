// Salary Comparison Chart Generator - Enhanced for DSE Students & Parents
// Uses Chart.js with parent-friendly terminology and interactive features

let salaryData = [];
let filteredData = [];
let currentExperience = 'junior'; // Default to fresh graduates

// DSE Subject to Major Mapping
const dseSubjectMapping = {
    'ICT': ['cs', 'ie', 'game', 'math'],
    'M1/M2': ['cs', 'ie', 'math', 'finance', 'eng', 'data-analyst', 'data-scientist', 'ai-ml-engineer'],
    'Physics': ['cs', 'ie', 'eng', 'math', 'ai-ml-engineer', 'devops'],
    'Chemistry': ['health', 'math', 'data-scientist'],
    'Biology': ['health', 'math', 'data-scientist'],
    'BAFS': ['finance', 'accounting', 'business', 'marketing'],
    'Economics': ['finance', 'business', 'marketing', 'math'],
    'Chinese': ['edu', 'media', 'social-worker'],
    'English': ['edu', 'media', 'business', 'marketing'],
    'History': ['edu', 'media', 'social-worker'],
    'Geography': ['edu', 'social-worker'],
    'Liberal Studies': ['edu', 'social-worker', 'media', 'business']
};

// Major to Career Mapping
const majorToCareer = {
    'cs': ['software-dev', 'web-dev', 'mobile-dev', 'data-analyst', 'ai-ml-engineer'],
    'ie': ['it-support', 'devops', 'security', 'software-dev'],
    'game': ['game-dev', 'indie-game-dev', 'design'],
    'math': ['data-analyst', 'data-scientist', 'ai-ml-engineer', 'finance', 'education'],
    'finance': ['finance', 'accounting', 'marketing'],
    'eng': ['engineering', 'software-dev', 'ai-ml-engineer'],
    'edu': ['education', 'social-worker', 'media'],
    'health': ['healthcare']
};

// Plain language labels (parent-friendly)
const plainLabels = {
    'bottom': '入行起薪',
    'lower': '初級水平',
    'median': '累積經驗後',
    'upper': '資深水平',
    'top': '晉升管理層後'
};

// Prospect badges
const prospectBadges = {
    9: { text: '極高需求', color: '#27ae60', bg: '#d5f5e3' },
    8: { text: '高需求', color: '#27ae60', bg: '#d5f5e3' },
    7: { text: '穩定增長', color: '#229954', bg: '#d4efdf' },
    6: { text: '穩定', color: '#f1c40f', bg: '#fdebd0' },
    5: { text: '一般', color: '#f39c12', bg: '#fae5d3' },
    4: { text: '飽和', color: '#e67e22', bg: '#f9e79f' },
    3: { text: '高風險', color: '#e74c3c', bg: '#fadbd8' },
    2: { text: '極高風險', color: '#c0392b', bg: '#f5b7b1' }
};

// Load salary data from JSON
async function loadSalaryData() {
    try {
        const response = await fetch('data/salary-data.json');
        const data = await response.json();
        salaryData = data.industries;
        filteredData = [...salaryData];
        
        // Sort by median salary (low to high)
        updateFilteredData();
        
        initCharts();
        initDSEFilter();
    } catch (error) {
        console.error('Error loading salary data:', error);
        alert('無法載入薪金數據，請稍後再試');
    }
}

// Update filtered data with current experience level
function updateFilteredData() {
    filteredData = salaryData.map(ind => {
        const salary = ind.salaries[currentExperience];
        return {
            ...ind,
            salary: salary,
            experienceLevel: currentExperience
        };
    });
    
    // Sort by median salary (low to high)
    filteredData.sort((a, b) => a.salary.median - b.salary.median);
}

// Filter by Experience Level
window.filterByExperience = function(expLevel) {
    currentExperience = expLevel;
    updateFilteredData();
    updateCharts();
    
    // Update button states
    document.querySelectorAll('#experienceFilter .filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.exp === expLevel) {
            btn.classList.add('active');
        }
    });
};

// Initialize DSE Subject Filter
function initDSEFilter() {
    const filterContainer = document.getElementById('dseFilter');
    if (!filterContainer) return;
    
    const subjects = Object.keys(dseSubjectMapping);
    const filterHTML = `
        <div class="filter-section">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">🎓 按 DSE 選科篩選</h3>
            <div class="filter-buttons">
                ${subjects.map(subject => `
                    <button class="filter-btn" data-subject="${subject}" onclick="filterBySubject('${subject}')">
                        ${subject}
                    </button>
                `).join('')}
                <button class="filter-btn filter-reset" onclick="resetFilter()">
                    顯示全部
                </button>
            </div>
        </div>
    `;
    
    filterContainer.innerHTML = filterHTML;
}

// Filter by DSE Subject
window.filterBySubject = function(subject) {
    const relatedMajors = dseSubjectMapping[subject];
    const relatedCareers = new Set();
    
    relatedMajors.forEach(major => {
        if (majorToCareer[major]) {
            majorToCareer[major].forEach(career => relatedCareers.add(career));
        }
    });
    
    filteredData = salaryData.filter(ind => relatedCareers.has(ind.id));
    filteredData.sort((a, b) => a.salary.median - b.salary.median);
    
    // Update UI
    updateCharts();
    highlightFilter(subject);
};

// Reset Filter
window.resetFilter = function() {
    filteredData = [...salaryData];
    filteredData.sort((a, b) => a.salary.median - b.salary.median);
    updateCharts();
    highlightFilter(null);
};

// Highlight active filter button
function highlightFilter(activeSubject) {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.subject === activeSubject) {
            btn.classList.add('active');
        }
    });
}

// Update all charts with filtered data
function updateCharts() {
    // Destroy existing charts first
    if (window.salaryChartInstance) {
        window.salaryChartInstance.destroy();
    }
    if (window.scatterChartInstance) {
        window.scatterChartInstance.destroy();
    }
    if (window.hoursChartInstance) {
        window.hoursChartInstance.destroy();
    }
    if (window.stressChartInstance) {
        window.stressChartInstance.destroy();
    }
    if (window.prospectsChartInstance) {
        window.prospectsChartInstance.destroy();
    }
    
    // Recreate all charts
    createSalaryBoxPlot();
    createScatterPlot();
    createHoursChart();
    createStressChart();
    createProspectsChart();
    
    // Close insights section if open
    const insightsSection = document.getElementById('insightsSection');
    if (insightsSection) {
        insightsSection.style.display = 'none';
    }
}

// Initialize all charts
function initCharts() {
    createSalaryBoxPlot();
    createScatterPlot();
    createHoursChart();
    createStressChart();
    createProspectsChart();
}

// Create Salary Point Chart with Median Line
function createSalaryBoxPlot() {
    const ctx = document.getElementById('salaryChart').getContext('2d');
    
    const labels = filteredData.map(ind => {
        const emoji = ind.id.includes('game') ? '🎮 ' : '';
        return emoji + ind.name.split(' (')[0];
    });
    
    // Point data for each quartile (monthly salary in HKD)
    const bottomData = filteredData.map((ind, i) => ({ x: ind.salary.bottom / 12 / 1000, y: i }));
    const lowerData = filteredData.map((ind, i) => ({ x: ind.salary.lowerQuartile / 12 / 1000, y: i }));
    const medianData = filteredData.map((ind, i) => ({ x: ind.salary.median / 12 / 1000, y: i }));
    const upperData = filteredData.map((ind, i) => ({ x: ind.salary.upperQuartile / 12 / 1000, y: i }));
    const topData = filteredData.map((ind, i) => ({ x: ind.salary.top / 12 / 1000, y: i }));
    
    // Point chart data with median line
    const pointData = {
        labels: labels,
        datasets: [
            // Bottom (10th) - Point
            {
                type: 'scatter',
                label: '入行起薪 (10th)',
                data: bottomData,
                backgroundColor: 'rgba(230, 126, 34, 1)',
                borderColor: 'rgba(230, 126, 34, 1)',
                pointRadius: 6,
                pointHoverRadius: 8,
                pointStyle: 'circle',
                order: 4
            },
            // Lower (25th) - Point
            {
                type: 'scatter',
                label: '初級水平 (25th)',
                data: lowerData,
                backgroundColor: 'rgba(241, 196, 15, 1)',
                borderColor: 'rgba(241, 196, 15, 1)',
                pointRadius: 6,
                pointHoverRadius: 8,
                pointStyle: 'circle',
                order: 3
            },
            // Median (50th) - Point + Line
            {
                type: 'line',
                label: '中位數 (50th)',
                data: medianData,
                backgroundColor: 'rgba(46, 204, 113, 1)',
                borderColor: 'rgba(46, 204, 113, 1)',
                borderWidth: 3,
                pointRadius: 8,
                pointHoverRadius: 10,
                pointStyle: 'circle',
                pointBackgroundColor: 'rgba(46, 204, 113, 1)',
                pointBorderColor: 'rgba(255, 255, 255, 1)',
                pointBorderWidth: 2,
                order: 0,
                fill: false
            },
            // Upper (75th) - Point
            {
                type: 'scatter',
                label: '資深水平 (75th)',
                data: upperData,
                backgroundColor: 'rgba(52, 152, 219, 1)',
                borderColor: 'rgba(52, 152, 219, 1)',
                pointRadius: 6,
                pointHoverRadius: 8,
                pointStyle: 'circle',
                order: 2
            },
            // Top (90th) - Point
            {
                type: 'scatter',
                label: '頂尖收入 (90th)',
                data: topData,
                backgroundColor: 'rgba(155, 89, 182, 1)',
                borderColor: 'rgba(155, 89, 182, 1)',
                pointRadius: 6,
                pointHoverRadius: 8,
                pointStyle: 'circle',
                order: 1
            }
        ]
    };
    
    const config = {
        type: 'scatter',
        data: pointData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            onClick: function(evt, elements) {
                if (elements.length > 0) {
                    const index = elements[0].index;
                    const datasetIndex = elements[0].datasetIndex;
                    showIndustryInsights(index);
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const ind = filteredData[context.dataIndex];
                            const datasetLabel = context.dataset.label || '';
                            const value = context.parsed.x;
                            return [
                                `${datasetLabel}: HK$${value.toFixed(0)}K/月`,
                                ``,
                                `⏰ 工時：${ind.workingHours.median} 小時/週`,
                                `😰 壓力：${ind.stressLevel.score}/10`,
                                `📈 前景：${ind.prospects.score}/10`
                            ];
                        }
                    }
                },
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        boxWidth: 15
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '月薪 (HKD 千)',
                        font: { size: 14, weight: 'bold' }
                    },
                    ticks: { callback: function(value) { return '$' + value + 'K'; } },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' }
                },
                y: {
                    type: 'category',
                    title: {
                        display: true,
                        text: '職位',
                        font: { size: 14, weight: 'bold' }
                    },
                    labels: labels,
                    ticks: { autoSkip: false, font: { size: 11 } },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    reverse: false
                }
            }
        }
    };
    
    window.salaryChartInstance = new Chart(ctx, config);
}

// Show Industry Insights
window.showIndustryInsights = function(index) {
    const ind = filteredData[index];
    const section = document.getElementById('insightsSection');
    
    if (!section) return;
    
    const expLabel = document.querySelector(`#experienceFilter .filter-btn.active`)?.textContent || '';
    
    // Name & Emoji
    document.getElementById('insightName').textContent = ind.name;
    document.getElementById('insightEmoji').textContent = ind.id.includes('game') ? '🎮' : '💼';
    
    // Salary Details for current experience
    const salaryHTML = `
        <li><span class="salary-label">入行起薪</span><span class="salary-value">$${(ind.salary.bottom/12).toFixed(0)}K</span></li>
        <li><span class="salary-label">初級水平</span><span class="salary-value">$${(ind.salary.lowerQuartile/12).toFixed(0)}K</span></li>
        <li><span class="salary-label">中位數</span><span class="salary-value">$${(ind.salary.median/12).toFixed(0)}K</span></li>
        <li><span class="salary-label">資深水平</span><span class="salary-value">$${(ind.salary.upperQuartile/12).toFixed(0)}K</span></li>
        <li><span class="salary-label">頂尖收入</span><span class="salary-value">$${(ind.salary.top/12).toFixed(0)}K</span></li>
    `;
    document.getElementById('insightSalary').innerHTML = salaryHTML;
    
    // Career Progression
    const progressionHTML = `
        <div class="progression-grid">
            <div class="progression-item">
                <div class="progression-label">🎓 畢業生</div>
                <div class="progression-value">$${(ind.salaries.junior.median/12).toFixed(0)}K</div>
            </div>
            <div class="progression-item">
                <div class="progression-label">💼 中級</div>
                <div class="progression-value">$${(ind.salaries.mid.median/12).toFixed(0)}K</div>
            </div>
            <div class="progression-item">
                <div class="progression-label">👔 資深</div>
                <div class="progression-value">$${(ind.salaries.senior.median/12).toFixed(0)}K</div>
            </div>
        </div>
    `;
    
    // Work Details
    const prospectInfo = getProspectInfo(ind.prospects.score);
    const workHTML = `
        <li><span class="salary-label">經驗年資</span><span class="work-value">${expLabel}</span></li>
        <li><span class="salary-label">每週工時</span><span class="work-value">${ind.workingHours.median} 小時</span></li>
        <li><span class="salary-label">工時範圍</span><span class="work-value">${ind.workingHours.min}-${ind.workingHours.max} 小時</span></li>
        <li><span class="salary-label">壓力指數</span><span class="work-value">${ind.stressLevel.score}/10</span></li>
        <li><span class="salary-label">前景評分</span><span class="prospect-badge" style="background:${prospectInfo.bg};color:${prospectInfo.color}">${prospectInfo.text}</span></li>
    `;
    document.getElementById('insightWork').innerHTML = workHTML;
    
    // Add career progression section
    const progressionSection = document.createElement('div');
    progressionSection.className = 'insights-card full-width';
    progressionSection.innerHTML = `
        <h4>📈 職業發展路徑</h4>
        ${progressionHTML}
    `;
    const prospectCard = document.getElementById('insightProspect').parentElement;
    prospectCard.parentNode.insertBefore(progressionSection, prospectCard.nextSibling);
    
    // Prospect Details
    const prospectHTML = `
        <li><span class="salary-label">行業增長</span><span class="work-value">${ind.prospects.growth}</span></li>
        <li><span class="salary-label">詳細說明</span><span style="color:#7f8c8d;font-size:0.9em">${ind.prospects.note}</span></li>
        <li><span class="salary-label">工作備註</span><span style="color:#7f8c8d;font-size:0.9em">${ind.workingHours.note}</span></li>
        <li><span class="salary-label">壓力說明</span><span style="color:#7f8c8d;font-size:0.9em">${ind.stressLevel.note}</span></li>
    `;
    document.getElementById('insightProspect').innerHTML = prospectHTML;
    
    // Degrees
    const degreesHTML = ind.relatedDegrees.map(d => `<span class="degree-tag">${d}</span>`).join('');
    document.getElementById('insightDegrees').innerHTML = degreesHTML;
    
    // Skills
    const skillsHTML = ind.skills.map(s => `<span class="skill-tag">${s}</span>`).join('');
    document.getElementById('insightSkills').innerHTML = skillsHTML;
    
    // Source
    document.getElementById('insightSource').textContent = ind.source;
    
    // Show section
    section.style.display = 'block';
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

// Close Insights
window.closeInsights = function() {
    document.getElementById('insightsSection').style.display = 'none';
};

// Get Prospect Info
function getProspectInfo(score) {
    if (score >= 8) return { text: '極高需求', color: '#27ae60', bg: '#d5f5e3' };
    if (score >= 6) return { text: '高需求', color: '#27ae60', bg: '#d5f5e3' };
    if (score >= 4) return { text: '穩定', color: '#f39c12', bg: '#fae5d3' };
    return { text: '高風險', color: '#e74c3c', bg: '#fadbd8' };
}

// Create Salary vs Stress Scatter Plot (ROI Analysis)
function createScatterPlot() {
    const ctx = document.getElementById('scatterChart')?.getContext('2d');
    if (!ctx) return;
    
    const scatterData = filteredData.map(ind => ({
        x: ind.stressLevel.score,
        y: ind.salary.median / 12,  // Monthly salary
        label: ind.name.split(' (')[0],
        id: ind.id
    }));
    
    const avgStress = filteredData.reduce((sum, ind) => sum + ind.stressLevel.score, 0) / filteredData.length;
    const avgSalary = filteredData.reduce((sum, ind) => sum + ind.salary.median / 12, 0) / filteredData.length;
    
    const data = {
        datasets: [{
            label: '職位',
            data: scatterData,
            backgroundColor: scatterData.map(d => {
                if (d.x <= avgStress && d.y >= avgSalary) return 'rgba(39, 174, 96, 0.8)';
                if (d.x > avgStress && d.y >= avgSalary) return 'rgba(241, 196, 15, 0.8)';
                if (d.x <= avgStress && d.y < avgSalary) return 'rgba(52, 152, 219, 0.8)';
                return 'rgba(231, 76, 60, 0.8)';
            }),
            borderColor: scatterData.map(d => {
                if (d.x <= avgStress && d.y >= avgSalary) return 'rgba(39, 174, 96, 1)';
                if (d.x > avgStress && d.y >= avgSalary) return 'rgba(241, 196, 15, 1)';
                if (d.x <= avgStress && d.y < avgSalary) return 'rgba(52, 152, 219, 1)';
                return 'rgba(231, 76, 60, 1)';
            }),
            pointRadius: 10,
            pointHoverRadius: 14
        }]
    };
    
    const config = {
        type: 'scatter',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const d = context.raw;
                            return `${d.label}\n月薪：HK$${d.y.toLocaleString(undefined, {maximumFractionDigits: 0})}\n壓力：${d.x}/10`;
                        }
                    }
                },
                legend: { display: false }
            },
            scales: {
                x: {
                    min: 0,
                    max: 10,
                    title: { display: true, text: '壓力指數 (1-10 分)', font: { size: 14, weight: 'bold' } }
                },
                y: {
                    title: { display: true, text: '月薪中位數 (HKD 千)', font: { size: 14, weight: 'bold' } },
                    ticks: { callback: function(value) { return '$' + value.toFixed(0) + 'K'; } }
                }
            }
        }
    };
    
    window.scatterChartInstance = new Chart(ctx, config);
}

// Create Working Hours Chart
function createHoursChart() {
    const ctx = document.getElementById('hoursChart').getContext('2d');
    
    const sortedByHours = [...filteredData].sort((a, b) => a.workingHours.median - b.workingHours.median);
    const labels = sortedByHours.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByHours.map(ind => {
        if (ind.workingHours.median <= 45) return 'rgba(39, 174, 96, 0.8)';
        if (ind.workingHours.median <= 50) return 'rgba(241, 196, 15, 0.8)';
        if (ind.workingHours.median <= 60) return 'rgba(243, 156, 18, 0.8)';
        return 'rgba(231, 76, 60, 0.8)';
    });
    
    const data = {
        labels: labels,
        datasets: [{
            label: '每週工時 (小時)',
            data: sortedByHours.map(ind => ind.workingHours.median),
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.8', '1')),
            borderWidth: 1
        }]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByHours[context.dataIndex];
                            return [`中位數：${value} 小時/週`, `範圍：${ind.workingHours.min}-${ind.workingHours.max} 小時`];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 80,
                    title: { display: true, text: '每週工時', font: { size: 14, weight: 'bold' } }
                },
                y: { ticks: { autoSkip: false, font: { size: 10 } } }
            }
        }
    };
    
    window.hoursChartInstance = new Chart(ctx, config);
}

// Create Stress Level Chart
function createStressChart() {
    const ctx = document.getElementById('stressChart').getContext('2d');
    
    const sortedByStress = [...filteredData].sort((a, b) => a.stressLevel.score - b.stressLevel.score);
    const labels = sortedByStress.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByStress.map(ind => {
        if (ind.stressLevel.score <= 4) return 'rgba(39, 174, 96, 0.8)';
        if (ind.stressLevel.score <= 6) return 'rgba(241, 196, 15, 0.8)';
        if (ind.stressLevel.score <= 8) return 'rgba(243, 156, 18, 0.8)';
        return 'rgba(231, 76, 60, 0.8)';
    });
    
    const data = {
        labels: labels,
        datasets: [{
            label: '壓力指數 (1-10)',
            data: sortedByStress.map(ind => ind.stressLevel.score),
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.8', '1')),
            borderWidth: 1
        }]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByStress[context.dataIndex];
                            return [`壓力指數：${value}/10`, `${ind.stressLevel.note}`];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 10,
                    title: { display: true, text: '壓力指數 (1-10 分，越低越好)', font: { size: 14, weight: 'bold' } }
                },
                y: { ticks: { autoSkip: false, font: { size: 10 } } }
            }
        }
    };
    
    window.stressChartInstance = new Chart(ctx, config);
}

// Create Career Prospects Chart
function createProspectsChart() {
    const ctx = document.getElementById('prospectsChart').getContext('2d');
    
    const sortedByProspects = [...filteredData].sort((a, b) => b.prospects.score - a.prospects.score);
    const labels = sortedByProspects.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByProspects.map(ind => {
        if (ind.prospects.score >= 8) return 'rgba(39, 174, 96, 0.8)';
        if (ind.prospects.score >= 6) return 'rgba(241, 196, 15, 0.8)';
        if (ind.prospects.score >= 4) return 'rgba(243, 156, 18, 0.8)';
        return 'rgba(231, 76, 60, 0.8)';
    });
    
    const data = {
        labels: labels,
        datasets: [{
            label: '行業前景 (1-10)',
            data: sortedByProspects.map(ind => ind.prospects.score),
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.8', '1')),
            borderWidth: 1
        }]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByProspects[context.dataIndex];
                            return [`前景評分：${value}/10`, `增長：${ind.prospects.growth}`];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 10,
                    title: { display: true, text: '行業前景 (1-10 分，越高越好)', font: { size: 14, weight: 'bold' } }
                },
                y: { ticks: { autoSkip: false, font: { size: 10 } } }
            }
        }
    };
    
    window.prospectsChartInstance = new Chart(ctx, config);
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadSalaryData();
});
