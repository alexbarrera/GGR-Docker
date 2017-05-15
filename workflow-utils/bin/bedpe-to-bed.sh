#!/bin/bash

awk -F'\t' 'BEGIN{OFS=FS}{print $1,$2,$3,$7,$8,$9; print $4,$5,$6,$7,$8,$9}' $1