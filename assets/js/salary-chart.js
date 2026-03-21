// Salary Comparison Chart Generator
// Uses Chart.js to create interactive box plot charts

let salaryData = [];

// Load salary data from JSON
async function loadSalaryData() {
    try {
        const response = await fetch('../data/salary-data.json');
        const data = await response.json();
        salaryData = data.industries;
        
        // Sort by median salary (low to high)
        salaryData.sort((a, b) => a.salary.median - b.salary.median);
        
        initCharts();
    } catch (error) {
        console.error('Error loading salary data:', error);
        alert('無法載入薪金數據，請稍後再試');
    }
}

// Initialize all charts
function initCharts() {
    createSalaryBoxPlot();
    createHoursChart();
    createStressChart();
    createProspectsChart();
}

// Create Salary Box Plot Chart
function createSalaryBoxPlot() {
    const ctx = document.getElementById('salaryChart').getContext('2d');
    
    const labels = salaryData.map(ind => {
        const emoji = ind.id.includes('game') ? '🎮 ' : '';
        return emoji + ind.name.split(' (')[0];
    });
    
    // Box plot data
    const boxData = {
        labels: labels,
        datasets: [
            {
                label: 'Top (90th percentile)',
                data: salaryData.map(ind => ind.salary.top / 1000),
                backgroundColor: 'rgba(52, 152, 219, 0.8)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1,
                type: 'bar',
                order: 5
            },
            {
                label: 'Upper Quartile (75th)',
                data: salaryData.map(ind => ind.salary.upperQuartile / 1000),
                backgroundColor: 'rgba(93, 173, 226, 0.8)',
                borderColor: 'rgba(93, 173, 226, 1)',
                borderWidth: 1,
                type: 'bar',
                order: 4
            },
            {
                label: 'Median (50th)',
                data: salaryData.map(ind => ind.salary.median / 1000),
                backgroundColor: 'rgba(133, 193, 233, 0.9)',
                borderColor: 'rgba(133, 193, 233, 1)',
                borderWidth: 2,
                type: 'line',
                order: 3,
                pointRadius: 4,
                pointHoverRadius: 6
            },
            {
                label: 'Lower Quartile (25th)',
                data: salaryData.map(ind => ind.salary.lowerQuartile / 1000),
                backgroundColor: 'rgba(174, 214, 241, 0.8)',
                borderColor: 'rgba(174, 214, 241, 1)',
                borderWidth: 1,
                type: 'bar',
                order: 2
            },
            {
                label: 'Bottom (10th percentile)',
                data: salaryData.map(ind => ind.salary.bottom / 1000),
                backgroundColor: 'rgba(212, 230, 241, 0.8)',
                borderColor: 'rgba(212, 230, 241, 1)',
                borderWidth: 1,
                type: 'bar',
                order: 1
            }
        ]
    };
    
    const config = {
        type: 'bar',
        data: boxData,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = context.parsed.x;
                            return `${label}: HK$${value.toLocaleString()}K/年 (HK$${(value * 1000 / 12).toLocaleString(undefined, {maximumFractionDigits: 0})}/月)`;
                        },
                        afterLabel: function(context) {
                            const index = context.dataIndex;
                            const ind = salaryData[index];
                            return [
                                `工時：${ind.workingHours.median} 小時/週`,
                                `壓力：${ind.stressLevel.score}/10`,
                                `前景：${ind.prospects.score}/10`
                            ];
                        }
                    }
                },
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                },
                title: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    stacked: false,
                    title: {
                        display: true,
                        text: '年薪 (HKD 千)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value + 'K';
                        }
                    }
                },
                y: {
                    stacked: false,
                    title: {
                        display: true,
                        text: '職位',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Create Working Hours Chart
function createHoursChart() {
    const ctx = document.getElementById('hoursChart').getContext('2d');
    
    // Sort by working hours (low to high)
    const sortedByHours = [...salaryData].sort((a, b) => a.workingHours.median - b.workingHours.median);
    
    const labels = sortedByHours.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByHours.map(ind => {
        if (ind.workingHours.median <= 45) return 'rgba(39, 174, 96, 0.8)'; // Green
        if (ind.workingHours.median <= 50) return 'rgba(241, 196, 15, 0.8)'; // Yellow
        if (ind.workingHours.median <= 60) return 'rgba(243, 156, 18, 0.8)'; // Orange
        return 'rgba(231, 76, 60, 0.8)'; // Red
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
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByHours[context.dataIndex];
                            return [
                                `中位數：${value} 小時/週`,
                                `範圍：${ind.workingHours.min}-${ind.workingHours.max} 小時`,
                                `${ind.workingHours.note}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 80,
                    title: {
                        display: true,
                        text: '每週工時',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return value + 'h';
                        }
                    }
                },
                y: {
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Create Stress Level Chart
function createStressChart() {
    const ctx = document.getElementById('stressChart').getContext('2d');
    
    // Sort by stress level (low to high)
    const sortedByStress = [...salaryData].sort((a, b) => a.stressLevel.score - b.stressLevel.score);
    
    const labels = sortedByStress.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByStress.map(ind => {
        if (ind.stressLevel.score <= 4) return 'rgba(39, 174, 96, 0.8)'; // Green
        if (ind.stressLevel.score <= 6) return 'rgba(241, 196, 15, 0.8)'; // Yellow
        if (ind.stressLevel.score <= 8) return 'rgba(243, 156, 18, 0.8)'; // Orange
        return 'rgba(231, 76, 60, 0.8)'; // Red
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
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByStress[context.dataIndex];
                            return [
                                `壓力指數：${value}/10`,
                                `${ind.stressLevel.note}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 10,
                    title: {
                        display: true,
                        text: '壓力指數 (1-10 分，越低越好)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Create Career Prospects Chart
function createProspectsChart() {
    const ctx = document.getElementById('prospectsChart').getContext('2d');
    
    // Sort by prospects (high to low)
    const sortedByProspects = [...salaryData].sort((a, b) => b.prospects.score - a.prospects.score);
    
    const labels = sortedByProspects.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByProspects.map(ind => {
        if (ind.prospects.score >= 8) return 'rgba(39, 174, 96, 0.8)'; // Green
        if (ind.prospects.score >= 6) return 'rgba(241, 196, 15, 0.8)'; // Yellow
        if (ind.prospects.score >= 4) return 'rgba(243, 156, 18, 0.8)'; // Orange
        return 'rgba(231, 76, 60, 0.8)'; // Red
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
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByProspects[context.dataIndex];
                            return [
                                `前景評分：${value}/10`,
                                `增長：${ind.prospects.growth}`,
                                `${ind.prospects.note}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 10,
                    title: {
                        display: true,
                        text: '行業前景 (1-10 分，越高越好)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Add click event to career paths
function addCareerPathListeners() {
    document.querySelectorAll('.career-paths li').forEach(li => {
        li.addEventListener('click', function() {
            const roleName = this.getAttribute('data-role');
            if (roleName) {
                // Find the industry with matching ID
                const industry = salaryData.find(ind => ind.id === roleName);
                if (industry) {
                    alert(`${industry.name}\n\n薪金中位數：HK$${(industry.salary.median / 12).toLocaleString(undefined, {maximumFractionDigits: 0})}/月\n工時：${industry.workingHours.median} 小時/週\n壓力：${industry.stressLevel.score}/10\n前景：${industry.prospects.score}/10\n\n${industry.notes}`);
                }
            }
        });
    });
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadSalaryData();
    addCareerPathListeners();
});
