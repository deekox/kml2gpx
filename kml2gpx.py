import os
import sys
from zipfile import ZipFile
import xml.etree.ElementTree as ET

usageString=f"usage: {sys.argv[0]} <kml/kmz file> [output_file_name]"

if __name__ != "__main__":
    print(usageString)
    exit(1)

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print(usageString)
    exit(1)

inputFilePath=sys.argv[1]
outputFilePath=""
if len(sys.argv) == 2:
    outputFilePath = os.path.basename(os.path.splitext(os.path.basename(inputFilePath))[0]) + ".gpx"
elif sys.argv[2].endswith(".gpx"):
    outputFilePath = sys.argv[2]
else:
    outputFilePath = sys.argv[2] + ".gpx"

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
coordinates = root.find('ns:Document/ns:Placemark/ns:LineString/ns:coordinates', namespaces)
if coordinates != None:
    newRoot = ET.Element('gpx')
    gtrk = ET.SubElement(newRoot, 'trk')
    trkSeg = ET.SubElement(gtrk, 'trkseg')
    for line in coordinates.text.splitlines():
        if len(line) > 0:
            vals = line.strip().split(',')
            if len(vals) >= 2:
            # print(f">>{line}<<, len: {len(line)}  len(vals)= {len(vals)}")
            #   print(f"{vals[0]}   {vals[1]}") 
              trkpt = ET.SubElement(trkSeg, "trkpt")
              trkpt.set("lon", vals[0])
              trkpt.set("lat", vals[1])
    tree = ET.ElementTree(newRoot)
    tree.write(outputFilePath)
else:
    print("Unable to find <coordinates> element in .klm file. Giving up :(")
    sys.exit(1)

