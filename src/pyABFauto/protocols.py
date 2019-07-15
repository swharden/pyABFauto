"""
ABFs are typically recorded using a saved protocol.
Code here makes different types of plots according to their protocol.
"""

import pyabf
import pyabf.tools

import pyABFauto

def figureByProtocol(abf, fig):
    assert(isinstance(abf, pyabf.ABF))
    assert(isinstance(fig, pyABFauto.figure.Figure))

    if abf.protocol == "0000":
        pass

    elif abf.protocol == "0111 continuous ramp":
        fig.plotContinuous()
        
    elif abf.protocol == "0112 steps dual -50 to 150 step 10":
        fig.plotStacked()

    elif abf.protocol == "0201 memtest":
        #print(pyabf.tools.memtest.step_summary(abf))
        fig.plotStacked()

    elif abf.protocol == "0202 IV dual":
        fig.plotStacked()

    elif abf.protocol == "0203 IV fast":
        fig.plotStacked()

    else:
        # unknown protocol
        if abf.dataLengthMin > 1:
            fig.plotContinuous()
        else:
            fig.plotStacked()
        fig.shadeBackground()