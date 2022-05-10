"""
This script simulates a long-running but auto-exiting python application
"""

import time
print("starting")
for i in range(5):
    time.sleep(1)
    print(f"sleeping {time.time()}")
print("exiting")
