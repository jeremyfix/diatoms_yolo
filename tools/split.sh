#!/bin/bash

# Suppose you have a dataset created as :
# rootdir/all/
# Where the all directory contains all the images.


rootdir=/tmp/Classification/

for d in $rootdir/all/* 
do 
	if [ ! -d $d ]; then
		continue
	fi
	species=$(basename $d)
	

	find $d -name "*.jpg" | shuf > $rootdir/list
	split -l $[ $(wc -l $rootdir/list |cut -d" " -f1) * 80 / 100  ]	$rootdir/list $rootdir/list_

	rm -rf $rootdir/train/$species
	mkdir $rootdir/train/$species
	for f in $(cat $rootdir/list_aa)
	do  
		echo "Linking $f"
		ln -s  $f $rootdir/train/$species/$(basename $f)
	done

	rm -rf $rootdir/test/$species
	mkdir $rootdir/test/$species
	for f in $(cat $rootdir/list_ab)
	do  
		echo "Linking $f"
		ln -s  $f $rootdir/test/$species/$(basename $f)
	done
done

