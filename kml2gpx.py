from genericpath import isfile
import os
import sys

usageString=f"usage: {sys.argv[0]} <kml/kmz file> [output_file_name]"

if __name__ != "__main__":
    print(usageString)
    exit(1)

print(f"len(sys.argv)={len(sys.argv)}")

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

print(f"input {inputFilePath}\noutput: {outputFilePath}")
