"""
The Figure class is how automatic figures are generated.
Customize styling here.
"""

import os
import pyabf
import matplotlib.pyplot as plt
import pyABFauto


class Figure:
    def __init__(self, abf):
        assert isinstance(abf, pyabf.ABF)
        self.abf = abf
        self._setup()

    def sweepColor(self,  colormap="Dark2", reverse=False):
        colormap = plt.get_cmap(colormap)
        sweepFraction = self.abf.sweepNumber/len(self.abf.sweepList)
        color = colormap(1 - sweepFraction)
        return color

    def _setup(self):
        plt.figure(figsize=(8, 6))

    def labelAxes(self):
        plt.ylabel(self.abf.sweepLabelY)
        plt.xlabel(self.abf.sweepLabelX)

    def plotStacked(self, vertOffset=0):
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber)
            plt.plot(self.abf.sweepX, self.abf.sweepY + vertOffset * sweepNumber,
                     color=self.sweepColor(), alpha=.5)
        plt.margins(0, .05)
        self.labelAxes()

    def plotContinuous(self, startAtSec=0, minutes=False):
        i1 = int(startAtSec * self.abf.dataRate)
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber, absoluteTime=True)
            Xs = self.abf.sweepX[i1:]
            Ys = self.abf.sweepY[i1:]
            if minutes:
                Xs /= 60
            plt.plot(Xs, Ys, color='b', lw=.5)
        plt.margins(0, .05)
        self.labelAxes()
        if (minutes):
            plt.xlabel("time (minutes)")

    def addTagLines(self, minutes=False):
        for i, comment in enumerate(self.abf.tagComments):
            if minutes:
                tagPosition = self.abf.tagTimesMin[i]
            else:
                tagPosition = self.abf.tagTimesSec[i]
            plt.axvline(tagPosition, linewidth=2, color='r',
                        alpha=.5, linestyle='--')

    def shadeBackground(self):
        for i, ax in enumerate(plt.gcf().axes):
            ax.set_facecolor((1.0, 0.9, 0.9))
            t = ax.text(.97, .97, "WARNING: unsupported protocol",
                        transform=plt.gca().transAxes,
                        verticalalignment='top',
                        horizontalalignment='right',
                        fontsize=22,
                        family='monospace',
                        color='k')
            t.set_bbox(dict(facecolor='#FFFF00', edgecolor='k', lw=2))

    def grid(self):
        plt.grid(alpha=.2, color='k', ls='--')

    def _preSaveAdjustments(self, stampFilename=False):
        plt.tight_layout()
        if not stampFilename:
            return
        lowerCornerText = f"{self.abf.abfID}.abf\n{self.abf.protocol}"
        plt.gcf().text(0.005, 0.005, lowerCornerText,
                       transform=plt.gca().transAxes,
                       fontsize=10,
                       family='monospace',
                       verticalalignment='bottom',
                       color='.5')

    def save(self):
        self._preSaveAdjustments()
        outputFolder = os.path.dirname(
            self.abf.abfFilePath) + "/" + pyABFauto.AUTOANALYSIS_FOLDER_NAME
        outputFolder = os.path.abspath(outputFolder)
        if not os.path.exists(outputFolder):
            os.mkdir(outputFolder)
        outputFileName = f"{self.abf.abfID}_autoanalysis.png"
        outputFile = os.path.join(outputFolder, outputFileName)
        plt.savefig(outputFile)
        print("saved:", outputFile)

    def close(self):
        plt.close()
