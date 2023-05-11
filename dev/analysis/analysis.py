import pathlib
import pyabf
import pyabf.tools.ap
import pyabf.filter
import numpy as np
import json
import datetime


def _save_json(abf_path: pathlib.Path, values: dict, name: str, version: int):
    analysis_folder = abf_path.parent.joinpath("_autoanalysis")
    abf_id = abf_path.name[:-4]
    json_path = analysis_folder.joinpath(f"{abf_id}.{name}.json")
    values["analysis_version"] = version
    values["analysis_date"] = datetime.datetime.now().isoformat()
    json_object = json.dumps(values, indent=4)
    with open(json_path, 'w') as f:
        f.write(json_object)
    print(f"saved: {json_path}")


def analyze_rmp(abf_path: pathlib.Path):
    abf = pyabf.ABF(abf_path)
    pyabf.filter.gaussian(abf, 1)
    xs = abf.getAllXs()
    ys = abf.getAllYs()
    rmp = np.nanmean(ys)
    values = {"rmp": float(rmp)}
    _save_json(abf_path, values, "rmp", 1)


def analyze_gain(abf_path: pathlib.Path, epoch: int):
    abf = pyabf.ABF(abf_path)

    indexMin = abf.sweepEpochs.p1s[epoch]
    indexMax = abf.sweepEpochs.p2s[epoch]
    indexMid = int((indexMax + indexMin) / 2)

    sec1 = indexMin / abf.dataRate
    sec2 = indexMax / abf.dataRate
    print(f"Analyzing APs between {sec1} and {sec2} sec")

    counts = [None] * abf.sweepCount
    currents = [None] * abf.sweepCount

    for sweep in range(abf.sweepCount):
        abf.setSweep(sweep)
        indexes = pyabf.tools.ap.ap_points_currentSweep(abf)
        indexes = [x for x in indexes if x >= indexMin and x <= indexMax]
        counts[sweep] = len(indexes)
        currents[sweep] = abf.sweepC[indexMid]

    values = {"counts": counts, "currents": currents}
    _save_json(abf_path, values, "gain", 1)


def analyze_all_protocol(folder: pathlib.Path, protocol: str):
    for abf_path in folder.glob("*.abf"):
        print(abf_path)
        abf = pyabf.ABF(abf_path, loadData=False)
        if not protocol in abf.protocol:
            continue
        print("ANALYZING")
        analyze_gain(abf_path, 2)


if __name__ == "__main__":
    path = "X:/Data/zProjects/NTS CSDS/abfs/2023-05-10"
    analyze_all_protocol(pathlib.Path(path), "0143")
