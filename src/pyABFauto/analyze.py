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
import psutil

import pyABFauto
import pyABFauto.protocols
import pyABFauto.analyses
import pyABFauto.logging
import pyABFauto.analyses.unknown


class TerminalColors:
    YELLOW = '\u001b[33m'
    MAGENTA = '\u001b[35m'
    WHITE = '\u001b[0m'
    CYAN = '\u001b[36m'


def printYellow(message: str):
    print(f"{TerminalColors.YELLOW}{message}{TerminalColors.WHITE}")


def printMagenta(message: str):
    print(f"{TerminalColors.MAGENTA}{message}{TerminalColors.WHITE}")


def printCyan(message: str):
    print(f"{TerminalColors.CYAN}{message}{TerminalColors.WHITE}")


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
    print()
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
    protocolID = abf.protocol

    # manual replacements here for improperly named protocols
    protocolAliases = {
        "SpritzProtocol": "0913",
        "Persistent": "0313",
        "01 0201": "0201",
        "02 0203": "0203",
        "03 0112": "0112",
        "04 0502": "0502",
        "05 0501": "0501",
        "05 0502": "0502",
    }

    for search, replace in protocolAliases.items():
        if search in protocolID:
            protocolID = protocolID.replace(search, replace)

    protocolID = protocolID.split(" ")[0]
    protocolFunctionName = "analyze_%s" % (protocolID)
    protocolFunctionName = protocolFunctionName.replace("-", "_")
    protocolFunctionName = protocolFunctionName.replace(".", "_")

    print(f"Analyzing [{abfPath}] with protocol [{protocolID}]")

    fig = pyABFauto.figure.Figure(abf)
    plt.title(abf.abfID+".abf")
    if hasattr(pyABFauto.protocols, protocolFunctionName):
        analysisFunction = getattr(pyABFauto.protocols, protocolFunctionName)
        try:
            analysisFunction(abf, fig)
        except Exception as e:
            printMagenta(f"EXCEPTION!!!\n{e}\n")
            traceback.print_exc()
            pyABFauto.analyses.unknown.crash(abf, fig)
    else:
        printMagenta(f"WARNING: unknown protocol ({abf.protocol}) " +
                     f"does not have function ({protocolFunctionName})")
        if abf.dataLengthMin > 2:
            pyABFauto.analyses.unknown.continuous(abf, fig)
        else:
            pyABFauto.analyses.unknown.stacked(abf, fig)
    fig.save()
    fig.close()
    plt.close('all')
    gc.collect()
    del(abf.sweepY)
    del(abf.sweepX)
    del(abf)
    printCyan(f"MEMORY: {psutil.Process().memory_info().rss / 1e6} MB")
