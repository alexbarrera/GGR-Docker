#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <STAR log>"
    exit 1
fi

reads_processed=$(($(grep 'Number of input reads' $1 | cut -f 2) * 2))
reads_mapped=$(($(grep "Uniquely mapped reads number" $1 | cut -f 2 )  * 2))
echo -e $reads_processed"\t"$reads_mapped
