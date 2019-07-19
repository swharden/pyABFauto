# pyABFauto
**The pyABFauto project provides an analysis pipeline for ABF files that requires no human input.** 

When given a new ABF file is seen its header and data are read using [pyABF](https://github.com/swharden/pyABF), its experiment type is automatically determined (using the protocol file name as a hint), the appropriate analyses are performed, and several graphs are created and saved as PNG files. 

When pyABFauto is combined with a dynamic web interface (such as [FlaskABF](https://github.com/swharden/FlaskABF)) and made accessible to the experimenter, the scientist can rapidly assess neuron properties and the outcome of an experiment at rig-time.

## Project status: alpha

This project is currently under development and is not intended to be used by the public. It is made public for reference and as an example application using the latest versions of [pyABF](https://github.com/swharden/pyABF).

An earlier version of byABFauto can be found [here](/dev/pyABFauto-v1).