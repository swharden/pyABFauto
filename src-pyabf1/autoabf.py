import os
PATH_HERE = os.path.dirname(__file__)
PATH_DATA = os.path.abspath(os.path.dirname(__file__)+"/../../data/abfs/")
import sys
sys.path.insert(0, PATH_HERE+"/../../src/")

import glob
import logging
import datetime

log = logging.getLogger(__name__)
log.debug(f"autoabf imported")
log.setLevel(level=logging.INFO)

sys.path.append(R"C:\Users\swharden\Documents\GitHub\pyABF\src")

import pyabf
pyabf.abf.log.setLevel(level=logging.WARN)
pyabf.abfHeader.log.setLevel(level=logging.WARN)
pyabf.sweep.log.setLevel(level=logging.WARN)

import analysisByProtocol
analysisByProtocol.log.setLevel(level=logging.INFO)

def dataFolderCreate(abfFolder, DATAFOLDER = "swhlab"):
    """Given an ABF folder (or abf file), make the data folder if needed."""
    if abfFolder.endswith(".abf"):
        abfFolder = os.path.dirname(abfFolder)
    dirData = os.path.join(abfFolder, DATAFOLDER)
    if not os.path.exists(dirData):
        log.info(f"Creating {dirData}")
        os.mkdir(dirData)
    return

def dataFilesForAbf(abfFileName, DATAFOLDER = "swhlab"):
    """Given an ABF file, return the list of data file paths."""
    dirABF = os.path.dirname(abfFileName)
    abfID = os.path.basename(abfFileName).replace(".abf","")
    dirData = os.path.join(dirABF, DATAFOLDER)
    files = glob.glob(f"{dirABF}/{DATAFOLDER}/{abfID}*.*")
    return sorted(files)

def fileListContainsAbfData(analyzedFileList, abfID):
    """
    Returns True if data for the abf ID exists in the file list.
    """
    for fname in analyzedFileList:
        if ".tif" in fname:
            continue
        bn = os.path.basename(fname)
        if bn.startswith(abfID):
            return True
    return False


def abfIDsAnalyzed(dataFolder):
    """
    Scan the data folder and return a list of ABFIDs 
    which have already been analyzed.
    """
    ids = []
    for fname in sorted(glob.glob(dataFolder+"/*.*")):
        if ".tif" in fname:
            continue
        id = os.path.basename(fname)[:-4]
        ids.append(id)
    return ids


def autoAnalyzeFolder(abfFolder, reanalyze=False):
    assert os.path.isdir(abfFolder)
    log.info(f"auto-analyzing folder: {abfFolder}")
    analyzedFileList = abfIDsAnalyzed(abfFolder+"/swhlab/")
    fnames = sorted(glob.glob(abfFolder+"/*.abf"))
    for fileNumber, abfFile in enumerate(fnames):
        abfID = os.path.basename(abfFile)[:-4]
        progress = "%s %d/%d (%.02f%%)" % (abfID,
                                           fileNumber+1,
                                           len(fnames),
                                           100*(fileNumber+1)/len(fnames))

        if reanalyze == True or not fileListContainsAbfData(analyzedFileList, abfID):
            log.info("Analyzing "+progress)
            autoAnalyzeAbf(abfFile, True)
        else:
            log.info("Skipping "+progress)


def autoAnalyzeAbf(abf, reanalyze=True):
    """
    Given an abf filename (or ABF object), produce an analysis graph of its
    data. If the protocol has a known analysis routine, run it. If not, run
    the unknown() analysis routine. In all cases, an input ABF should produce
    at least some type of output graph.
    """

    # error checking
    if isinstance(abf, str):
        abf = pyabf.ABF(abf, False)
    assert isinstance(abf, pyabf.ABF)
    log.debug(f"Auto-analyzing {abf.abfID}.abf")

    # determine if old files exist
    matchingFiles = abfnav.dataFilesForAbf(abf.abfFilePath)
    if reanalyze is False:
        if len(matchingFiles):
            log.debug(f"skipping {abf.abfID} (data files exist)")
            return
    else:
        for fname in matchingFiles:
            if ".tif" in fname.lower():
                continue
            log.debug(f"deleting {fname}")
            os.remove(fname)

    ### a few manual search/replace for special titles

    # IV-like protocols
    if "MTIV3" in abf.protocol:
        abf.protocol = "OVLY MTIV3"

    # AP steps
    if "SHIV3" in abf.protocol:
        abf.protocol = "OVAP SHIV3"

    # MT-like protocol where drug is applied
    if "MT-mon" in abf.protocol:
        abf.protocol = "MTMN MT-mon"

    # SS uses this
    if abf.protocol == "EPSCs Single":
        abf.protocol = "MTMN MT-mon"

    # force all SS IC steps to also make single-AP plots
    if "steps dual" in abf.protocol and "Sarthak" in abf.abfFilePath:
        abf.protocol = "OVAP override "+abf.protocol

    # if the protocol is in the autoanalysis format determine its function
    if not "permanent" in abf.protocolPath:
        log.warn("non-permanent protocol used! (%s)"%(abf.protocol))
    functionName = None
    if " " in abf.protocol and len(abf.protocol.split(" ")[0]) == 4:
        functionName = "protocol_"+abf.protocol.split(" ")[0]
        if not functionName in dir(analysisByProtocol):
            functionName = None
        if functionName and not hasattr(analysisByProtocol, functionName):
            functionName = None

    # if a properly formatted protocol was found, run its analysis
    if functionName:
        log.debug(f"analyzing known protocol via: {functionName}()")
        getattr(analysisByProtocol, functionName)(abf)
    else:
        msg = f"{abf.abfID} uses an unknown protocol: {abf.protocol}"
        log.warn(msg)
        with open(os.path.dirname(abf.abfFilePath)+"/pyabf.log", 'a') as f:
            timestamp = str(datetime.datetime.now())
            f.write(f"[{timestamp}] [{abf.abfFilePath}] {msg}\n")
        log.debug("analyzing with unknown()")
        analysisByProtocol.unknown(abf)
    return

if __name__ == "__main__":
    autoAnalyzeAbf(R"X:\Data\SD\PFC Oxytocin\Sarthaks PhD project\data\17518010.abf", reanalyze=True)
    #autoAnalyzeFolder(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P", reanalyze=True)
    print("DONE")
