import os
import sys
assert os.path.exists("../src/pyABFauto")

sys.path.append("../src/")
import pyABFauto

if __name__ == "__main__":
    # abfFolderPath = R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P"
    # watcher = pyABFauto.monitor.folderMonitor(abfFolderPath)
    # print(watcher)
    # watcher.analyzeNext()

    demoMemtest = R"data/19702034.abf"
    # demoIVstep = R"data/19702035.abf"
    # demoIVfast = R"data/19702036.abf"
    # demoApRamp = R"data/19702037.abf"
    # demoApSteps = R"data/19702038.abf"
    # demoApContinuous = R"data/18109034.abf"

    #pyABFauto.analyzeFolder("data")
    pyABFauto.analyzeAbf(demoMemtest)

    print("DONE")
