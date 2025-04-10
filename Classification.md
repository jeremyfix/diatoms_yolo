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


## Cleurie/Orne

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

The list of annotated categories on Cleurie/Orne is given below. It contains 190
labels.

```
"ACAF"
"ACLI"
"ACOP"
"ADCT"
"ADEU"
"ADJK"
"ADMI"
"ADMO"
"ADPY"
"ADRI"
"ADSA"
"ADSU"
"AHOF"
"AMID"
"AMLB"
"AOVA"
"APED"
"AUGR"
"Broken valve"
"CAPS"
"CATO"
"CEUG"
"CFON"
"CHAL"
"CINV"
"CLCT"
"CLNT"
"CMEN"
"CMLF"
"COPL"
"CPED"
"CPLA"
"CSNU"
"DEHR"
"DKRA"
"DMES"
"DOBL"
"DOCU"
"DPST"
"DSTE"
"DVUL"
"EEXI"
"EINC"
"ENLB"
"ENMI"
"ENVE"
"ESLE"
"ESOL"
"ETEN"
"FFAM"
"FFVI"
"FGRA"
"FLNZ"
"FPEC"
"FPRU"
"FRCP"
"FRUM"
"FSAP"
"FSBH"
"FSLU"
"FVAU"
"GANG"
"GANT"
"GEXL"
"GIRDLE"
"GITA"
"GMIC"
"GMIN"
"GOLI"
"GOMS"
"GPAR"
"GPLI"
"GPUM"
"GSCI"
"GSPP"
"GTER"
"HCAP"
"HVEN"
"KGES"
"KKOL"
"KPLO"
"LHUN"
"MAAT"
"MADE"
"MAFO"
"MCON"
"MERS"
"MPMI"
"MVAR"
"NAMP"
"NANT"
"NCOM"
"NCPL"
"NCPR"
"NCRY"
"NCTE"
"NDIS"
"NFON"
"NGRE"
"NHAN"
"NHTI"
"NIBU"
"NIFR"
"NIGR"
"NIME"
"NINC"
"NINT"
"NIOG"
"NIPM"
"NIPU"
"NISO"
"NIVA"
"NLAN"
"NLBT"
"NLIN"
"NMEN"
"NMIC"
"NPAD"
"NPAE"
"NPAL"
"NPAT"
"NRAD"
"NRCH"
"NRCS"
"NRHY"
"NSOC"
"NSOL"
"NSTS"
"NTEN"
"NTPT"
"NUMB"
"NVCC"
"NVEN"
"NZAL"
"NZSS"
"NZSS1"
"NZSU"
"PAPH"
"PBIO"
"PCON"
"PDAO"
"PGIB"
"PGRN"
"PHEL"
"PINS"
"PLAU"
"PLFR"
"PLHU"
"PLIG"
"PMCH"
"PMIC"
"PMNT"
"POBL"
"PROH"
"PSAP"
"PSAT"
"PSHO"
"PSIN"
"PSOT"
"PTCO"
"PTDE"
"PTDS"
"PTLA"
"PTSP"
"RABB"
"RPUS"
"RSIN"
"RUNI"
"SANG"
"SBKU"
"SBRE"
"SELS"
"SHAN"
"SLED"
"SLEP"
"SNIG"
"SPIN"
"SPUP"
"SSEM"
"STKR"
"SUMI"
"SURS"
"SURS1"
"SVIT"
"SVNT"
"TERATO"
"TTAB"
"UACU"
"UULN"
"XXXX"
```
