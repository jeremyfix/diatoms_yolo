#!/bin/bash

# This script takes as input two csv files, an input image directory and a target root dir

# - taxon_to_exclude.csv
# - diatoms_all.csv
# - diatoms_dir/
# - root_dir/

# It distributes the images from the diatoms_dir into the root_dir according to the genus assigned to the image.

# The taxon_to_exclude.csv contains the taxon to ignore. It is a comma separated file with the following columns :
# - Original extraction name
# - Atlas
# - several other columns that are ignored

# The images to be excluded are thos in in the diatoms_dir/<Original extraction name>/<Atlas> directories. In the
# taxon_to_exclude.csv, several consecutive atlas values can be specified. In this case, the Original extraction name is
# not repeated.

# The genus is provided in the diatoms_all.csv comma separated file with the following columns :
# - Column1 : id
# - photo: relative path to the image
# - genus
# - species


# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <taxon_to_exclude.csv> <diatoms_all.csv> <diatoms_dir/> <root_dir/>"
    exit 1
fi

# Assign input arguments to variables
taxon_to_exclude_csv="$1"
diatoms_all_csv="$2"
diatoms_dir="$3"
root_dir="$4"

# Create the root directory if it doesn't exist or remove it if its does. Ask user confirmation if it exists
if [ -d "$root_dir" ]; then
    read -p "The directory $root_dir already exists. Do you want to remove it? (y/n) " choice
    if [ "$choice" == "y" ]; then
        rm -rf "$root_dir"
        mkdir "$root_dir"
    else
        echo "Exiting without removing the directory."
        exit 1
    fi
else
    mkdir "$root_dir"
fi

# Read the taxon_to_exclude.csv file and create an array of excluded taxa
declare -A excluded_taxa
original_extraction_name=""
while read -r line; do
    IFS=';' read -r new_original_extraction_name atlas _ <<< "$line"

    # Skip the header line
    if [[ "$new_original_extraction_name" == "Original extraction name" ]]; then
        continue
    fi
    
    # If the new original extraction name is different from the previous one, update it
    if [ "$new_original_extraction_name" != "" ]; then
        original_extraction_name="$new_original_extraction_name"
    fi

    excluded_taxa["$original_extraction_name,$atlas"]=1
    echo "Excluded: $original_extraction_name, $atlas"
done < "$taxon_to_exclude_csv"

# Read the diatoms_all.csv file and create an array of genus names
# The genus names are used to create directories in the root directory
# While reading the file, we skip the excluded taxa. To decide whether an image must be skipped, we check if the
# filename column is /diatoms/<Original extraction name>/<Atlas>/<filename>.{jpg,png}

declare -A genus_names
while read -r line; do
    IFS=';' read -r id photo genus species _ <<< "$line"

    echo "Processing: $id, $photo, $genus, $species"

    # Skip the header line
    if [[ "$id" == "Column1" ]]; then
        continue
    fi

    # Extract the original extraction name and atlas from the photo path
    original_extraction_name=$(basename "$(dirname "$(dirname "$photo")")")
    atlas=$(basename "$(dirname "$photo")")

    # Check if the current taxon is excluded
    if [[ -n "${excluded_taxa["$original_extraction_name,$atlas"]}" ]]; then
        echo "Excluded: $original_extraction_name, $atlas"
        continue
    fi

    # Create the genus directory if it doesn't exist
    genus_dir="$root_dir/$genus"
    mkdir -p "$genus_dir"

    # Copy the image to the genus directory.
    cp "$diatoms_dir/$photo" "$genus_dir/"

done < "$diatoms_all_csv"

