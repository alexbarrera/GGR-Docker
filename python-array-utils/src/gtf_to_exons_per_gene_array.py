#!/usr/bin/env python

import sys
import pybedtools as pybd
from multiprocessing import Pool


def featuretype_filter(feature, featuretype):
    if feature[2] == featuretype:
        return True
    return False


def subset_featuretypes(target, feature_fn, featuretype):
    result = target.filter(feature_fn, featuretype).saveas()
    return pybd.BedTool(result.fn)


def gene_filter(feature, genename):
    if feature.attrs['gene_id'] == genename:
        return True
    return False


def exons_txt(interval):
    target = genome_gtf
    gene_id = interval.attrs['gene_id']
    gene_name = interval.attrs['gene_name']
    fields = [interval.chrom, interval.strand]
    fields += ["%s(%s)" % (gene_name, gene_id)]
    g = pybd.BedTool(str(interval), from_string=True).saveas()
    feats_in_gene = genome_gtf.intersect(g, s=True)
    gene_exons = subset_featuretypes(feats_in_gene, featuretype_filter, 'exon') \
        .merge(s=True) \
        .remove_invalid()
    aux = [[tt.start, tt.end] for tt in gene_exons]
    fields += [repr(aux)]
    return '\t'.join(fields)


if __name__ == "__main__":

    ifile = sys.argv[1]
    try:
        nprocs = int(sys.argv[2])
    except IndexError:
        nprocs = 1

    genome_gtf = pybd.BedTool(ifile) \
        .sort() \
        .remove_invalid() \
        .saveas()
    genes = subset_featuretypes(genome_gtf, featuretype_filter, 'gene')

    # print header
    print '\t'.join(['chr', 'strand', 'gene', 'exons'])

    pool = Pool(nprocs)

    ll = pool.map(exons_txt, [g for g in genes])

    for l in ll:
        sys.stdout.write(l)
        sys.stdout.write('\n')
