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
import imaging 

def watchForever(delaySec=5):
    while True:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        watcher = pyABFauto.commandFileWatcher()

        # convert new TIFs
        tifPaths = watcher.getTifsNeedingAnalysis()
        if len(tifPaths):
            print(f"[{timestamp}] {len(tifPaths)} TIFs require conversion.")
            for tifPath in tifPaths:
                tifFolder = os.path.dirname(tifPath)
                tifName = os.path.basename(tifPath)
                tifOutFolder = tifFolder+"/_autoanalysis/"
                if not os.path.exists(tifOutFolder):
                    os.mkdir(tifOutFolder)
                tifOutPath = tifOutFolder + tifName + ".jpg"
                try:
                    imaging.convertTifToJpg(tifPath, tifOutPath)
                except Exception as e:
                    print(f"TIF conversion failed for: {tifPath}")
                    print(e)

        # analyze new ABFs
        abfPaths = watcher.getAbfsNeedingAnalysis()
        if len(abfPaths):
            print(f"[{timestamp}] {len(abfPaths)} ABFs require analysis.")
            for i, abfPath in enumerate(abfPaths):
                print(f"analyzing {i+1} of {len(abfPaths)} ABFs...")
                try:
                    pyABFauto.analyzeAbf(abfPath)
                except Exception as ex:
                    print(f"\n\n### EXCEPTION: {abfPath}\n{ex}\n\n")
            print(f"waiting for new ABFs...")

        # wait and repeat
        time.sleep(delaySec)


if __name__ == "__main__":
    watchForever()
