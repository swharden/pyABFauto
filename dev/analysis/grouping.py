import pathlib
import pyabf


def get_groups(folder_path: pathlib.Path):
    groups_by_parent = {}
    parent = "orphan"
    for abf_file in folder_path.glob("*.abf"):
        tif_file = folder_path.joinpath(abf_file.name[:-4]+".tif")
        if (tif_file.exists()):
            parent = abf_file
        if not parent in groups_by_parent.keys():
            groups_by_parent[parent] = []
        groups_by_parent[parent] += [abf_file]

    return groups_by_parent


def get_next_abf_protocol(parent_abf: pathlib.Path, protocol_id: str) -> pathlib.Path:
    groups = get_groups(parent_abf.parent)
    if not parent_abf in groups.keys():
        raise Exception(f"{parent_abf} is not a parent")
    for child in groups[parent_abf]:
        abf = pyabf.ABF(child, loadData=False)
        if (abf.protocol.startswith(protocol_id)):
            return child
    raise Exception(f"{parent_abf} has no child protocol {protocol_id}")


abf_path = pathlib.Path(
    "X:/Data/zProjects/NTS CSDS/abfs/2023-05-01/2023_05_01_0057.abf")

path = get_next_abf_protocol(abf_path, "0111")
print(path)
