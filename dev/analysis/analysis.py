import pathlib
import pyabf
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


if __name__ == "__main__":
    abf_path = "X:/Data/zProjects/NTS CSDS/abfs/2023-05-05/2023_05_05_0044.abf"
    abf_path = pathlib.Path(abf_path)
    analyze_rmp(abf_path)
