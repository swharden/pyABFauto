
import os
import glob

from PIL import Image
from PIL import ImageOps
from PIL import ImageMath


def convertWithImageMagick(tifFilePath, jpgFilePath, autoContrast=True):
    cmd = "convert \"%s\" \"%s\" " % (tifFilePath, jpgFilePath)
    if autoContrast:
        cmd = cmd.replace("convert", "convert -contrast-stretch .1%x.1%")
    print(cmd)
    os.system(cmd)


def convertTifToJpg(tifFilePath, jpgFilePath, autoContrast=True):
    print("  converting", os.path.basename(tifFilePath), "to jpg...")

    im = Image.open(tifFilePath)

    if im.mode == "F":
        im = ImageMath.eval("convert(a/8, 'L')", a=im)

    if im.mode == "L":
        print("  converting image with PIL")
        if autoContrast:
            im = ImageOps.autocontrast(im, .05)
        im = im.convert('RGB')
        im.save(jpgFilePath)
    else:
        print("  converting image with ImageMagick")
        convertWithImageMagick(tifFilePath, jpgFilePath)


def autoConvertToPNG(tifFilePath: str, pngFilePath: str):
    # ensure AutoTIF is in your system path
    cmd = 'AutoTIF.exe "{tifFilePath}" "{pngFilePath}"'
    print("  " + cmd)
    os.system(cmd)


if __name__ == "__main__":
    print("TEST")
    testIn = R"X:\Data\C57\ECB-pilot\PIR\Jordan\2020_07_01_0005.tif"
    testOut = R"C:\Users\swharden\Documents\temp\test.jpg"
    convertTifToJpg(testIn, testOut)