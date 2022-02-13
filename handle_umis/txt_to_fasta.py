import argparse

"""
    This function is used to convert the primer file into a fasta file that can be handled by CUTADAPT.
"""


parser=argparse.ArgumentParser(prog='primer file txt to fasta')
parser.add_argument('--i', help='Input file')
parser.add_argument('--o', help='Output file')
args=parser.parse_args()

inFile=open(args.i, 'r')

outFile=open(args.o, 'w')

cnt=0
for i in inFile:
	cnt+=1
	outFile.write('> R'+str(cnt)+'\n'+'^'+str(i.split('\t')[3]))
	
