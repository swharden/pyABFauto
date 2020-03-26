import os
import sys
assert os.path.exists("../src/pyABFauto")

sys.path.append("../src/")
import pyABFauto

if __name__ == "__main__":

    #pyABFauto.analyzeAbf(R"X:\Data\DIC2\2016\2016-04\2016-04-28\16428032.abf")

    # abfFolderPath = R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P"
    # watcher = pyABFauto.monitor.folderMonitor(abfFolderPath)
    # print(watcher)
    # watcher.analyzeNext()

    pyABFauto.analyzeFolder(R"X:\Data\DIC2\2016\2016-04\2016-04-28")

    # demoMemtest = R"data/19702034.abf"
    # demoIVstep = R"data/19702035.abf"
    # demoIVfast = R"data/19702036.abf"
    # demoApRamp = R"data/19702037.abf"
    # demoApSteps = R"data/19702038.abf"
    # demoApTimeTags = R"data/19228004.abf"
    # pyABFauto.analyzeAbf(demoApTimeTags)

    print("DONE")
