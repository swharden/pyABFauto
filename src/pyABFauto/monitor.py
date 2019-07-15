"""
Code here allows directories to be monitored for new ABFs
and analyzed as they appear on disk.
"""

import os
import glob

import pyABFauto


class folderMonitor:
    def __init__(self, folderPath):
        self.folders = []
        self.addFolder(folderPath)

    def analyzeAll(self):
        abfs = self.abfsNeedingAnalysis()
        for abf in abfs:
            self.analyze(abf)

    def analyzeNext(self):
        abfs = self.abfsNeedingAnalysis()
        if len(abfs):
            self.analyze(abfs[0])

    def analyze(self, abfPath):
        pyABFauto.autoAnalyze.analyze(abfPath)

    def _abfsNeedingAnalysisInAFolder(self, folderPath):
        abfs = []

        abfFiles = glob.glob(folderPath+"/*.abf")
        abfFiles = [os.path.basename(x) for x in abfFiles]
        abfIDs = [os.path.splitext(x)[0] for x in abfFiles]

        abfGraphs = glob.glob(folderPath+"/swhlab/*.png")
        abfGraphs = [os.path.basename(x) for x in abfGraphs]
        abfGraphList = ",".join(abfGraphs)

        for abfID in abfIDs:
            if not abfID in abfGraphList:
                abfs.append(os.path.join(folderPath, abfID+".abf"))

        return abfs

    def abfsNeedingAnalysis(self):
        abfs = []
        for folderPath in self.folders:
            abfs += self._abfsNeedingAnalysisInAFolder(folderPath)
        return abfs

    def addFolder(self, folderPath):
        assert os.path.isdir(folderPath)
        folderPath = os.path.abspath(folderPath)
        if not folderPath in self.folders:
            self.folders.append(folderPath)
            print(f"added folder to watch list: {folderPath}")

    def __repr__(self):
        return f"folderMonitor watching {len(self.folders)} folders ({len(self.abfsNeedingAnalysis())} ABFs need analysis)"
