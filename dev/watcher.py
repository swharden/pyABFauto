"""
This script watches the X-Drive command file (folder list)
and analyzes new ABFs as they appear.
"""

import gc
import tracemalloc
import datetime
import time
import sys
import os
import imaging

REPO_FOLDER = os.path.dirname(os.path.dirname(__file__))
assert os.path.exists(REPO_FOLDER + "/src/pyABFauto")
sys.path.append(REPO_FOLDER + "/src/")
if True:
    import pyABFauto


def watchForever(delaySec=5):
    tracemalloc.start()
    while True:

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        watcher = pyABFauto.commandFileWatcher()
        actionTaken = False

        # convert new TIFs
        tifPaths = watcher.getTifsNeedingAnalysis()
        if len(tifPaths):
            print(f"[{timestamp}] {len(tifPaths)} TIFs require conversion.")
            actionTaken = True
            for tifPath in tifPaths:
                tifFolder = os.path.dirname(tifPath)
                tifName = os.path.basename(tifPath)
                tifOutFolder = tifFolder+"/_autoanalysis/"
                if not os.path.exists(tifOutFolder):
                    os.mkdir(tifOutFolder)
                try:
                    #tifOutPath = tifOutFolder + tifName + ".jpg"
                    tifOutPath = tifOutFolder + tifName + ".png"
                    #imaging.convertTifToJpg(tifPath, tifOutPath)
                    imaging.autoConvertToPNG(tifPath, tifOutPath)
                except Exception as e:
                    print(f"TIF conversion failed for: {tifPath}")
                    print(e)

        # analyze new ABFs
        abfPaths = watcher.getAbfsNeedingAnalysis()
        if len(abfPaths):
            print(f"[{timestamp}] {len(abfPaths)} ABFs require analysis.")
            actionTaken = True
            for i, abfPath in enumerate(abfPaths):
                print(f"analyzing {i+1} of {len(abfPaths)} ABFs...")
                try:
                    pyABFauto.analyzeAbf(abfPath)
                except Exception as ex:
                    print(f"\n\n### EXCEPTION: {abfPath}\n{ex}\n\n")
            print(f"waiting for new ABFs...")

        # show memory information
        if actionTaken:
            gc.collect()
            memory = tracemalloc.get_traced_memory()[0]/1e6
            print(f"memory: {memory} MB")

        # wait and repeat
        time.sleep(delaySec)


if __name__ == "__main__":

    while True:
        watchForever()