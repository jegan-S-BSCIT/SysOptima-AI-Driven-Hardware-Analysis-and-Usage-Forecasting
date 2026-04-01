
import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.getcwd())

from core.hardware_detector import HardwareDetector

def test_hardware_detection():
    print("Initializing HardwareDetector...")
    detector = HardwareDetector()
    
    print("Detecting all hardware...")
    try:
        data = detector.detect_all()
        print("\n--- Hardware Data Dump ---")
        print(json.dumps(data, indent=2))
        
        # Verify specific Section 1 requirements
        print("\n--- Verification ---")
        
        # CPU
        cpu = data.get("cpu", {})
        if "name" in cpu and "physical_cores" in cpu and "frequency_mhz" in cpu:
            print("[PASS] CPU info detected")
        else:
            print("[FAIL] CPU info incomplete:", cpu)
            
        # RAM
        ram = data.get("ram", {})
        if "total_gb" in ram and "available_gb" in ram:
            print("[PASS] RAM info detected")
        else:
            print("[FAIL] RAM info incomplete:", ram)
            
        # Storage
        disk = data.get("disk", {})
        if "total_gb" in disk and "used_gb" in disk and "free_gb" in disk:
            print("[PASS] Storage info detected")
        else:
            print("[FAIL] Storage info incomplete:", disk)
            
        # GPU
        gpu = data.get("gpu", {})
        if "name" in gpu:
            print("[PASS] GPU info detected:", gpu["name"])
        else:
            print("[FAIL] GPU info missing")
            
        # OS
        os_info = data.get("os", {})
        if "system" in os_info:
            print("[PASS] OS info detected:", os_info["system"])
        else:
            print("[FAIL] OS info missing")
            
    except Exception as e:
        print(f"[ERROR] Detection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_hardware_detection()
