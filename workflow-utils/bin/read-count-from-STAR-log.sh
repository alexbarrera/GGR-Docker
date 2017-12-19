#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <STAR log>"
    exit 1
fi

reads_processed=$(($(grep 'Number of input reads' $1 | cut -f 2) * 2))
reads_mapped_uniquely=$(($(grep "Uniquely mapped reads number" $1 | cut -f 2 )  * 2))
reads_mapped_multiply=$(($(grep "Number of reads mapped to multiple loci" $1 | cut -f 2 )  * 2))
echo -e $reads_processed"\t"$reads_mapped_uniquely"\t"$reads_mapped_multiply
