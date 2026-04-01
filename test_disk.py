import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from benchmark.lightweight_benchmark import LightweightBenchmark

bench = LightweightBenchmark()
print(bench.run_disk_benchmark())
