import os

sourceDir = "/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 11 - system access/tiff_test"
fileNames = os.listdir(sourceDir)
nameSizePairs = []

for fileName in fileNames:
    fileName = fileName.strip()
    if fileName.endswith(".tif"):
        size = os.path.getsize(sourceDir + "/" + fileName)
        nameSizePairs.append((fileName, size))

nameSizePairs.sort(key=lambda s: s[1], reverse=True)
print nameSizePairs[nameSizePairs.index(max(nameSizePairs))]