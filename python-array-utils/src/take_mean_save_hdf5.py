#!/usr/bin/env python
import numpy as np
import h5py
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='take mean from numpy arrays and store a gzipped file')
parser.add_argument('-arrays', type=file, nargs='+')
parser.add_argument('-out', type=str, help='output file name')

args = parser.parse_args()

Ms = args.arrays
out = args.out
if not out.endswith('.h5'):
    out += '.h5'
try:
    Ms = [np.load(M) for M in Ms]
except IOError:
    Ms = [pd.read_csv(txt, comment="#", delimiter=' ', skiprows=2, header=None) for txt in args.arrays]
M = np.dstack(Ms).mean(axis=2)

print M.shape

f = h5py.File(out, "w")
f.create_dataset('reads', M.shape, data=M, dtype='i', compression='gzip', compression_opts=9)
f.close()