import re
import argparse
import pysam
import sys
from collections import defaultdict

"""
    This module adds primer and primer error tags as well as UMI final tag.

Usage::

    add_tags --i INFILE --o OUTFILE --len LENGTH_OF_UMIs --r READ_ID.TXT

Input: - bam file
       - length of the UMIs
       - read ids (with primer and umi tags)

Output: bam file with all tags

"""



def read_pair_generator(bam, region_string=None):
	"""
	https://www.biostars.org/p/306041/
	Generate read pairs in a BAM file or within a region string.
	Reads are added to read_dict until a pair is found.
	"""
	read_dict = defaultdict(lambda: [None, None])
	for read in bam.fetch(region=region_string):
		if not read.is_proper_pair or read.is_secondary or read.is_supplementary:
			continue
		qname = read.query_name
		if qname not in read_dict:
			if read.is_read1:
				read_dict[qname][0] = read
			else:
				read_dict[qname][1] = read
		else:
			if read.is_read1:
				yield read, read_dict[qname][1]
			else:
				yield read_dict[qname][0], read
			del read_dict[qname]


def main(argv=None):
	if argv is None:
		argv=sys.argv	


	parser=argparse.ArgumentParser(prog='add primer tags and BX tag with chromosome, location and fragmentation site')
	parser.add_argument('--i', help='Input file')
	parser.add_argument('--o', help='Output file')
	parser.add_argument('--r', help='file with reads id')
	parser.add_argument('--len', help='length of the UMI')
	args=parser.parse_args()

	bamFile=pysam.Samfile(args.i, 'rb')
	outBam = pysam.Samfile(args.o, 'wb', template=bamFile)

	expr = r'^(?P<ID>.+)_(?P<UMI>.{'+args.len+'})'
	regex=re.compile(expr)
	
	dico=dict()
	with open(args.r, 'r') as read_id:
		for line in read_id:
			readid=line.split('_')[0]+'_'+line.split('_')[1]
			pr=line.split('_')[2]
			pe=line.split('_')[3].rstrip()
			dico[readid]=(pr, pe)
	
	dico_rand=dict()
	for read1, read2 in read_pair_generator(bamFile):
	    """
	        Fragmentation site calcul
	    """
			if read2.is_reverse:			
				alignLocRand = read2.aend - 1
				dico_rand[read1.qname]=alignLocRand
			else:
				alignLocRand = read2.pos
				dico_rand[read1.qname]=alignLocRand
	bamFile.close()

	bamFile=pysam.Samfile(args.i, 'rb')
	for read in bamFile:	
	    """
	        Add primer tags and UMI final tags
	    """
				tmp=dico.get(read.qname)
				alignLocRand=dico_rand.get(read.qname)
				read.set_tag('pr', tmp[0])
				read.set_tag('pe', tmp[1])
				retour=regex.search(str(read))
				if retour:
					umi=retour.group('UMI')
					prTag=read.get_tag('pr').split('-')
					strand=prTag[1]
					if read.tid == 0: #because Pysam doesn't handle chr Y, X, and M
						chrom='M'
					elif read.tid == 23:
						chrom='X'
					elif read.tid == 24:
						chrom='Y'
					else:
						chrom=str(read.tid)
					if read.has_tag('BX'):
						new_umi=read.get_tag('BX')
						read.set_tag('BX', 'chr'+chrom+'-'+strand+'-'+str(alignLocRand)+'-'+new_umi)
					else:
						read.set_tag('BX', 'chr'+chrom+'-'+strand+'-'+str(alignLocRand)+'-'+umi)
					outBam.write(read)


if __name__=="__main__":
	main(sys.argv)
