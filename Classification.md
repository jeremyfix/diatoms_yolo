# Notes for the classification

Dataset description :

- Atlas:
	- 33864 images from atlas
	- 950 taxons, 640 with more than 10 images, 360 with more than 30 images

There is a tag, in addition to the taxon :

- connective: when the diatom is seen from the side; In that, it might be hard
  to determine the label. Proposition to handle it as an additional class
- recadrer : they contain multiple diatoms, better to remove them from the
  training data

Be carefull, there is a scale on the images, and the aspect ratio is important.
We should :

- pad the images to have a given image size with a constant scale, like 10
  pix/micrometer
- pad the images to have a squared image so that the resize for Yolo does not
  break the aspect ratio


The categories semantics for the real dataset (Cleurie/Orne) are given in the JSON from the Biigle annotations.

On the categories :

- Broken valve : the diatom is broken but its taxon might be labeled
- Terato : to be removed
- xxxx: unidentified diatom
- more than 4 letters taxon : the taxon is uncertain, better to remove these

We wish to classify the diatoms :

- at the gender level :  expected accuracy at 100% , super easy
- at the taxon level  

A table will be provied to map the taxon name to the gender.
