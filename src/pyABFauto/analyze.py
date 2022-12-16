"""
Code here determines if ABFs can be analyzed with predefined protocols.
  * If they can, the figure is made with the code defined in protocols.py
  * If the protocol is not recognized, a generic plot is created
"""

import os
import glob
import pathlib
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


class TerminalColors:
    YELLOW = '\u001b[33m'
    MAGENTA = '\u001b[35m'
    WHITE = '\u001b[0m'


def analyzeFolder(folderPath):
    print("analyzing folder:", folderPath)
    for abfPath in glob.glob(folderPath+"/*.abf"):
        rsvFilePath = str(abfPath).replace(".abf", ".rsv")
        if pathlib.Path(rsvFilePath).exists():
            print("skipping ABF with RSV:", rsvFilePath)
            continue
        analyzeAbf(abfPath)


def analyzeAbf(abfPath):
    abfPath = os.path.abspath(abfPath)
    print("analyzing ABF:", abfPath)
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

    if protocolID == "Persistent":
        protocolID = "0313"

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
            print(TerminalColors.MAGENTA)
            print("EXCEPTION!!!")
            print(e)
            traceback.print_exc()
            print(TerminalColors.WHITE)
            pyABFauto.analyses.unknown.crash(abf, fig)
    else:
        print(TerminalColors.MAGENTA)
        print(f"WARNING: unknown protocol ({abf.protocol}) " + 
            f"does not have function ({protocolFunctionName})")
        print(TerminalColors.WHITE)
        if abf.dataLengthMin > 2:
            pyABFauto.analyses.unknown.continuous(abf, fig)
        else:
            pyABFauto.analyses.unknown.stacked(abf, fig)
    fig.save()
    fig.close()
    plt.close('all')
