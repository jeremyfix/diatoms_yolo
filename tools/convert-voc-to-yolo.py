# coding: utf-8

# Standard imports
import sys
import glob

# External imports
from pylabel import importer

if len(sys.argv) != 3:
    print("Usage: python convert-voc-to-yolo.py <src-ann-dir> <target-ann-dir>")
    sys.exit(1)

src_ann_dir = sys.argv[1]
target_ann_dir = sys.argv[2]

# Get all the xml files in the source directory
dataset = importer.ImportVOC(path=src_ann_dir)
dataset.export.ExportToYoloV5(output_path=target_ann_dir)
