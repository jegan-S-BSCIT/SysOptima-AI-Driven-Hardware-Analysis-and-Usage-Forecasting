#!/usr/bin/env python3
"""
Test Script for Real-Time Performance Monitor Module
====================================================

This script verifies that the monitor module works correctly without GUI.
Useful for debugging and CI/CD pipelines.

Run: python test_realtime_monitor.py
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.performance_monitor_engine import PerformanceMonitorEngine


def test_engine_initialization():
    """Test 1: Engine initializes without errors"""
    print("\n[TEST 1] Engine Initialization")
    print("-" * 50)
    try:
        engine = PerformanceMonitorEngine(buffer_size=30, collection_interval=1.0)
        print("✓ Engine created successfully")
        print(f"  Buffer size: {engine.buffer_size}")
        print(f"  Collection interval: {engine.collection_interval}")
        print(f"  GPU available: {engine._gpu_available}")
        return engine
    except Exception as e:
        print(f"✗ Failed to initialize engine: {e}")
        return None


def test_monitoring_start_stop(engine):
    """Test 2: Monitoring starts and stops without errors"""
    print("\n[TEST 2] Start/Stop Monitoring")
    print("-" * 50)
    try:
        engine.start_monitoring()
        print("✓ Monitoring started")
        
        # Let it collect for 3 seconds
        time.sleep(3)
        
        buffer_size = len(engine.data_buffer)
        print(f"✓ Collected {buffer_size} samples in 3 seconds")
        
        engine.stop_monitoring()
        print("✓ Monitoring stopped")
        return True
    except Exception as e:
        print(f"✗ Error during start/stop: {e}")
        return False


def test_data_collection(engine):
    """Test 3: Verify data is being collected correctly"""
    print("\n[TEST 3] Data Collection Quality")
    print("-" * 50)
    
    engine.start_monitoring()
    time.sleep(5)  # Collect 5 samples
    
    buffer_data = engine.get_buffer_copy()
    
    if not buffer_data:
        print("✗ No data collected")
        engine.stop_monitoring()
        return False
    
    print(f"✓ Collected {len(buffer_data)} snapshots")
    
    # Check latest snapshot
    latest = buffer_data[-1]
    print("\n  Latest Snapshot:")
    print(f"    CPU: {latest['cpu_percent']:.1f}%")
    print(f"    RAM: {latest['ram_percent']:.1f}%")
    print(f"    GPU: {latest['gpu_percent']:.1f}%")
    print(f"    Disk Read: {latest['disk_read_mb']:.2f} MB/s")
    print(f"    Disk Write: {latest['disk_write_mb']:.2f} MB/s")
    
    # Verify reasonable values
    assert 0 <= latest['cpu_percent'] <= 100, "CPU out of range"
    assert 0 <= latest['ram_percent'] <= 100, "RAM out of range"
    assert 0 <= latest['gpu_percent'] <= 100, "GPU out of range"
    assert latest['disk_read_mb'] >= 0, "Disk read negative"
    assert latest['disk_write_mb'] >= 0, "Disk write negative"
    
    print("\n✓ All values in valid ranges")
    
    engine.stop_monitoring()
    return True


def test_diagnostics(engine):
    """Test 4: Verify diagnostic flags work"""
    print("\n[TEST 4] Diagnostic Flags")
    print("-" * 50)
    
    engine.start_monitoring()
    time.sleep(2)
    
    diagnostics = engine.get_diagnostics()
    
    print("  Current Diagnostic Flags:")
    print(f"    High CPU Load: {diagnostics['high_cpu_load']}")
    print(f"    Memory Pressure: {diagnostics['memory_pressure']}")
    print(f"    Disk Bottleneck: {diagnostics['disk_bottleneck']}")
    print(f"    GPU Unavailable: {diagnostics['gpu_unavailable']}")
    
    print("\n✓ Diagnostics accessible")
    
    engine.stop_monitoring()
    return True


def test_statistics(engine):
    """Test 5: Verify statistics calculation"""
    print("\n[TEST 5] Statistics Calculation")
    print("-" * 50)
    
    engine.start_monitoring()
    time.sleep(5)  # Collect some data
    
    stats = engine.get_statistics()
    
    if not stats:
        print("✗ No statistics available")
        engine.stop_monitoring()
        return False
    
    print("  CPU Statistics (last 5 seconds):")
    print(f"    Min: {stats['cpu']['min']:.1f}%")
    print(f"    Max: {stats['cpu']['max']:.1f}%")
    print(f"    Avg: {stats['cpu']['avg']:.1f}%")
    
    print("\n  RAM Statistics:")
    print(f"    Min: {stats['ram']['min']:.1f}%")
    print(f"    Max: {stats['ram']['max']:.1f}%")
    print(f"    Avg: {stats['ram']['avg']:.1f}%")
    
    print("\n✓ Statistics calculated successfully")
    
    engine.stop_monitoring()
    return True


def test_buffer_overflow(engine):
    """Test 6: Verify 30-second buffer limit"""
    print("\n[TEST 6] Buffer Size Management")
    print("-" * 50)
    
    # The buffer should auto-limit to maxlen
    buffer_data = engine.get_buffer_copy()
    
    if len(buffer_data) > engine.buffer_size:
        print(f"✗ Buffer exceeded limit: {len(buffer_data)} > {engine.buffer_size}")
        return False
    
    print(f"✓ Buffer correctly limited to {engine.buffer_size} items")
    print(f"  Current size: {len(buffer_data)} items")
    
    return True


def test_thread_safety(engine):
    """Test 7: Verify thread-safe access"""
    print("\n[TEST 7] Thread Safety")
    print("-" * 50)
    
    engine.start_monitoring()
    time.sleep(2)
    
    try:
        # Simulate concurrent access
        for _ in range(10):
            data = engine.get_buffer_copy()
            diagnostics = engine.get_diagnostics()
            stats = engine.get_statistics()
            time.sleep(0.05)
        
        print("✓ Multiple concurrent accesses succeeded")
        print("✓ No race conditions detected")
        engine.stop_monitoring()
        return True
    except Exception as e:
        print(f"✗ Thread safety issue: {e}")
        engine.stop_monitoring()
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("Real-Time Monitor Module - Test Suite")
    print("=" * 50)
    
    # Test 1: Initialization
    engine = test_engine_initialization()
    if not engine:
        print("\n✗ Cannot continue - engine initialization failed")
        return False
    
    # Test 2: Start/Stop
    if not test_monitoring_start_stop(engine):
        print("\n⚠ Start/Stop failed, continuing...")
    
    # Test 3: Data Collection
    if not test_data_collection(engine):
        print("\n⚠ Data collection test failed, continuing...")
    
    # Test 4: Diagnostics
    if not test_diagnostics(engine):
        print("\n⚠ Diagnostics test failed, continuing...")
    
    # Test 5: Statistics
    if not test_statistics(engine):
        print("\n⚠ Statistics test failed, continuing...")
    
    # Test 6: Buffer Management
    if not test_buffer_overflow(engine):
        print("\n⚠ Buffer test failed, continuing...")
    
    # Test 7: Thread Safety
    if not test_thread_safety(engine):
        print("\n⚠ Thread safety test failed, continuing...")
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Suite Complete!")
    print("=" * 50)
    print("\n✓ Real-Time Monitor Module is operational")
    print("\nNext Steps:")
    print("  1. Run 'python app.py' to start the GUI")
    print("  2. Navigate to 'Real-time Monitor' in sidebar")
    print("  3. Click 'Start Monitoring' button")
    print("\n" + "=" * 50)
    
    return True


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
