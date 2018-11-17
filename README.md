# pyABFauto
The pyABFauto project seeks to provide an analysis pipeline for ABF files (containing whole-cell patch-clamp electrophysiology data) that requires no human input. When given an ABF file, its header and data will be read using [pyABF](https://github.com/swharden/pyABF), its experiment type will be automatically determined, the appropriate analysis performed, and several graphs of the data will be saved as PNG files. When combined with a dynamic web interface, this allows the experimenter to rapidly assess the outcome of an experiment at rig-time.
