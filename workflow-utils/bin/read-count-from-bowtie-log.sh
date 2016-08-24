#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <bowtie log>"
    exit 1
fi

reads_processed=$(grep 'reads processed' $1 | cut -f 4 -d ' ')
reads_mapped=$(grep 'Reported' $1 | cut -f 2 -d ' ')
if grep -q "paired-end" $1; then
    echo -e $(($reads_processed*2)) "\t" $(($reads_mapped*2))
else
    echo -e $reads_processed"\t"$reads_mapped
fi