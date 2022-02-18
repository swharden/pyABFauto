"""
Code here determines if ABFs can be analyzed with predefined protocols.
  * If they can, the figure is made with the code defined in protocols.py
  * If the protocol is not recognized, a generic plot is created
"""

import os
import glob
from posixpath import basename
from random import Random, random
import pyabf
import matplotlib.pyplot as plt
import traceback
import random
import shutil
import tracemalloc
import gc

import pyABFauto
import pyABFauto.protocols
import pyABFauto.analyses
import pyABFauto.logging
import pyABFauto.analyses.unknown


def analyzeFolder(folderPath):
    for abfPath in glob.glob(folderPath+"/*.abf"):
        analyzeAbf(abfPath)


def analyzeAbf(abfPath):
    abfPath = os.path.abspath(abfPath)

    with open(abfPath, 'rb') as f:
        firstFourBytes = f.read(4)
    if str(firstFourBytes) == R"b'MM\x00*'":
        print(f"WARNING: this file is actually a TIF: {abfPath}")
        tifPath = abfPath + "_NotAnABF_" + \
            str(random.random())[2:] + ".tif"
        print(f"Renaming it to: {tifPath}")
        shutil.move(abfPath, tifPath)
        return

    abf = pyabf.ABF(abfPath)
    protocolID = abf.protocol.split(" ")[0]

    # manual replacements here for improperly named protocols
    if "SpritzProtocol" in protocolID:
        protocolID = "0913"

    protocolFunctionName = "analyze_%s" % (protocolID)
    protocolFunctionName = protocolFunctionName.replace("-", "_")
    protocolFunctionName = protocolFunctionName.replace(".", "_")

    print()
    print(f"Analyzing [{abfPath}] with protocol [{protocolID}]")

    fig = pyABFauto.figure.Figure(abf)
    plt.title(abf.abfID+".abf")
    if hasattr(pyABFauto.protocols, protocolFunctionName):
        analaysisFunction = getattr(pyABFauto.protocols, protocolFunctionName)
        try:
            analaysisFunction(abf, fig)
        except Exception as e:
            print("EXCEPTION!!!")
            print(e)
            traceback.print_exc()
            pyABFauto.analyses.unknown.crash(abf, fig)
    else:
        print(
            f"WARNING: unknown protocol ({abf.protocol}) needs function ({protocolFunctionName})")
        if abf.dataLengthMin > 2:
            pyABFauto.analyses.unknown.continuous(abf, fig)
        else:
            pyABFauto.analyses.unknown.stacked(abf, fig)
    fig.save()
    fig.close()
