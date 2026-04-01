"""
GPU Detection Test Script
Tests the robust two-step GPU detection approach
"""

from core.hardware_detector import HardwareDetector

def test_gpu_detection():
    """Test GPU detection and display results"""
    print("=" * 60)
    print("SysOptima GPU Detection Test")
    print("=" * 60)
    
    detector = HardwareDetector()
    gpu_info = detector.detect_gpu()
    
    print("\n[GPU Detection Results]")
    print(f"GPU Name:        {gpu_info.get('name', 'N/A')}")
    print(f"Total VRAM:      {gpu_info.get('memory_total_mb', 0):.0f} MB")
    print(f"Used VRAM:       {gpu_info.get('memory_used_mb', 0):.0f} MB")
    print(f"Detection Status: {gpu_info.get('status', 'Unknown')}")
    
    # Verify detection success
    if gpu_info.get('name') == "Unknown GPU":
        print("\n[WARNING] GPU detection failed - showing 'Unknown GPU'")
        print("Please verify:")
        print("  1. NVIDIA drivers are installed")
        print("  2. nvidia-smi is accessible from command line")
        print("  3. GPU is properly connected")
    else:
        print("\n[SUCCESS] GPU detected successfully!")
        if "nvidia-smi" in gpu_info.get('status', '').lower():
            print("  -> Detection method: nvidia-smi (fallback for WDDM mode)")
        elif "gputil" in gpu_info.get('status', '').lower():
            print("  -> Detection method: GPUtil (primary method)")
        elif "wmic" in gpu_info.get('status', '').lower():
            print("  -> Detection method: Windows WMIC (last resort)")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_gpu_detection()
