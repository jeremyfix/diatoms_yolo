# coding: utf-8

# Standard imports
import sys
import glob

# External imports
from ultralytics.data.converter import convert_coco

if len(sys.argv) != 3:
    print("Usage: python convert-coco-to-yolo.py <src-ann-dir> <target-ann-dir>")
    sys.exit(1)

src_ann_dir = sys.argv[1]
target_ann_dir = sys.argv[2]


convert_coco(
    labels_dir=src_ann_dir,
    save_dir=target_ann_dir,
    use_segments=True,
    use_keypoints=False,
    cls91to80=False,
)
