#!/usr/bin/python3
import sys
import re
import argparse
"""
    This module takes the UMI in the mi tag and append it to the readid.

Usage::

    add_umi --i INFILE --o OUTFILE --len LENGTH_OF_UMIs

Input: - fastq file
       - length of the UMIs

Output: fastq file with UMI append to the read_id

"""

def main(argv=None):
	if argv is None: 
		argv = sys.argv
	
	parser = argparse.ArgumentParser(prog="trimming id")
	parser.add_argument('--i', help='Input file')
	parser.add_argument('--o', help='Output file')
	parser.add_argument('--len', default=12, help='length of the UMI barcode')
	args=parser.parse_args()

	fileIn=open(args.i, 'r')
	fileOut=open(args.o, 'w')

	def get_info(lines=None):
		dico=['nom', 'seq', 'option', 'qualite']
		return {key: val for key,val in zip(dico, lines)}

	expr = r'^(?P<ID>.+)mi:Z:+(?P<UMI>.{' + args.len + '})'
	regex = re.compile(expr)

	n=4
	with fileIn as prep_read:
		lines=[]
		for line in prep_read:
			lines.append(line.rstrip())
			if len(lines)==n:
				record=get_info(lines)
				retour=regex.search(record['nom'])
				if retour:
					fileOut.write(retour.group('ID')+retour.group('UMI')+"\n")
					fileOut.write(record['seq']+'\n'+record['option']+'\n'+record['qualite']+'\n')
				lines=[]
	fileOut.close()

if __name__=="__main__":
	main(sys.argv)

