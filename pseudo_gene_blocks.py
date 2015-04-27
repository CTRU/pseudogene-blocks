#!/usr/bin/python
import sys
import getopt
import pprint
pp = pprint.PrettyPrinter(indent=4)

sys.path.append('/software/lib/python2.7/site-packages/pysam-0.7.5-py2.7-linux-x86_64.egg/')
import pysam

letters = 'b:' # the : means an argument needs to be passed after the letter
opts, extraparams = getopt.getopt(sys.argv[1:], letters) 

for o,p in opts:
  if o in ['-b']:
     bam_file = p

verbose = 0

MIN_MAPQ = 10
MIN_ALIGNED_LENGTH = 50

samfile = pysam.Samfile( bam_file, "rb" )

pseudo_block_chr   = 0
pseudo_block_start = 0
pseudo_block_pre   = 0


#for x in samfile.pileup( '7', 6011362, 6028979):
for x in samfile.pileup( ):

  pileup_chr   = samfile.getrname(x.tid)
  pileup_pos   = x.pos

  total_reads    = 0
  low_qual_reads = 0
  diff_chr_reads = 0

  # while the read start is larger than the bed block end read in new blocks.

  for read in x.pileups:
    if (read.alignment.is_unmapped ):
      continue

    total_reads += 1

    if ( read.alignment.mapq <= MIN_MAPQ ):
      low_qual_reads += 1
    elif (read.alignment.rnext != read.alignment.tid ):
      diff_chr_reads += 1


    # if the fraction of reads with low qual or having mates mapped to diff chromosomes are > 20%

    low_qual_reads_fraction = ( low_qual_reads + diff_chr_reads )/total_reads * 100.00;
    if ( low_qual_reads_fraction > 20 ):

      if ( pseudo_block_chr and pseudo_block_chr != pileup_chr ):
        print "\t".join([ pileup_chr, str(pseudo_block_start), str(pseudo_block_pre)])
        pseudo_block_chr   = 0
        pseudo_block_start = 0
        pseudo_block_pre   = 0

      if ( pseudo_block_start and pileup_pos > pseudo_block_pre + 5 ):
        print "\t".join([ pileup_chr, str(pseudo_block_start), str(pseudo_block_pre)])
        pseudo_block_chr   = 0
        pseudo_block_start = 0
        pseudo_block_pre   = 0

      if ( pseudo_block_start == 0 ):
        pseudo_block_chr   = pileup_chr
        pseudo_block_start = pileup_pos
        pseudo_block_pre   = pileup_pos

      pseudo_block_pre   = pileup_pos


if ( pseudo_block_start and pileup_pos > pseudo_block_pre + 1 ):
  print "\t".join([ pileup_chr, str(pseudo_block_start), str(pseudo_block_pre)])

