#!/usr/bin/env python
import numpy as np
import h5py
import argparse

# Assume all arrays are same dimensions

parser = argparse.ArgumentParser(description='merge hdf5 files')
parser.add_argument('-files', type=str, nargs='+')
parser.add_argument('-out', type=str, help='output file name')

args = parser.parse_args()

out = args.out
if not out.endswith('.h5'):
    out += '.h5'

mats = []
for f in args.files:
    fi = h5py.File(f, 'r')
    mats.append(fi['reads'][:])    
    fi.close()
M = np.stack(mats, 1)

f = h5py.File(out, 'w')
f.create_dataset('reads', M.shape, data=M, dtype='i', compression='gzip', compression_opts=9)
f.close()