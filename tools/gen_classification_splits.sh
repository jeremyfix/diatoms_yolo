#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <diatoms_dir>"
	exit 1
fi

# diatoms_dir must contain the images within a all/ directory
diatoms_dir="$1"
num_min_samples=10

cd $diatoms_dir || exit 1

# Optional : unlink previously generated split
for d in train test ; do rm -rf $d; done

# Create the train/val dir layout
for d in train test; do mkdir -p $d; done

# Generate the train/val split (80/20) per class and keep only the classes that
# have at least 10 samples
for cls in all/*; do 
	num=$(find $cls -type f | wc -l) 
	cls=$(basename $cls)
	if [ $num -gt $num_min_samples ]; then
		echo "Keeping $cls with $num samples"

		# Create the train/val split
		mkdir -p train/$cls
		mkdir -p test/$cls

		# Get the list of files in the class directory
		files=$(find $diatoms_dir/all/$cls -type f | shuf)

		# Split the files into train and test sets
		num_files=$(echo "$files" | wc -l)
		num_train=$((num_files * 80 / 100))
		num_test=$((num_files - num_train))
		echo "$files" | head -n $num_train | xargs -I {} ln -s {} train/$cls/
		echo "$files" | tail -n $num_test | xargs -I {} ln -s {} test/$cls/
	else
		echo "Excluding $cls with $num samples < $num_min_samples"
	fi
done
