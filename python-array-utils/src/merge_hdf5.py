#!/usr/bin/env python
import numpy as np
import h5py
import argparse

# Assume all arrays are same dimensions

parser = argparse.ArgumentParser(description='merge hdf5 files')
parser.add_argument('-files', required=True, type=str, nargs='+')
parser.add_argument('-out', required=True, type=str, help='output file name')
parser.add_argument('--stackaxis', default=1, type=int, help='Axis choosen to stack reads in output dataset for HDF5 file.')

args = parser.parse_args()

out = args.out
if not out.endswith('.h5'):
    out += '.h5'

mats = []
for f in args.files:
    fi = h5py.File(f, 'r')
    mats.append(fi['reads'][:])    
    fi.close()
M = np.stack(mats, args.stackaxis)

f = h5py.File(out, 'w')
f.create_dataset('reads', M.shape, data=M, dtype='i', compression='gzip', compression_opts=9)
f.close()