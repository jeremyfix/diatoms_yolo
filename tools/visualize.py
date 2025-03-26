# coding: utf-8

"""
This script randomly sample an image with its annotations and display them
"""

# Standard imports
import glob
import sys
import pathlib
import random

# External imports
from ultralytics.data.utils import visualize_image_annotations

if len(sys.argv) != 2:
    print("Usage: python visualize.py <root_dir>")
    print("e.g. python visualize.py data")
    sys.exit(1)


label_map = {  # Define the label map with all annotated class labels.
    0: "diatom",
}

# Get all the image files in the root directory
image_files = glob.glob(f"{sys.argv[1]}/**/*.jpg", recursive=True)
# For every image, with path ending as either root_dir/images/train/filename.jpg or root_dir/images/valid/filename.jpg
# the annotation is in the file root_dir/labels/train/filename.txt or root_dir/labels/valid/filename.txt

# Randomly sample an image and its annotation file
image_file = image_files[random.randint(0, len(image_files) - 1)]
annotation_file = image_file.replace("images", "labels").replace(".jpg", ".txt")

print(image_file, annotation_file)

# Visualize
visualize_image_annotations(
    image_file,
    annotation_file,
    label_map,
)
