/**
 * SysOptima Frontend Logic
 * B.Sc. IT Final Year Project
 * 
 * LAG PREVENTION ARCHITECTURE:
 * - Single timer control (only ONE setInterval active)
 * - Manual start/stop control
 * - Controlled refresh intervals
 * - No continuous re-rendering
 * - Efficient DOM updates (only changed values)
 */

// Global state
let monitoringActive = false;
let monitoringTimer = null;
let refreshInterval = 1000; // Default 1 second

// Chart instances (global to prevent recreation)
let cpuChart, ramChart, gpuChart, diskChart;
let benchmarkChart, comparisonChart;

// History data for charts (limited to 60 points)
let chartHistory = {
    cpu: [],
    ram: [],
    gpu: [],
    disk: []
};

// Base API URL
const API_BASE = 'http://localhost:5000/api';

/**
 * Initialize application on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('SysOptima initialized');
    initializeCharts();
    setupEventListeners();
    checkMonitoringStatus();
});

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Refresh interval change
    document.getElementById('refresh-interval').addEventListener('change', function(e) {
        refreshInterval = parseInt(e.target.value);
        console.log('Refresh interval changed to:', refreshInterval);
        
        // If monitoring is active, restart with new interval
        if (monitoringActive) {
            stopMonitoring();
            setTimeout(() => startMonitoring(), 100);
        }
    });
}

/**
 * Initialize all charts with minimal config
 */
function initializeCharts() {
    const chartConfig = {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: true,
            animation: false, // Disable animations for performance
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: { display: false },
                y: { 
                    display: false,
                    min: 0,
                    max: 100
                }
            },
            elements: {
                line: {
                    borderWidth: 2,
                    tension: 0.4
                },
                /* Removed for desktop-only build. */
                // Global state
                let monitoringActive = false;
                let monitoringTimer = null;
                let refreshInterval = 1000; // Default 1 second
        }
    };
    
    // CPU Chart
    cpuChart = new Chart(document.getElementById('cpu-chart'), {
        ...chartConfig,
        data: {
            labels: Array(60).fill(''),
            datasets: [{
                data: Array(60).fill(0),
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true
            }]
        }
    });
    
    // RAM Chart
    ramChart = new Chart(document.getElementById('ram-chart'), {
        ...chartConfig,
        data: {
            labels: Array(60).fill(''),
            datasets: [{
                data: Array(60).fill(0),
                borderColor: '#8B5CF6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                fill: true
            }]
        }
    });
    
    // GPU Chart
    gpuChart = new Chart(document.getElementById('gpu-chart'), {
        ...chartConfig,
        data: {
            labels: Array(60).fill(''),
            datasets: [{
                data: Array(60).fill(0),
                borderColor: '#F59E0B',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                fill: true
            }]
        }
    });
    
    // Disk Chart
    diskChart = new Chart(document.getElementById('disk-chart'), {
        ...chartConfig,
        data: {
            labels: Array(60).fill(''),
            datasets: [{
                data: Array(60).fill(0),
                borderColor: '#10B981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true
            }]
        },
        options: {
            ...chartConfig.options,
            scales: {
                x: { display: false },
                y: { 
                    display: false,
                    min: 0,
                    max: 200 // MB/s
                }
            }
        }
    });
}

/**
 * Check current monitoring status
 */
async function checkMonitoringStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.monitoring_active && !monitoringActive) {
            // Backend says monitoring is active but frontend doesn't know
            // Start frontend monitoring
            startMonitoring();
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

/**
 * Start live monitoring
 * LAG PREVENTION: Only ONE timer is created
 */
async function startMonitoring() {
    // Prevent multiple timers
    if (monitoringActive) {
        console.log('Monitoring already active');
        return;
    }
    
    try {
        // Call backend to set monitoring flag
        const response = await fetch(`${API_BASE}/monitor/start`, {
            method: 'POST'
        });
        
        if (!response.ok) throw new Error('Failed to start monitoring');
        
        // Update UI state
        monitoringActive = true;
        document.getElementById('start-btn').disabled = true;
        document.getElementById('start-btn').classList.add('opacity-50', 'cursor-not-allowed');
        document.getElementById('stop-btn').disabled = false;
        document.getElementById('stop-btn').classList.remove('bg-gray-300', 'text-gray-500', 'cursor-not-allowed');
        document.getElementById('stop-btn').classList.add('bg-red-600', 'hover:bg-red-700', 'text-white');
        document.getElementById('monitoring-indicator').classList.remove('hidden');
        document.getElementById('monitoring-indicator').classList.add('flex');
        
        // Start the SINGLE timer
        monitoringTimer = setInterval(fetchLiveData, refreshInterval);
        
        // Immediate first fetch
        fetchLiveData();
        
        console.log('Monitoring started with interval:', refreshInterval);
        
    } catch (error) {
        console.error('Failed to start monitoring:', error);
        alert('Failed to start monitoring. Is the backend running?');
    }
}

/**
 * Stop live monitoring
 * LAG PREVENTION: Clear the timer immediately
 */
async function stopMonitoring() {
    if (!monitoringActive) {
        console.log('Monitoring already stopped');
        return;
    }
    
    try {
        // Clear the timer FIRST (most important)
        if (monitoringTimer) {
            clearInterval(monitoringTimer);
            monitoringTimer = null;
        }
        
        // Call backend to clear monitoring flag
        await fetch(`${API_BASE}/monitor/stop`, {
            method: 'POST'
        });
        
        // Update UI state
        monitoringActive = false;
        document.getElementById('start-btn').disabled = false;
        document.getElementById('start-btn').classList.remove('opacity-50', 'cursor-not-allowed');
        document.getElementById('stop-btn').disabled = true;
        document.getElementById('stop-btn').classList.add('bg-gray-300', 'text-gray-500', 'cursor-not-allowed');
        document.getElementById('stop-btn').classList.remove('bg-red-600', 'hover:bg-red-700', 'text-white');
        document.getElementById('monitoring-indicator').classList.add('hidden');
        document.getElementById('monitoring-indicator').classList.remove('flex');
        
        console.log('Monitoring stopped');
        
    } catch (error) {
        console.error('Failed to stop monitoring:', error);
    }
}

/**
 * Fetch live data from backend
 * LAG PREVENTION: Only updates changed values, no full re-render
 */
async function fetchLiveData() {
    try {
        const response = await fetch(`${API_BASE}/monitor/live`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch live data');
        }
        
        const data = await response.json();
        
        // Update CPU
        updateMetricCard('cpu', data.cpu.usage, data.cpu);
        
        // Update RAM
        updateMetricCard('ram', data.ram.usage_percent, data.ram);
        
        // Update GPU
        updateMetricCard('gpu', data.gpu.load, data.gpu);
        
        // Update Disk
        updateMetricCard('disk', data.disk.total_speed, data.disk);
        
        // Update last update time
        const now = new Date();
        document.getElementById('last-update').textContent = `Last update: ${now.toLocaleTimeString()}`;
        
    } catch (error) {
        console.error('Failed to fetch live data:', error);
        
        // If monitoring is active but fetch fails, stop monitoring
        if (monitoringActive) {
            stopMonitoring();
            alert('Lost connection to backend. Monitoring stopped.');
        }
    }
}

/**
 * Update a metric card efficiently
 * LAG PREVENTION: Only update DOM elements that changed
 */
function updateMetricCard(type, value, data) {
    const valueElement = document.getElementById(`${type}-value`);
    const infoElement = document.getElementById(`${type}-info`);
    const changeElement = document.getElementById(`${type}-change`);
    
    // Update value
    if (type === 'cpu') {
        valueElement.innerHTML = `${value}<span class="text-lg">%</span>`;
        infoElement.textContent = `${data.cores} cores @ ${data.frequency} GHz`;
    } else if (type === 'ram') {
        valueElement.innerHTML = `${data.used_gb}<span class="text-lg">GB</span>`;
        infoElement.textContent = `${value}% of ${data.total_gb}GB`;
    } else if (type === 'gpu') {
        valueElement.innerHTML = `${value}<span class="text-lg">%</span>`;
        infoElement.textContent = `Temp: ${data.temperature}°C`;
    } else if (type === 'disk') {
        valueElement.innerHTML = `${value}<span class="text-lg">MB/s</span>`;
        infoElement.textContent = `Read/Write Speed`;
    }
    
    // Update change indicator
    const history = chartHistory[type];
    if (history.length > 0) {
        const lastValue = history[history.length - 1];
        const change = value - lastValue;
        if (change > 0) {
            changeElement.textContent = `+${change.toFixed(1)}%`;
            changeElement.className = 'text-xs text-green-600';
        } else if (change < 0) {
            changeElement.textContent = `${change.toFixed(1)}%`;
            changeElement.className = 'text-xs text-red-600';
        } else {
            changeElement.textContent = '—';
            changeElement.className = 'text-xs text-gray-400';
        }
    }
    
    // Update chart history (keep last 60 points)
    history.push(value);
    if (history.length > 60) {
        history.shift();
    }
    
    // Update chart (efficient update, no recreation)
    updateChart(type, history);
}

/**
 * Update chart data efficiently
 * LAG PREVENTION: No chart recreation, just data update
 */
function updateChart(type, data) {
    let chart;
    switch(type) {
        case 'cpu': chart = cpuChart; break;
        case 'ram': chart = ramChart; break;
        case 'gpu': chart = gpuChart; break;
        case 'disk': chart = diskChart; break;
        default: return;
    }
    
    // Pad data to 60 points
    const paddedData = [...Array(60 - data.length).fill(0), ...data];
    
    chart.data.datasets[0].data = paddedData;
    chart.update('none'); // 'none' mode = no animation
}

/**
 * Run benchmark tests
 */
async function runBenchmark() {
    const runButton = document.getElementById('run-benchmark-btn');
    const loadingDiv = document.getElementById('benchmark-loading');
    const resultsDiv = document.getElementById('benchmark-results');
    
    try {
        // Show loading
        runButton.disabled = true;
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        
        // Call backend
        const response = await fetch(`${API_BASE}/benchmark/run`, {
            method: 'POST'
        });
        
        if (!response.ok) throw new Error('Benchmark failed');
        
        const data = await response.json();
        
        // Update benchmark results
        displayBenchmarkResults(data);
        
        // Load comparison and health data
        await loadComparison();
        await loadHealthData();
        
        // Hide loading, show results
        loadingDiv.classList.add('hidden');
        resultsDiv.classList.remove('hidden');
        runButton.disabled = false;
        
    } catch (error) {
        console.error('Benchmark failed:', error);
        alert('Benchmark failed. Please check if backend is running.');
        loadingDiv.classList.add('hidden');
        runButton.disabled = false;
    }
}

/**
 * Display benchmark results
 */
function displayBenchmarkResults(data) {
    const benchmarks = data.benchmarks;
    
    // CPU
    document.getElementById('bench-cpu-score').textContent = benchmarks.cpu.score.toFixed(1);
    document.getElementById('bench-cpu-rating').textContent = benchmarks.cpu.rating;
    document.getElementById('bench-cpu-rating').className = getRatingClass(benchmarks.cpu.rating);
    document.getElementById('bench-cpu-time').textContent = `Time: ${benchmarks.cpu.time.toFixed(3)}s`;
    
    // RAM
    document.getElementById('bench-ram-score').textContent = benchmarks.ram.score.toFixed(1);
    document.getElementById('bench-ram-rating').textContent = benchmarks.ram.rating;
    document.getElementById('bench-ram-rating').className = getRatingClass(benchmarks.ram.rating);
    document.getElementById('bench-ram-time').textContent = `Time: ${benchmarks.ram.time.toFixed(3)}s`;
    
    // Storage
    document.getElementById('bench-storage-score').textContent = benchmarks.storage.score.toFixed(1);
    document.getElementById('bench-storage-rating').textContent = benchmarks.storage.rating;
    document.getElementById('bench-storage-rating').className = getRatingClass(benchmarks.storage.rating);
    document.getElementById('bench-storage-speed').textContent = `Speed: ${benchmarks.storage.speed.toFixed(1)} MB/s`;
    
    // GPU
    document.getElementById('bench-gpu-score').textContent = benchmarks.gpu.score.toFixed(1);
    document.getElementById('bench-gpu-rating').textContent = benchmarks.gpu.rating;
    document.getElementById('bench-gpu-rating').className = getRatingClass(benchmarks.gpu.rating);
    document.getElementById('bench-gpu-class').textContent = `Class: ${benchmarks.gpu.classification}`;
    
    // Overall
    document.getElementById('bench-overall-score').textContent = data.overall_score.toFixed(1);
    document.getElementById('bench-bottleneck').textContent = data.bottleneck;
    
    // Create benchmark chart
    createBenchmarkChart(benchmarks, data.overall_score);
}

/**
 * Create benchmark comparison chart
 */
function createBenchmarkChart(benchmarks, overall) {
    const ctx = document.getElementById('benchmark-chart');
    
    if (benchmarkChart) {
        benchmarkChart.destroy();
    }
    
    benchmarkChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['CPU', 'RAM', 'Storage', 'GPU', 'Overall'],
            datasets: [{
                label: 'Score',
                data: [
                    benchmarks.cpu.score,
                    benchmarks.ram.score,
                    benchmarks.storage.score,
                    benchmarks.gpu.score,
                    overall
                ],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(79, 70, 229, 0.8)'
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Load comparison data
 */
async function loadComparison() {
    try {
        const response = await fetch(`${API_BASE}/comparison`);
        
        if (!response.ok) {
            document.getElementById('comparison-empty').classList.remove('hidden');
            document.getElementById('comparison-data').classList.add('hidden');
            return;
        }
        
        const data = await response.json();
        
        // Hide empty state, show data
        document.getElementById('comparison-empty').classList.add('hidden');
        document.getElementById('comparison-data').classList.remove('hidden');
        
        // Update status badges
        updateStatusBadge('cpu', data.status.cpu);
        updateStatusBadge('ram', data.status.ram);
        updateStatusBadge('storage', data.status.storage);
        updateStatusBadge('gpu', data.status.gpu);
        updateStatusBadge('overall', data.status.overall);
        
        // Create comparison chart
        createComparisonChart(data);
        
        // Populate comparison table
        populateComparisonTable(data);
        
    } catch (error) {
        console.error('Failed to load comparison:', error);
    }
}

/**
 * Update status badge
 */
function updateStatusBadge(component, status) {
    const element = document.getElementById(`comp-${component}-status`);
    element.textContent = status;
    
    if (status === 'Above Average') {
        element.className = 'text-sm px-3 py-1 rounded-full bg-green-100 text-green-700';
    } else if (status === 'Below Average') {
        element.className = 'text-sm px-3 py-1 rounded-full bg-red-100 text-red-700';
    } else {
        element.className = 'text-sm px-3 py-1 rounded-full bg-blue-100 text-blue-700';
    }
}

/**
 * Create comparison chart
 */
function createComparisonChart(data) {
    const ctx = document.getElementById('comparison-chart');
    
    if (comparisonChart) {
        comparisonChart.destroy();
    }
    
    comparisonChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['CPU', 'RAM', 'Storage', 'GPU'],
            datasets: [
                {
                    label: 'Your System',
                    data: [
                        data.local.cpu,
                        data.local.ram,
                        data.local.storage,
                        data.local.gpu
                    ],
                    backgroundColor: 'rgba(79, 70, 229, 0.2)',
                    borderColor: 'rgba(79, 70, 229, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Reference (Avg)',
                    data: [
                        data.reference.cpu_score,
                        data.reference.ram_score,
                        data.reference.storage_score,
                        data.reference.gpu_score
                    ],
                    backgroundColor: 'rgba(156, 163, 175, 0.2)',
                    borderColor: 'rgba(156, 163, 175, 1)',
                    borderWidth: 2,
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            }
        }
    });
}

/**
 * Populate comparison table
 */
function populateComparisonTable(data) {
    const tbody = document.getElementById('comparison-table');
    tbody.innerHTML = '';
    
    const components = ['cpu', 'ram', 'storage', 'gpu', 'overall'];
    const names = ['CPU', 'RAM', 'Storage', 'GPU', 'Overall'];
    
    components.forEach((comp, index) => {
        const local = data.local[comp];
        const ref = data.reference[comp === 'overall' ? 'overall' : comp + '_score'];
        const diff = data.differences[comp];
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-4 py-3 text-sm font-medium text-gray-900">${names[index]}</td>
            <td class="px-4 py-3 text-sm text-right text-gray-900">${local.toFixed(1)}</td>
            <td class="px-4 py-3 text-sm text-right text-gray-500">${ref.toFixed(1)}</td>
            <td class="px-4 py-3 text-sm text-right ${diff.percent >= 0 ? 'text-green-600' : 'text-red-600'}">
                ${diff.percent >= 0 ? '+' : ''}${diff.percent.toFixed(1)}%
            </td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Load system health data
 */
async function loadHealthData() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        
        if (!response.ok) {
            document.getElementById('health-empty').classList.remove('hidden');
            document.getElementById('health-data').classList.add('hidden');
            return;
        }
        
        const data = await response.json();
        
        // Hide empty state, show data
        document.getElementById('health-empty').classList.add('hidden');
        document.getElementById('health-data').classList.remove('hidden');
        
        // Update health card
        const healthCard = document.getElementById('health-status-card');
        const healthColors = {
            'Excellent': 'bg-gradient-to-r from-green-500 to-green-600',
            'Good': 'bg-gradient-to-r from-blue-500 to-blue-600',
            'Fair': 'bg-gradient-to-r from-yellow-500 to-yellow-600',
            'Poor': 'bg-gradient-to-r from-red-500 to-red-600'
        };
        healthCard.className = `rounded-lg p-8 text-white text-center mb-6 ${healthColors[data.health_status]}`;
        
        document.getElementById('health-score').textContent = data.overall_score.toFixed(1) + '%';
        document.getElementById('health-status-text').textContent = data.health_status;
        document.getElementById('health-bottleneck').textContent = data.bottleneck;
        
        // Populate recommendations
        populateRecommendations(data.recommendations);
        
    } catch (error) {
        console.error('Failed to load health data:', error);
    }
}

/**
 * Populate recommendations list
 */
function populateRecommendations(recommendations) {
    const container = document.getElementById('recommendations-list');
    container.innerHTML = '';
    
    if (recommendations.length === 0) {
        container.innerHTML = '<p class="text-center text-gray-500">No recommendations - your system is performing well!</p>';
        return;
    }
    
    recommendations.forEach(rec => {
        const priorityColors = {
            'high': 'bg-red-100 text-red-700 border-red-200',
            'medium': 'bg-yellow-100 text-yellow-700 border-yellow-200',
            'low': 'bg-blue-100 text-blue-700 border-blue-200'
        };
        
        const typeIcons = {
            'software': '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>',
            'hardware': '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/></svg>'
        };
        
        const div = document.createElement('div');
        div.className = `border rounded-lg p-4 ${priorityColors[rec.priority]}`;
        div.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="flex-shrink-0 mt-1">${typeIcons[rec.type]}</div>
                <div class="flex-1">
                    <div class="flex items-center justify-between mb-1">
                        <span class="font-semibold text-sm">${rec.component}</span>
                        <span class="text-xs uppercase">${rec.priority} Priority</span>
                    </div>
                    <p class="text-sm">${rec.message}</p>
                    <span class="text-xs mt-1 inline-block">${rec.type === 'software' ? '💻 Software' : '🔧 Hardware'}</span>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
}

/**
 * Get rating CSS class
 */
function getRatingClass(rating) {
    if (rating.includes('ABOVE')) {
        return 'text-sm text-green-600 font-medium';
    } else if (rating.includes('BELOW')) {
        return 'text-sm text-red-600 font-medium';
    } else {
        return 'text-sm text-blue-600 font-medium';
    }
}

/**
 * Tab navigation
 */
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('border-primary', 'text-primary');
        btn.classList.add('border-transparent', 'text-gray-500');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.remove('hidden');
    
    // Add active class to selected button
    const activeButton = document.getElementById(`tab-${tabName}`);
    activeButton.classList.add('border-primary', 'text-primary');
    activeButton.classList.remove('border-transparent', 'text-gray-500');
}
