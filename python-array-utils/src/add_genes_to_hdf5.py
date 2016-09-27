#!/usr/bin/env python
import numpy as np
import h5py
import argparse

parser = argparse.ArgumentParser(description='merge hdf5 files')
parser.add_argument('hdf5file', type=str, help='HDF5 file')
parser.add_argument('outFileName', type=str, help='Output filename')
parser.add_argument('--gene-names', type=file, help='Genes file, with one gene per line')
parser.add_argument('--genes-bedfile', type=file, help='Genes file, with one gene per line')
parser.add_argument('--gene-name-max-len', type=int, default=20, help='Genes file, with one gene per line')

args = parser.parse_args()

np_str = 'S%d' % args.gene_name_max_len
if args.genes_bedfile:
    genes = np.loadtxt(args.genes_bedfile, dtype=np_str)[:, 3]
else:
    try:
        genes = np.loadtxt(args.gene_names, dtype=np_str)
    except ValueError, e:
        print '[ERROR] Either gene-names or genes-bedfile should be provided'
        import sys
        sys.exit(1)

f = h5py.File(args.hdf5file, 'r')
fd = h5py.File(args.outFileName, 'w')
f.copy('reads', fd)
f.close()

fd.create_dataset('genes', genes.shape, data=genes, dtype=np_str, compression='gzip', compression_opts=9)
fd.close()