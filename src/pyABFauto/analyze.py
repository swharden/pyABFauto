"""
Code here determines if ABFs can be analyzed with predefined protocols.
  * If they can, the figure is made with the code defined in protocols.py
  * If the protocol is not recognized, a generic plot is created
"""

import os
import glob
import pyabf
import matplotlib.pyplot as plt

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
    abf = pyabf.ABF(abfPath)
    protocolID = abf.protocol.split(" ")[0]

    # manual replacements here for improperly named protocols
    if protocolID == "SpritzProtocol-10s-ISI":
        protocolID = "jefftau"

    protocolFunctionName = "analyze_%s" % (protocolID)
    protocolFunctionName = protocolFunctionName.replace("-", "_")
    protocolFunctionName = protocolFunctionName.replace(".", "_")

    print()
    print(f"Analyzing [{abfPath}] with protocol [{protocolID}]")

    fig = pyABFauto.figure.Figure(abf)
    plt.title(abf.abfID+".abf")
    if hasattr(pyABFauto.protocols, protocolFunctionName):
        analaysisFunction = getattr(pyABFauto.protocols, protocolFunctionName)
        analaysisFunction(abf, fig)
    else:
        print(f"WARNING: unknown protocol ({abf.protocol}) needs function ({protocolFunctionName})")
        if abf.dataLengthMin > 2:
            pyABFauto.analyses.unknown.continuous(abf, fig)
        else:
            pyABFauto.analyses.unknown.stacked(abf, fig)
    fig.save()
    fig.close()