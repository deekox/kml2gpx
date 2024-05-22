import os
import sys
from zipfile import ZipFile
import xml.etree.ElementTree as ET

usageString=f"usage: {sys.argv[0]} <kml/kmz file> [output_file_name]"

def createGPX(coordinates, outputPath):
    newRoot = ET.Element('gpx')
    gtrk = ET.SubElement(newRoot, 'trk')
    trkSeg = ET.SubElement(gtrk, 'trkseg')
    for line in coordinates.text.splitlines():
        if len(line) > 0:
            vals = line.strip().split(',')
            if len(vals) >= 2:
                trkpt = ET.SubElement(trkSeg, "trkpt")
                trkpt.set("lon", vals[0])
                trkpt.set("lat", vals[1])
    tree = ET.ElementTree(newRoot)
    tree.write(outputPath)


if __name__ != "__main__":
    print(usageString)
    exit(1)

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print(usageString)
    exit(1)

inputFilePath=sys.argv[1]
outputFilePath=""
if len(sys.argv) == 2:
    outputFilePath = os.path.basename(os.path.splitext(os.path.basename(inputFilePath))[0])
elif sys.argv[2].endswith(".gpx"):
    outputFilePath = sys.argv[2][:-4]
else:
    outputFilePath = sys.argv[2]


inputFileExtension = os.path.basename(os.path.splitext(os.path.basename(inputFilePath))[1])

if inputFileExtension == ".kmz":
    ZipFile(inputFilePath, 'r').extract('doc.kml')
    inputFilePath = 'doc.kml'

tree = ET.parse(inputFilePath)
root = tree.getroot()
if root == None:
    print("Cannot find root")
    sys.exit(1)

namespaces = { "ns" : root.tag[1:-4] }
cnt = 0
for coordinates in root.findall('ns:Document/ns:Placemark/ns:LineString/ns:coordinates', namespaces):
    cnt = cnt + 1
if cnt == 0:
    print("Unable to find <coordinates> element in .klm file. Giving up :(")
    sys.exit(1)
else:
    i = 1
    for placemark in root.findall('ns:Document/ns:Placemark', namespaces):
        name = placemark.find('ns:name', namespaces)
        filename = outputFilePath + f"_{i}-{cnt}_" + name.text.strip() + ".gpx"
        coordinates = placemark.find('ns:LineString/ns:coordinates', namespaces)
        if coordinates != None:
            createGPX(coordinates, filename)
            i = i + 1


