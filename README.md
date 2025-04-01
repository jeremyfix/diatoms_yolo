# diatoms_yolo

Using ultralytics yolo cli to train an object detector for diatoms.

To train yolo on our custom datasets, we need to convert the data to the format
expected by Yolo as documented :

- [https://docs.ultralytics.com/datasets/obb/](https://docs.ultralytics.com/datasets/obb/) for oriented bounding boxes : class_index x1 y1 x2 y2 x3 y3 x4 y4 with normalized x, y (in [0, 1])
- [https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format](https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format) for non oriented bounding boxes, (class_idx, x, y, width, height) with normalized x, y, width, height (in [0, 1])

## Setup

```
python3 -m venv venv
source venv/bin/activate
python -m pip install ultralytics pylabel wandb
```

## Cleurie/Orne dataset

### Layout

The Cleurie/Orne data exported from Bigle has to be restructured and its
annotations must be converted from COCO to yolo.

As a first step, we convert the layout of the data into the following :

```
CleurieOrne
	images
		all
			...
			02085325_2020_img220616_065.JPG
			...
			02089000_2021_img_240513_006.JPG
			...
	labels
		all
			...
			02085325_2020_img220616_065.txt
			...
			02089000_2021_img_240513_006.txt
			...
```

You must first copy all the images, flat, in the images/all subdirectory. Then,
for the labels, 

```
python3 tools/convert-coco-to-yolo.py /opt/Datasets/Diatoms/Bigle/annotations/ tmp/
```

This will create all the label files into `tmp/labels/...`. I then copied all
the annotation files, flat, into the `CleurieOrne/labels/all`. The converter
(which is coming from ultralytics) is creating one subdirectory by coco json
file. You may not need to copy all the annotations, flat, in a single directory,
I do not know.

At this point, we want to visually check our images and annotations are ok. You
can do so running the python script :

```
python3 tools/visualize_obb.py CleurieOrne
```

This will randomly pick one sample and plot the bounding boxes around the
diatoms.

![Example image with its oriented bounding boxes around the diatoms](https://github.com/jeremyfix/diatoms_yolo/blob/main/html/assets/obb.png)

## Atlas dataset
### Layout

The atlas dataset is structured as 36K train images and 4K valid images with the
following layout :

```
dataset101
	train
		annotations
			...
			00894.jpg
			...
		images
			...
			00894.xml
			...
	val
		annotations
		images
```

The annotation format is the Pascal VOC format

```
<annotation>
  <folder>images</folder>
  <filename>00000.png</filename>
  <source>
    <database>dataset01/</database>
  </source>
  <size>
    <width>1000</width>
    <height>1000</height>
    <depth>1</depth>
  </size>
  <object>
    <name>diatom</name>
    <bndbox>
      <xmin>444</xmin>
      <ymin>608</ymin>
      <xmax>536</xmax>
      <ymax>696</ymax>
    </bndbox>
  </object>
  <object>
   ...
```

### Conversion in yolo format

We begin by creating the directory layout

```
mkdir -p data/images
mkdir -p data/labels
```

To convert the images layout, we just symlink to the original images :

```
export ORIGINAL_DATA_DIR=/original/directory
ln -s $ORIGINAL_DATA_DIR/train/images data/images/train
ln -s $ORIGINAL_DATA_DIR/val/images data/images/val
```


As a sanity check, the following command will count the number of images for
training and validation

```
ls -l data/images/train/ | wc -l
ls -l data/images/valid/ | wc -l
```

For the **labels**, we need to translate the xml into (class_idx, x, y, width, heigh)
coordinates, normalized by the image widths and heights. For now, let us use
[pylabel](https://github.com/pylabel-project/pylabel) but it should not be too
difficult to write your own converter.

```
python tools/convert-voc-to-yolo.py $ORIGINAL_DATA_DIR/train/annotations data/labels/train/
python tools/convert-voc-to-yolo.py $ORIGINAL_DATA_DIR/valid/annotations data/labels/val/ 
```

It should take 10 minutes pour 40k annotations.


## Training

To allow wandb logging, see the ultralytics doc
[https://docs.ultralytics.com/integrations/weights-biases/#installation](https://docs.ultralytics.com/integrations/weights-biases/#installation)

```
yolo settings wandb=True
wandb login YOUR_API_KEY
```

To train a yolov11n on the data : 

```
yolo detect train data=./data/data.yaml model=yolo11n.yaml project=atlas
```

## Inference

To test the predictions on an image, 

```
yolo detect predict model=best.pt source=/path/to/image
```

# Troubleshoots

## no labels found

For some reasons, and this may be due to the fact that images added to the dataset with symbolic links, yolo may fail to
locate the labels related to the images. When I was debugging this, I had the right directory structure but I believe
yolo is computing the labels path using the real image path. 

To solve this, instead of doing symlinks, I copied the image files and this solved the problem.


