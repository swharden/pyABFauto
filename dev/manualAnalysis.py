import os
import sys
import glob
import pyabf
import shutil
import pathlib

REPO_FOLDER = os.path.dirname(os.path.dirname(__file__))
assert os.path.exists(REPO_FOLDER + "/src/pyABFauto")
sys.path.append(REPO_FOLDER + "/src/")
if True:
    import pyABFauto


def addFakeParentImages(abfFolder, parentProtocols=['0201 memtest', '1 MTIV3']):
    tifSourcePath = R"X:\Users_Public\Scott\x.tif"
    for abfPath in glob.glob(abfFolder+"/*.abf"):
        abf = pyabf.ABF(abfPath, loadData=False)
        for protocol in parentProtocols:
            if protocol in abf.protocol:
                abfFileName = os.path.basename(abfPath)
                tifFileName = os.path.basename(abfPath.replace(".abf", ".tif"))
                tifFilePath = os.path.join(abfFolder, tifFileName)
                if not os.path.exists(tifFilePath):
                    print("CREATING:", tifFilePath)
                    shutil.copy(tifSourcePath, tifFilePath)


def lowercaseTifs(abfFolder):
    for tifPath in glob.glob(abfFolder+"/*.TIF"):
        if tifPath.endswith(".TIF"):
            print("lowercasing TIF file:", os.path.basename(tifPath))
            print("LOWERCASING:", tifPath)
            os.rename(tifPath, tifPath.replace(".TIF", ".tif"))


def deleteStatsFiles(abfFolder):
    for statsFilePath in glob.glob(abfFolder+"/*.sta"):
        print("deleting stats file:", statsFilePath)
        os.remove(statsFilePath)


def recursivelyFindAndAnalyze(folder, protocol=None):
    abfPaths = [x for x in pathlib.Path(folder).glob("**/*.abf")]
    for i, abfPath in enumerate(abfPaths):
        abf = pyabf.ABF(abfPath, loadData=False)
        print(f"{i+1} of {len(abfPaths)}: {abf.abfID} {abf.protocol}")
        if abf.protocol.startswith(protocol):
            pyABFauto.analyzeAbf(abfPath)


if __name__ == "__main__":
    recursivelyFindAndAnalyze(
        "X:/Data/zProjects/CCh in rat pups/experiments", "0918")
    print("DONE")
