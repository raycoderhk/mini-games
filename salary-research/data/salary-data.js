// Salary Data Wrapper
// This file loads and exports the salary data for the chart

// Load salary data from JSON file
async function loadSalaryData() {
    try {
        const response = await fetch('data/salary-data.json');
        const data = await response.json();
        window.salaryData = data;
        console.log('✅ Salary data loaded:', data.industries.length, 'industries');
        return data;
    } catch (error) {
        console.error('❌ Error loading salary data:', error);
        throw error;
    }
}

// Auto-load on page load
if (typeof window !== 'undefined') {
    window.loadSalaryData = loadSalaryData;
}
