"""
The Figure class is how automatic figures are generated.
Customize styling here.
"""

import os
import pyabf
import matplotlib
import matplotlib.pyplot as plt
import pyABFauto
import numpy as np

matplotlib.use("Agg")


class Figure:
    def __init__(self, abf):
        assert isinstance(abf, pyabf.ABF)
        self.abf = abf
        self._setup()

    def sweepColor(self,  reverse=False):
        # colormap = plt.get_cmap("rainbow")

        # quantized colors from turbo with yellow omitted
        # https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html
        colormap = matplotlib.colors.LinearSegmentedColormap.from_list(
            name="custom",
            colors=["#466be3", "#29bbec", "#30f199",
                    "#edd03a", "#fb8023", "#d23104"])

        sweepCount = len(self.abf.sweepList)
        sweepCount = max(sweepCount, 2)
        sweepFraction = self.abf.sweepNumber / (sweepCount - 1)
        color = colormap(sweepFraction)
        return color

    def _setup(self):
        plt.figure(figsize=(8, 6))

    def labelAxes(self):
        plt.ylabel(self.abf.sweepLabelY)
        plt.xlabel(self.abf.sweepLabelX)

    def plotStacked(self, vertOffset=0, alpha=.5):
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber)
            plt.plot(self.abf.sweepX, self.abf.sweepY + vertOffset * sweepNumber,
                     color=self.sweepColor(), alpha=alpha)
        plt.margins(0, .05)
        self.labelAxes()

    def plotMean(self, vertOffset=0, alpha=.5):
        values = np.empty((self.abf.sweepCount, len(self.abf.sweepX)))
        for sweepNumber in self.abf.sweepList:
            self.abf.setSweep(sweepNumber)
            values[sweepNumber] = self.abf.sweepY
        mean = np.mean(values, 0)
        plt.plot(self.abf.sweepX, mean)
        plt.margins(0, .05)
        plt.grid(alpha=.5)
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

    def shadeBackground(self, message="WARNING: unsupported protocol"):
        for i, ax in enumerate(plt.gcf().axes):
            ax.set_facecolor((1.0, 0.9, 0.9))
            t = ax.text(.97, .97, message,
                        transform=plt.gca().transAxes,
                        verticalalignment='top',
                        horizontalalignment='right',
                        fontsize=22,
                        family='monospace',
                        color='k')
            t.set_bbox(dict(facecolor='#FFFF00', edgecolor='k', lw=2))

    def drawAxisCenterText(self, message: str):
        plt.gca().text(x=.5,
                       y=.5,
                       s=message,
                       transform=plt.gca().transAxes,
                       verticalalignment='center',
                       horizontalalignment='center',
                       fontsize=120,
                       fontweight=800,
                       color='k',
                       alpha=.1)

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
