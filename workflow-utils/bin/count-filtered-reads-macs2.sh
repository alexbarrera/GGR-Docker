#!/bin/bash

grep -m 1 -E "(tags|fragments) after filtering in treatment" $1 | awk '{print $NF}'