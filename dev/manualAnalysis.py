import os
import sys
import glob
import pyabf
import shutil

REPO_FOLDER = os.path.dirname(os.path.dirname(__file__))
assert os.path.exists(REPO_FOLDER + "/src/pyABFauto")
sys.path.append(REPO_FOLDER + "/src/")
import pyABFauto

def addFakeParentImages(abfFolder, parentProtocols = ['0201 memtest', '1 MTIV3']):
    tifSourcePath=R"X:\Users_Public\Scott\x.tif"
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

if __name__ == "__main__":

    for analyzeThis in [
        R"X:/Data/Alchem/Physostigmine/10-08-2021/2021_10_08_DIC1_0021.abf",
    ]:
        if os.path.isdir(analyzeThis):
            deleteStatsFiles(analyzeThis)
            lowercaseTifs(analyzeThis)
            addFakeParentImages(analyzeThis)
            pyABFauto.analyzeFolder(analyzeThis)
        else:
            pyABFauto.analyzeAbf(analyzeThis)

    print("DONE")
