import os
import sys
import glob
import pyabf
import shutil
assert os.path.exists("../src/pyABFauto")

sys.path.append("../src/")
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

if __name__ == "__main__":

    analyzeThis = R"X:\Data\DIC2\2017\2017-01\2017-01-18"

    if os.path.isdir(analyzeThis):
        lowercaseTifs(analyzeThis)
        addFakeParentImages(analyzeThis)
        pyABFauto.analyzeFolder(analyzeThis)
    else:
        pyABFauto.analyzeAbf(analyzeThis)

    print("DONE")
