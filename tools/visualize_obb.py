# coding: utf-8

"""
Little script to plot an oriented bounding box
"""

# Standard imports
import glob
import sys
import pathlib
import random

# External imports
from ultralytics.utils.plotting import Annotator
import cv2
import numpy as np
import matplotlib.pyplot as plt


def draw_obb(image_path, label_path):
    image = cv2.imread(image_path)
    with open(label_path, "r") as file:
        for line in file:
            parts = line.strip().split()
            cls, points = int(parts[0]), list(map(float, parts[1:]))
            points = [
                (int(points[i] * image.shape[1]), int(points[i + 1] * image.shape[0]))
                for i in range(0, len(points), 2)
            ]
            points = np.array(points, np.int32).reshape((-1, 1, 2))
            cv2.polylines(
                image, [points], isClosed=True, color=(0, 255, 0), thickness=2
            )
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


if len(sys.argv) != 2:
    print("Usage: python visualize.py <root_dir>")
    print("e.g. python visualize.py data")
    sys.exit(1)

# Get all the image files in the root directory
image_files = glob.glob(f"{sys.argv[1]}/**/*.JPG", recursive=True)

# Randomly sample an image and its annotation file
image_file = image_files[random.randint(0, len(image_files) - 1)]
annotation_file = image_file.replace("images", "labels").replace(".JPG", ".txt")

print(image_file, annotation_file)

draw_obb(image_file, annotation_file)
