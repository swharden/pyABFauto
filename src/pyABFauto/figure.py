"""
The Figure class is how automatic figures are generated.
Customize styling here.
"""

import os
import pyabf
import matplotlib.pyplot as plt


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

    def plotStacked(self):
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber)
            plt.plot(self.abf.sweepX, self.abf.sweepY,
                     color=self.sweepColor(), alpha=.5)
        plt.margins(0, .05)
        self.labelAxes()

    def plotContinuous(self):
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber, absoluteTime=True)
            plt.plot(self.abf.sweepX, self.abf.sweepY, color='b')
        plt.margins(0, .05)
        self.labelAxes()

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
            ax.text(.97, .97, "WARNING: unknown protocol",
                    transform=plt.gca().transAxes,
                    verticalalignment='top',
                    horizontalalignment='right',
                    fontsize=12,
                    color='r')

    def grid(self):
        plt.grid(alpha=.2, color='k', ls='--')

    def _preSaveAdjustments(self):
        plt.tight_layout()
        lowerCornerText = f"{self.abf.abfID}.abf\n{self.abf.protocol}"
        plt.gcf().text(0.005, 0.005, lowerCornerText,
                       transform=plt.gca().transAxes,
                       fontsize=10,
                       family='monospace',
                       verticalalignment='bottom',
                       color='.5')

    def save(self):
        self._preSaveAdjustments()
        outputFolder = os.path.dirname(self.abf.abfFilePath) + "/swhlab"
        outputFolder = os.path.abspath(outputFolder)
        if not os.path.exists(outputFolder):
            os.mkdir(outputFolder)
        outputFileName = f"{self.abf.abfID}_autoanalysis.png"
        outputFile = os.path.join(outputFolder, outputFileName)
        plt.savefig(outputFile)
        print("  saved:", outputFile)

    def close(self):
        plt.close()
