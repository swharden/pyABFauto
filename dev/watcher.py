"""
This script watches the X-Drive command file (folder list)
and analyzes new ABFs as they appear.
"""

import os
import sys
import time
import datetime

assert os.path.exists("../src/pyABFauto")

sys.path.append(
    R"C:\Users\swharden\Documents\GitHub\pyABFauto\src\pyABFauto\src")
sys.path.append("../src/")
import pyABFauto

def watchForever(delaySec=5):
    while True:
        watcher = pyABFauto.commandFileWatcher()
        abfPaths = watcher.getAbfsNeedingAnalysis()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(abfPaths):
            print(f"[{timestamp}] {len(abfPaths)} ABFs require analysis.")
            for i, abfPath in enumerate(abfPaths):
                print(f"analyzing {i+1} of {len(abfPaths)} ABFs...")
                try:
                    pyABFauto.analyzeAbf(abfPath)
                except Exception as ex:
                    print(f"\n\n### EXCEPTION: {abfPath}\n{ex}\n\n")
            print(f"waiting for new ABFs...")
        time.sleep(delaySec)


if __name__ == "__main__":
    watchForever()
    print("DONE")
