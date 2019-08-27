import os
import sys
assert os.path.exists("../src/pyABFauto")

sys.path.append("../src/")
import pyABFauto

if __name__ == "__main__":

    pyABFauto.analyzeAbf(R"X:\Data\OTR-Cre\VTA inj ChR2 NAc response\abfs\2019_08_27_0008.abf")

    # abfFolderPath = R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P"
    # watcher = pyABFauto.monitor.folderMonitor(abfFolderPath)
    # print(watcher)
    # watcher.analyzeNext()

    #pyABFauto.analyzeFolder(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-02-28 light firing")

    # demoMemtest = R"data/19702034.abf"
    # demoIVstep = R"data/19702035.abf"
    # demoIVfast = R"data/19702036.abf"
    # demoApRamp = R"data/19702037.abf"
    # demoApSteps = R"data/19702038.abf"
    # demoApTimeTags = R"data/19228004.abf"
    # pyABFauto.analyzeAbf(demoApTimeTags)

    print("DONE")
