"""
Code here assists in importing ABF and TIF files from numerous different folders
all into a central folder so modern tools (e.g., parent/child grouping in Origin)
can be used for analysis.
"""

import os
import sys
import glob

os.chdir(os.path.dirname(__file__))
sys.path.append("../../src/")
import abftools

# define where all the ABFs will go
FOLDER_DATA = R"X:\Data\SD\PFC Oxytocin\Sarthaks PhD project\data"

def import_abfs_by_reading_text_file():
    """import all ABFs and TIFs based on groups.txt"""

    # read the groups file to get a list of folders containing the ABFs of interest
    folders = abftools.getFoldersFromAbfFileList(R"X:\Data\SD\PFC Oxytocin\Sarthaks PhD project\groups.txt")

    # copy all ABFs (and TIFs) from each of those folders into the central data folder
    for folder in folders:
        abftools.importAbfs(folder, FOLDER_DATA)   

def fix_tif_parent_filenames_DOS(abfFolder):
    """
    Parents are defined as ABF and TIF files with the same filename.
    16429016.abf and 16429016_cell1.tif are NOT valid filenames to define a parent.
    This function identifies tifs like this and renames then appropriately.
    WARNING: this function only works for 8-character DOS filenames (smh)
    """
    for tifFileName in glob.glob(abfFolder+"/*.tif"):
        basename = os.path.basename(tifFileName)
        basenameWithoutExt = basename[:-4]
        expectedAbfFilename = basenameWithoutExt+".abf"
        basenameWithoutExtShort = basenameWithoutExt[:8]
        expectedAbfFilenameShort = basenameWithoutExtShort+".abf"
        if not os.path.exists(os.path.join(abfFolder, expectedAbfFilename)):
            if os.path.exists(os.path.join(abfFolder, expectedAbfFilenameShort)):
                tifFileName2 = expectedAbfFilenameShort.replace(".abf", ".TIF")
                if not os.path.exists(os.path.join(abfFolder, tifFileName2)):
                    print(basename, "->", tifFileName2)
                    os.rename(os.path.join(abfFolder, basename), os.path.join(abfFolder, tifFileName2))
            else:
                print("can't find", expectedAbfFilename)

if __name__=="__main__":
    #import_abfs_by_reading_text_file()
    fix_tif_parent_filenames_DOS(FOLDER_DATA)
    print("DONE")