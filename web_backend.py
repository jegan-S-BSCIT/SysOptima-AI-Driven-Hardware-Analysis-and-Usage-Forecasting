"""
SysOptima Web Backend - Flask API
B.Sc. IT Final Year Project

Architecture:
- Flask REST API for system monitoring
- Lightweight data collection
- Controlled monitoring (start/stop)
- No continuous background threads

Author: Final Year Student
"""

# NOTE: Web backend removed to enforce desktop-only application.
# This file is intentionally disabled and should not be executed.
raise SystemExit("Web backend removed. Use main.py for the desktop app.")

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psutil
import GPUtil
import time
import os
import tempfile
import json
from datetime import datetime
from threading import Lock

# Import existing modules
from core.lightweight_benchmarks import LightweightBenchmark
from core.performance_analyzer import PerformanceAnalyzer

app = Flask(__name__, 
            static_folder='web_static',
            template_folder='web_templates')
CORS(app)

# Thread-safe monitoring state
monitoring_lock = Lock()
monitoring_active = False
monitoring_history = {
    'cpu': [],
    'ram': [],
    'gpu': [],
    'disk': []
}

# Benchmark results cache
benchmark_cache = {
    'results': None,
    'timestamp': None
}

# Reference data for comparison
REFERENCE_DATA = {
    'cpu_score': 65,
    'ram_score': 70,
    'storage_score': 60,
    'gpu_score': 65,
    'overall': 65
}


def get_cpu_info():
    """Get current CPU usage and info"""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        
        return {
            'usage': round(cpu_percent, 1),
            'frequency': round(cpu_freq.current, 0) if cpu_freq else 0,
            'cores': cpu_count,
            'threads': cpu_threads,
            'temperature': 'N/A'  # Requires platform-specific libraries
        }
    except Exception as e:
        return {'error': str(e)}


def get_ram_info():
    """Get current RAM usage and info"""
    try:
        ram = psutil.virtual_memory()
        return {
            'used_gb': round(ram.used / (1024**3), 1),
            'total_gb': round(ram.total / (1024**3), 1),
            'usage_percent': round(ram.percent, 1),
            'available_gb': round(ram.available / (1024**3), 1)
        }
    except Exception as e:
        return {'error': str(e)}


def get_gpu_info():
    """Get current GPU load and info"""
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            return {
                'name': gpu.name,
                'load': round(gpu.load * 100, 1),
                'memory_used': round(gpu.memoryUsed / 1024, 1),
                'memory_total': round(gpu.memoryTotal / 1024, 1),
                'temperature': round(gpu.temperature, 1) if gpu.temperature else 'N/A'
            }
        else:
            return {
                'name': 'No GPU',
                'load': 0,
                'memory_used': 0,
                'memory_total': 0,
                'temperature': 'N/A'
            }
    except Exception as e:
        return {'error': str(e)}


def get_disk_info():
    """Get current disk I/O and info"""
    try:
        # Get disk I/O counters
        disk_io_start = psutil.disk_io_counters()
        time.sleep(0.5)
        disk_io_end = psutil.disk_io_counters()
        
        read_speed = (disk_io_end.read_bytes - disk_io_start.read_bytes) / 0.5
        write_speed = (disk_io_end.write_bytes - disk_io_start.write_bytes) / 0.5
        
        # Get disk usage
        disk_usage = psutil.disk_usage('/')
        
        return {
            'read_speed': round(read_speed / (1024**2), 1),  # MB/s
            'write_speed': round(write_speed / (1024**2), 1),  # MB/s
            'total_speed': round((read_speed + write_speed) / (1024**2), 1),
            'used_gb': round(disk_usage.used / (1024**3), 1),
            'total_gb': round(disk_usage.total / (1024**3), 1),
            'usage_percent': round(disk_usage.percent, 1)
        }
    except Exception as e:
        return {'error': str(e)}


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get monitoring status"""
    with monitoring_lock:
        return jsonify({
            'monitoring_active': monitoring_active,
            'timestamp': datetime.now().isoformat()
        })


@app.route('/api/monitor/start', methods=['POST'])
def start_monitoring():
    """Start monitoring (just set flag, frontend controls updates)"""
    global monitoring_active
    with monitoring_lock:
        monitoring_active = True
    return jsonify({
        'status': 'started',
        'message': 'Monitoring activated'
    })


@app.route('/api/monitor/stop', methods=['POST'])
def stop_monitoring():
    """Stop monitoring"""
    global monitoring_active
    with monitoring_lock:
        monitoring_active = False
    return jsonify({
        'status': 'stopped',
        'message': 'Monitoring deactivated'
    })


@app.route('/api/monitor/live', methods=['GET'])
def get_live_data():
    """Get current system metrics - ONLY called when monitoring is active"""
    with monitoring_lock:
        if not monitoring_active:
            return jsonify({
                'error': 'Monitoring not active',
                'monitoring_active': False
            }), 400
    
    # Collect live data
    cpu_data = get_cpu_info()
    ram_data = get_ram_info()
    gpu_data = get_gpu_info()
    disk_data = get_disk_info()
    
    # Store in history (keep last 60 data points)
    with monitoring_lock:
        monitoring_history['cpu'].append(cpu_data['usage'])
        monitoring_history['ram'].append(ram_data['usage_percent'])
        monitoring_history['gpu'].append(gpu_data['load'])
        monitoring_history['disk'].append(disk_data['total_speed'])
        
        # Keep only last 60 points
        for key in monitoring_history:
            if len(monitoring_history[key]) > 60:
                monitoring_history[key] = monitoring_history[key][-60:]
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'cpu': cpu_data,
        'ram': ram_data,
        'gpu': gpu_data,
        'disk': disk_data,
        'monitoring_active': monitoring_active
    })


@app.route('/api/monitor/history', methods=['GET'])
def get_history():
    """Get historical data for charts"""
    with monitoring_lock:
        return jsonify({
            'history': monitoring_history,
            'timestamp': datetime.now().isoformat()
        })


@app.route('/api/benchmark/run', methods=['POST'])
def run_benchmark():
    """Run lightweight benchmarks (user-triggered only)"""
    global benchmark_cache
    
    try:
        # Initialize benchmark engine
        benchmarker = LightweightBenchmark()
        
        # Run all benchmarks
        results = {
            'timestamp': datetime.now().isoformat(),
            'benchmarks': {}
        }
        
        # CPU Benchmark
        cpu_result = benchmarker.benchmark_cpu()
        results['benchmarks']['cpu'] = {
            'score': cpu_result['score'],
            'time': cpu_result['time'],
            'rating': cpu_result['rating']
        }
        
        # RAM Benchmark
        ram_result = benchmarker.benchmark_ram()
        results['benchmarks']['ram'] = {
            'score': ram_result['score'],
            'time': ram_result['time'],
            'rating': ram_result['rating']
        }
        
        # Storage Benchmark
        storage_result = benchmarker.benchmark_storage()
        results['benchmarks']['storage'] = {
            'score': storage_result['score'],
            'speed': storage_result['speed'],
            'rating': storage_result['rating']
        }
        
        # GPU Classification
        gpu_result = benchmarker.benchmark_gpu()
        results['benchmarks']['gpu'] = {
            'score': gpu_result['score'],
            'classification': gpu_result['classification'],
            'rating': gpu_result['rating']
        }
        
        # Overall Score
        overall_score = (
            cpu_result['score'] + 
            ram_result['score'] + 
            storage_result['score'] + 
            gpu_result['score']
        ) / 4
        
        results['overall_score'] = round(overall_score, 1)
        
        # Identify bottleneck
        scores = {
            'CPU': cpu_result['score'],
            'RAM': ram_result['score'],
            'Storage': storage_result['score'],
            'GPU': gpu_result['score']
        }
        bottleneck = min(scores, key=scores.get)
        results['bottleneck'] = bottleneck
        
        # Cache results
        benchmark_cache['results'] = results
        benchmark_cache['timestamp'] = datetime.now()
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Benchmark execution failed'
        }), 500


@app.route('/api/benchmark/results', methods=['GET'])
def get_benchmark_results():
    """Get cached benchmark results"""
    if benchmark_cache['results']:
        return jsonify(benchmark_cache['results'])
    else:
        return jsonify({
            'message': 'No benchmark results available. Run benchmark first.'
        }), 404


@app.route('/api/comparison', methods=['GET'])
def get_comparison():
    """Compare local system with reference hardware"""
    if not benchmark_cache['results']:
        return jsonify({
            'error': 'No benchmark results available. Run benchmark first.'
        }), 404
    
    local_results = benchmark_cache['results']['benchmarks']
    
    comparison = {
        'local': {
            'cpu': local_results['cpu']['score'],
            'ram': local_results['ram']['score'],
            'storage': local_results['storage']['score'],
            'gpu': local_results['gpu']['score'],
            'overall': benchmark_cache['results']['overall_score']
        },
        'reference': REFERENCE_DATA,
        'differences': {},
        'status': {}
    }
    
    # Calculate differences
    for component in ['cpu', 'ram', 'storage', 'gpu', 'overall']:
        local_key = component + '_score' if component != 'overall' else component
        local_value = comparison['local'][component]
        ref_value = REFERENCE_DATA.get(local_key, 65)
        
        diff = local_value - ref_value
        diff_percent = (diff / ref_value) * 100
        
        comparison['differences'][component] = {
            'absolute': round(diff, 1),
            'percent': round(diff_percent, 1)
        }
        
        # Determine status
        if diff_percent >= 10:
            status = 'Above Average'
        elif diff_percent <= -10:
            status = 'Below Average'
        else:
            status = 'Average'
        
        comparison['status'][component] = status
    
    return jsonify(comparison)


@app.route('/api/health', methods=['GET'])
def get_system_health():
    """Get overall system health and recommendations"""
    if not benchmark_cache['results']:
        return jsonify({
            'error': 'No benchmark results available. Run benchmark first.'
        }), 404
    
    results = benchmark_cache['results']
    overall_score = results['overall_score']
    bottleneck = results['bottleneck']
    
    # Determine health status
    if overall_score >= 75:
        health_status = 'Excellent'
        health_color = 'green'
    elif overall_score >= 60:
        health_status = 'Good'
        health_color = 'blue'
    elif overall_score >= 40:
        health_status = 'Fair'
        health_color = 'yellow'
    else:
        health_status = 'Poor'
        health_color = 'red'
    
    # Generate recommendations
    recommendations = []
    
    # CPU recommendations
    if results['benchmarks']['cpu']['score'] < 60:
        recommendations.append({
            'component': 'CPU',
            'type': 'software',
            'priority': 'high',
            'message': 'Close unnecessary background applications to reduce CPU load'
        })
        recommendations.append({
            'component': 'CPU',
            'type': 'software',
            'priority': 'medium',
            'message': 'Disable startup programs that you don\'t need'
        })
    
    # RAM recommendations
    if results['benchmarks']['ram']['score'] < 60:
        recommendations.append({
            'component': 'RAM',
            'type': 'software',
            'priority': 'high',
            'message': 'Close memory-intensive applications like browsers with many tabs'
        })
        if results['benchmarks']['ram']['score'] < 40:
            recommendations.append({
                'component': 'RAM',
                'type': 'hardware',
                'priority': 'medium',
                'message': 'Consider upgrading RAM for better multitasking performance'
            })
    
    # Storage recommendations
    if results['benchmarks']['storage']['score'] < 60:
        recommendations.append({
            'component': 'Storage',
            'type': 'software',
            'priority': 'medium',
            'message': 'Run disk cleanup and defragmentation (for HDD)'
        })
        if results['benchmarks']['storage']['score'] < 40:
            recommendations.append({
                'component': 'Storage',
                'type': 'hardware',
                'priority': 'high',
                'message': 'Upgrade to SSD for significantly faster performance'
            })
    
    # GPU recommendations
    if results['benchmarks']['gpu']['score'] < 60:
        recommendations.append({
            'component': 'GPU',
            'type': 'software',
            'priority': 'low',
            'message': 'Update GPU drivers for better performance'
        })
    
    # General recommendations
    if overall_score < 60:
        recommendations.append({
            'component': 'System',
            'type': 'software',
            'priority': 'high',
            'message': 'Regular system maintenance: clean temp files, update OS'
        })
    
    return jsonify({
        'overall_score': overall_score,
        'health_status': health_status,
        'health_color': health_color,
        'bottleneck': bottleneck,
        'recommendations': recommendations,
        'timestamp': results['timestamp']
    })


@app.route('/api/system/info', methods=['GET'])
def get_system_info():
    """Get static system information"""
    try:
        cpu_info = get_cpu_info()
        ram_info = get_ram_info()
        gpu_info = get_gpu_info()
        disk_info = get_disk_info()
        
        return jsonify({
            'os': f"{os.name}",
            'platform': psutil.os.uname().system if hasattr(psutil.os, 'uname') else 'Unknown',
            'cpu': {
                'cores': cpu_info.get('cores', 0),
                'threads': cpu_info.get('threads', 0),
                'frequency': cpu_info.get('frequency', 0)
            },
            'ram': {
                'total_gb': ram_info.get('total_gb', 0)
            },
            'gpu': {
                'name': gpu_info.get('name', 'Unknown'),
                'memory_total': gpu_info.get('memory_total', 0)
            },
            'disk': {
                'total_gb': disk_info.get('total_gb', 0)
            }
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("SysOptima Web Backend Starting...")
    print("=" * 60)
    print("Access the application at: http://localhost:5000")
    print("API Documentation:")
    print("  GET  /api/status          - Check monitoring status")
    print("  POST /api/monitor/start   - Start live monitoring")
    print("  POST /api/monitor/stop    - Stop live monitoring")
    print("  GET  /api/monitor/live    - Get live metrics")
    print("  POST /api/benchmark/run   - Run benchmarks")
    print("  GET  /api/comparison      - Get comparison data")
    print("  GET  /api/health          - Get system health")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
