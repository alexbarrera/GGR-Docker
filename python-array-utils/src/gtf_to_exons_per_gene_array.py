#!/usr/bin/env python
from __future__ import print_function

import argparse
import operator
from collections import defaultdict as dd

import pybedtools as pybd


def featuretype_filter(feature, featuretype):
    if feature[2] == featuretype:
        return True
    return False


def subset_featuretypes(target, feature_fn, featuretype):
    result = target.filter(feature_fn, featuretype).saveas()
    return pybd.BedTool(result.fn).sort().remove_invalid()


def print_out_exons(genes_list):
    for gid, g in sorted(genes_list.iteritems(), key=operator.itemgetter(0)):
        print(g[0]['chrom'],
              g[0]['strand'],
              gid,
              [[int(ee[1]), int(ee[2])] for ee in pybd.BedTool(g).merge(s=True, stream=True)],
              sep='\t')
    return


parser = argparse.ArgumentParser(description='GTF to genes with list of exons tab-delimited file')
parser.add_argument('ifile', type=file, help='GTF input file')
parser.add_argument('--tmp-prefix', type=str, default='pybedtools.', help='Prefix used for tmp files')

args = parser.parse_args()

pybd.settings.tempfile_prefix = args.tmp_prefix  # '/data/reddylab/Alex/tmp/pybedtools.'
ifile = args.ifile  # sys.argv[1]
genome_gtf = pybd.BedTool(ifile).sort().remove_invalid()

exons = subset_featuretypes(genome_gtf, featuretype_filter, 'exon')
last_gene_id = None
fields = None
aux = []
genes_list = dd(list)
last_chrom = None
for e in exons:
    if last_chrom and last_chrom != e.chrom:
        print_out_exons(genes_list)
        last_chrom = e.chrom
        genes_list = dd(list)

    gene_id = e.attrs['gene_id']
    gene_name = e.attrs['gene_name']
    gene_key = "%s(%s)" % (gene_name, gene_id)
    genes_list[gene_key].append(e)
    last_chrom = e.chrom
if last_chrom:
    print('#Printing exons for chromosome:', last_chrom)
    print_out_exons(genes_list)
