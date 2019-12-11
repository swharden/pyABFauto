"""
This script finds all autoanalysis folders named "swhlab" 
so they can ultimately be renamed to "_autoanalysis" (if they contain ABF analysis data)
"""

import os

logFile = os.path.join(os.path.dirname(__file__), "oldPaths.txt")


def locateAutoanalysisFolders(rootPath, oldName="swhlab"):
    dirCount = 0
    os.remove(logFile)
    with open(logFile, 'a') as f:
        for dirPath, subdirList, fileList in os.walk(rootPath):
            if os.path.basename(dirPath).lower() == oldName.lower():
                dirCount += 1
                print(f"{dirCount}: {dirPath}")
                f.write(dirPath+"\n")
    print(f"wrote: {logFile}")


if __name__ == "__main__":
    locateAutoanalysisFolders(r"D:\X_Drive\Data")
