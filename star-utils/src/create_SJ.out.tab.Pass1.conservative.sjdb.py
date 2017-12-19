#!/usr/bin/env python
##################################################
#  create_SJ.out.tab.Pass1.conservative.sjdb.py
#
#  Merge the STAR 1-pass novel splice junction databases ('SJ.out.tab').
#  Save only those splice junctions in autosomes and sex chromosomes.  
#  Filter out splice junctions that are non-canonical,
#  supported by only 10 or fewer reads.
#
##################################################
import pandas as pd
from collections import defaultdict
from sys import argv

SJ_DBs = argv[1].split(',')
SJ_DB_out = argv[2]

# samples = [s.replace(base, '').replace(suffix, '') for s in SJ_DBs]

# canonical_chroms = set(['chr'+str(x) for x in range(1,24)])
# canonical_chroms.add('chrX')
# canonical_chroms.add('chrY')

strand_dict = {}
strand_dict[0],strand_dict[1],strand_dict[2] = '.','+','-'

# SJ.out.tab format:
    
# Column 1: chromosome
# Column 2: first base of the intron (1-based)
# Column 3: last base of the intron (1-based)
# Column 4: strand
# Column 5: intron motif: 0: non-canonical; 1: GT/AG, 2: CT/AC, 3: GC/AG, 4: CT/GC, 5: AT/AC, 6: GT/AT
# Column 6: reserved
# Column 7: number of uniquely mapping reads crossing the junction
# Column 8: reserved
# Column 9: maximum left/right overhang 

splice_dict = defaultdict(dict)
for i,  SJ_DB in enumerate(SJ_DBs):
    columns = ['chrom','start','end','strand','intron_motif','reserved','num_uniq_mapped_reads','reserved','left/right_overhang']
    SJ_DB = pd.read_csv(SJ_DB, delim_whitespace=True, header=None, names = columns)
    # filter out non-canonical splice juntions
    SJ_DB = SJ_DB[SJ_DB.intron_motif != 0]
    # filter out splice junctions without support of greater than 1 unique read
    SJ_DB = SJ_DB[SJ_DB.num_uniq_mapped_reads > 1]
    SJ_DB['strand'] = [strand_dict[strand] for strand in SJ_DB['strand']]
    for chrom, start, end, strand in zip(SJ_DB.chrom, SJ_DB.start, SJ_DB.end, SJ_DB.strand):
        if (chrom,start,end,strand) in splice_dict:
            splice_dict[(chrom,start,end,strand)] += 1
        else:
            splice_dict[(chrom,start,end,strand)] = 1

splice_sites = splice_dict.keys()
splice_sites = sorted(splice_sites, key=lambda s: int(s[1]))
splice_sites = sorted(splice_sites, key=lambda s: s[0][3:])
# splice_sites = [splice_site for splice_site in splice_sites if splice_site[0] in canonical_chroms]

splice_sites = ['\t'.join([str(x) for x in splice_site]) for splice_site in splice_sites]
out = open(SJ_DB_out,'w')
out.write('\n'.join(splice_sites) + '\n')
out.close()
