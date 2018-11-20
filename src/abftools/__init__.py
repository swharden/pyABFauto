import os
import glob

def importAbfs(folderSource, folderDestination):
    """
    Import ABF files from a source location to a destination.
    Also imports TIF files with similar filenames.
    """
    assert os.path.isdir(folderSource)    
    assert os.path.isdir(folderDestination)
    allFiles = os.listdir(folderSource)
    abfFiles = [x for x in allFiles if x.lower().endswith(".abf")]
    tifFiles = [x for x in allFiles if x.lower().endswith(".tif")]
    for abfFile in abfFiles:
        abfid = abfFile[:-4]
        print("copying ABF", abfid)
        for tifFile in tifFiles:
            if tifFile.startswith(abfid):
                print("copying TIF:", abfid)
    return

if __name__=="__main__":
    print("WARNING: DO NOT RUN THIS SCRIPT DIRECTLY")
    pathSource = R"C:\Users\scott\Documents\GitHub\pyABF\data\abfs"
    pathDest = R"C:\Users\scott\Documents\temp"
    importAbfs(pathSource, pathDest)
    print("DONE")