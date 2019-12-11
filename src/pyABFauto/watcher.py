"""
Code here allows directories to be monitored for new ABFs
and analyzed as they appear on disk.
"""

import os
import glob

import pyABFauto
DEFAULT_COMMAND_FILE = R"X:\Lab Documents\network\autoAnalysisFolders.txt"
SERVER_XDRIVE_FOLDER = R"D:\X_Drive"
DEVELOPER_XDRIVE_FOLDER = R"X:"


class commandFileWatcher:

    def __init__(self, commandFile=DEFAULT_COMMAND_FILE):
        self.commandFilePath = os.path.abspath(commandFile)

    def getAbfsNeedingAnalysis(self, rescan=True):
        abfs = []
        for folder in self.getFolderListFromCommandsFile():
            newABFs = self.getAbfsNeedingAnalysisInAFolder(folder)
            if (len(newABFs) > 0):
                print(f"  Identified {len(newABFs)} ABFs needing analysis")
            abfs += newABFs
        return abfs

    def getFolderListFromCommandsFile(self):
        assert os.path.exists(self.commandFilePath)
        #print("Reading command file:", self.commandFilePath)
        folders = []
        with open(self.commandFilePath) as f:
            lines = f.read().split("\n")
        for line in lines:
            line = line.strip()
            if len(line) < 3:
                continue
            if line.startswith("#"):
                continue
            if not os.path.exists(line):
                line = line.replace(SERVER_XDRIVE_FOLDER,
                                    DEVELOPER_XDRIVE_FOLDER)
            if os.path.exists(line):
                line = os.path.abspath(line)
                if not line in folders:
                    folders.append(line)
            else:
                print("  ERROR: folder does not exist:", line)
        return folders

    def getAbfsNeedingAnalysisInAFolder(self, folderPath):
        abfs = []

        abfFiles = glob.glob(folderPath+"/*.abf")
        abfFiles = [os.path.basename(x) for x in abfFiles]
        abfIDs = [os.path.splitext(x)[0] for x in abfFiles]

        abfGraphs = glob.glob(folderPath+"/"+pyABFauto.AUTOANALYSIS_FOLDER_NAME+"/*.png")
        abfGraphs = [os.path.basename(x) for x in abfGraphs]
        abfGraphList = ",".join(abfGraphs)

        for abfID in abfIDs:
            if not abfID in abfGraphList:
                if not os.path.exists(os.path.join(folderPath, abfID+".rsv")):
                    abfs.append(os.path.join(folderPath, abfID+".abf"))

        return abfs
