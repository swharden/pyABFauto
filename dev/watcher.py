"""
This script watches the X-Drive command file (folder list)
and analyzes new ABFs as they appear.
"""

import os
import sys
import time

assert os.path.exists("../src/pyABFauto")

sys.path.append(
    R"C:\Users\swharden\Documents\GitHub\pyABFauto\src\pyABFauto\src")
sys.path.append("../src/")
import pyABFauto


def watchForever(delaySec=5):
    while True:
        print("\n"*5)
        watcher = pyABFauto.commandFileWatcher()
        abfPaths = watcher.getAbfsNeedingAnalysis()
        for i, abfPath in enumerate(abfPaths):
            print(f"analyzing {i+i} of {len(abfPaths)} ABFs...")
            pyABFauto.analyzeAbf(abfPath)
        print(f"waiting {delaySec} seconds before rescanning...")
        time.sleep(delaySec)


if __name__ == "__main__":
    watchForever()
    print("DONE")
