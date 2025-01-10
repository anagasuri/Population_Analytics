#!/bin/bash

# run the script
python3 generate_dirty_data.py

## clean the file 
# remove comments and empty lines
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | \

# remove extra commans and keep essential columns
sed 's/,,*/,/g' | cut -d ',' -f 1,2,4,5,6 | \

# walking speed between 2.0 and 8.0
awk -F ',' '$5 >= 2.0 && $5 <= 8.0' > ms_data.csv

## create insurance list file
# create insurance tiers in insurance.lst
echo -e "insurance_type\nLower\nMiddle\nHighest" > insurance.lst

## summary of clean data 
# count number of total visits not including rows, not including the header
echo "Total number of visits: $(tail -n +2 ms_data.csv | wc -l)"

# display first few records
echo "First few records:" 
head -n 5 ms_data.csv
