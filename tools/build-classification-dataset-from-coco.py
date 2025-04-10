"""
Considering json annotation files in the COCO format in a given directory, this script will take every single image,
crop every rotated bounding box and save the cropped image in a directory named by the category.

Input:
    - annotation_dir/file1.json
    - annotation_dir/file2.json

Output:
    - images/category1/image1_crop1.jpg
    - images/category2/image1_crop2.jpg

The annotation files contain the keys "images", "categories", "annotations"

The "images" key is like :
        "images": [
        {
            "height": 1542,
            "width": 2080,
            "id": 3426554,
            "file_name": "02049900_2020_img220610_001.JPG",
            "longitude": null,
            "latitude": null
        },
        ...


The "categories" key is like :
      "categories": [
        {
            "id": 295717,
            "name": "Broken valve"
        },
        {
            "id": 295718,
            "name": "TERATO"
        },
        ..

The "annotations" key is like :

       "annotations": [
        {
            "segmentation": [
                [
                    1007.42,
                    687.48,
                    1294.22,
                    560.97,
                    1262.55,
                    489.18,
                    975.75,
                    615.69,
                    1007.42,
                    687.48
                ]
            ],
            "iscrowd": 0,
            "area": 63152.60100000001,
            "image_id": 3426779,
            "bbox": [
                975.75,
                489.18,
                318.47,
                198.3
            ],
            "category_id": 295719,
            "id": 25053788
        },
        {
            "segmentation": [
                [
                    945.42,
                    730.83,
                    1150.34,
                    741.7,
                    1153.91,
                    674.4,
                    948.99,
                    663.53,
                    945.42,
                    730.83
                ]
            ],
            "iscrowd": 0,
            "area": 16297.663300000026,
            "image_id": 3426554,
            "bbox": [
                945.42,
                663.53,
                208.49000000000012,
                78.17000000000007
            ],
            "category_id": 295719,
            "id": 25053798
        },

The crop is using the oriented bounding box defined by the "segmentation" key.
"""

# Standard imports
import glob
import sys
import os
import pathlib

# External imports
import json
import cv2
import numpy as np


def process_annotation_file(
    annotation_file, base_image_dir: pathlib.Path, output_dir: pathlib.Path
):
    """
    Process a single annotation file and save the cropped images in the output directory.
    """
    with open(annotation_file, "r") as f:
        data = json.load(f)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

    # Create a dictionary to map category_id to category_name
    category_dict = {cat["id"]: cat["name"] for cat in data["categories"]}

    # Create a dictionary to map image_id to file_name
    image_dict = {img["id"]: img["file_name"] for img in data["images"]}

    # Create a directory for each category
    for cat in category_dict.values():
        os.makedirs(os.path.join(output_dir, cat), exist_ok=True)

    # Process each annotation
    for ann in data["annotations"]:
        image_id = ann["image_id"]
        category_id = ann["category_id"]
        segmentation = ann["segmentation"][0]

        # Get the file name of the image
        file_name = image_dict[image_id]

        # Read the image
        img_path = base_image_dir / file_name
        img = cv2.imread(str(img_path))

        # Get the coordinates of the bounding box
        points = np.array(segmentation).reshape(-1, 2).astype(np.int32)

        # Get the angle of the poygon
        (xc, yc), (width, height), angle = cv2.minAreaRect(points)
        xc = int(xc)
        yc = int(yc)
        width = int(width)
        height = int(height)
        # cv2.circle(img, (xc, yc), 5, (0, 255, 0), -1)

        # # Draw the bounding box from the points
        # cv2.polylines(img, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        # cv2.imshow("Image", img)
        # cv2.waitKey(0)

        M = cv2.getRotationMatrix2D((xc, yc), angle - 90, 1)
        rotated = cv2.warpAffine(img, M, img.shape[1::-1], flags=cv2.INTER_CUBIC)

        # cv2.imshow("Image", rotated)
        # cv2.waitKey(0)

        cropped = cv2.getRectSubPix(rotated, (height, width), (xc, yc))

        # cv2.imshow("Cropped Image", cropped)
        # cv2.waitKey(0)

        # Save the cropped image
        category_name = category_dict[category_id]
        output_path = output_dir / category_name / f"{file_name}_{ann['id']}.jpg"

        cv2.imwrite(str(output_path), cropped)


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print(
            "Usage: python build-classification-dataset-from-coco.py annotation_dir base_image_dir output_dir"
        )
        sys.exit(1)

    annotation_dir = sys.argv[1]
    base_image_dir = pathlib.Path(sys.argv[2])
    output_dir = pathlib.Path(sys.argv[3])

    # List all the json files in the annotation_dir
    json_files = glob.glob(annotation_dir + "/*.json")

    # Process each json file
    for json_file in json_files:
        process_annotation_file(json_file, base_image_dir, output_dir)
