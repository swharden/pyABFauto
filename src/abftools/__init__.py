import os
import glob
import shutil

def importAbfs(folderSource, folderDestination):
    """
    Import ABF files from a source location to a destination.
    Also imports TIF files with similar filenames.
    """
    assert os.path.isdir(folderSource)    
    assert os.path.isdir(folderDestination)
    print("\nScanning folder for ABF and TIF files:", folderSource)
    allFiles = os.listdir(folderSource)
    abfFiles = [x for x in allFiles if x.lower().endswith(".abf")]
    tifFiles = [x for x in allFiles if x.lower().endswith(".tif")]
    for abfFile in abfFiles:
        abfid = abfFile[:-4]
        print("copying ABF:", abfid)
        shutil.copy(os.path.join(folderSource, abfFile), os.path.join(folderDestination, abfFile))
        for tifFile in tifFiles:
            if tifFile.startswith(abfid):
                print("copying TIF:", abfid)
                shutil.copy(os.path.join(folderSource, tifFile), os.path.join(folderDestination, tifFile))
    return

def getFoldersFromAbfFileList(filename):
    """
    Given a text file containing many ABF files, return a list of the
    folders containing these ABF files.
    """
    folders = []
    with open(filename) as f:
        lines = f.read().split("\n")
    lines = [x.strip() for x in lines]
    for line in lines:
        if line.endswith(".abf"):
            folder = os.path.dirname(line)
            if os.path.isdir(folder):
                folders.append(folder)
    folders = sorted(list(set(folders)))
    return folders

if __name__=="__main__":
    print("WARNING: DO NOT RUN THIS SCRIPT DIRECTLY")

    print("DONE")