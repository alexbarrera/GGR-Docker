#!/bin/bash

awk -F'\t' 'BEGIN{OFS=FS}$5>1000{$5=1000}{print}' $1