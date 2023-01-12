import urllib.request


def getRecentFolders(daysBack: int = 1) -> list[str]:
    url = f"http://192.168.1.9/locate/recent/?days={daysBack}"
    text = urllib.request.urlopen(url).read().decode("utf-8")
    folders = []
    for line in text.split("\n"):
        line = line.strip().strip(',').strip('"').replace("\\\\", "\\")
        if not "X:" in line:
            continue
        folders.append(line)
    return folders


def addFoldersToAnalysisFile(folders: list[str]):
    analysisFilePath = R"X:\Lab Documents\network\autoAnalysisFolders.txt"
    with open(analysisFilePath) as f:
        analysisFileText = f.read()
    for folder in folders:
        if folder in analysisFileText:
            continue
        print(f"ADDING AUTO-ANALYSIS FOLDER: {folder}")
        with open(analysisFilePath, 'a') as f:
            f.write(folder + "\n")


def addRecentFoldersToAnalysisFile():
    folders = getRecentFolders()
    addFoldersToAnalysisFile(folders)
