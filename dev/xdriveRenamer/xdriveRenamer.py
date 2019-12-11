"""
This script finds all autoanalysis folders named "swhlab" 
so they can ultimately be renamed to "_autoanalysis" (if they contain ABF analysis data)
"""

import os
import glob

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


def numberOfAbfsInFolderAbove(folderPath):
    assert os.path.isdir(folderPath)
    folderAbovePath = os.path.dirname(folderPath)
    abfPaths = glob.glob(folderAbovePath+"/*.abf")
    return len(abfPaths)


def renameFolders(newFolderName="_autoanalysis"):
    with open(logFile) as f:
        folderPaths = f.readlines()
    for path in folderPaths:
        path = path.strip()
        path = path.replace("D:\X_Drive", "X:")

        if not os.path.isdir(path):
            continue

        if len(os.listdir(path)) == 0:
            print(f"DELETING EMPTY: {path}")
        elif numberOfAbfsInFolderAbove(path) > 0:
            newPath = os.path.join(os.path.dirname(path), newFolderName)
            print(f"RENAMING: {path}")
            print(f"          {newPath}")
            os.rename(path, newPath)
        else:
            print(f"SKIPPING: {path}")


if __name__ == "__main__":
    # locateAutoanalysisFolders(r"D:\X_Drive\Data")
    renameFolders()
