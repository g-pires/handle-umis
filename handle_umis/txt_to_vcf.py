import argparse
import sys

"""     
        This module converts  a txt file into a vcf file

Usage::
        
        txt_to_vcf --i INFILE --o OUTFILE --r REFERENCE_NAME --s SAMPLE_ID

Input:
        - txt file with variants
        - reference name of the reference genome
        - sample id name
Output:
        - vcf file 
        
"""

def main(argv=None):
        if argv is None:
                argv = sys.argv 

        parser=argparse.ArgumentParser(prog='txt to vcf')
        parser.add_argument('--i', help='Input txt file')
        parser.add_argument('--o', help='Output vcf file')
        parser.add_argument('--r', help='Reference genome name')
        parser.add_argument('--s', help='Sample name')
        args=parser.parse_args()

        fileOut=open(args.o, 'w')


        headerVcf = '##fileformat=VCFv4.2' + '\n' + \
        '##reference={ref}'.format(ref=args.r) + '\n' + \
        '##FILTER=<ID=LM,Description="Low coverage (fewer than 5 barcodes)">' + '\n' + \
        '##FILTER=<ID=RepT,Description="Variant in tandem repeat (TFR) regions">' + '\n' + \
        '##FILTER=<ID=RepS,Description="Variant in simple repeats (RepeatMasker) regions">' + '\n' + \
        '##FILTER=<ID=HP,Description="Inside or flanked by homopolymer regions">' + '\n' + \
        '##FILTER=<ID=LowC,Description="Variant in Low complexity regions, as defined in RepeatMasker">' + '\n' + \
        '##FILTER=<ID=SL,Description="Variant in micro-satelite regions, as defined in RepeatMasker">' + '\n' + \
        '##FILTER=<ID=SB,Description="Strand Bias">' + '\n' + \
        '##FILTER=<ID=DP,Description="Too many discordant pairs">' + '\n' + \
        '##FILTER=<ID=MM,Description="Too many mismatches in a read. Default threshold is 6.5 per 100 bases">' + '\n' + \
        '##FILTER=<ID=LowQ,Description="Low base quality">' + '\n' + \
        '##FILTER=<ID=RBCP,Description="Variant are clustered at the end of barcode-side reads">' + '\n' + \
        '##FILTER=<ID=RPCP,Description="Variant are clustered at the end of primer-side reads">' + '\n' + \
        '##FILTER=<ID=PB,Description="Primer bias filter. odds ratio > 10 or < 0.1">' + '\n' + \
        '##FILTER=<ID=PrimerCP,Description="variant is clustered within 2 bases from primer sequence due to possible primer dimers">' + '\n' + \
        '##INFO=<ID=TYPE,Number=.,Type=String,Description="Variant type: SNP/INDEL/COMPLEX">' + '\n' + \
        '##INFO=<ID=RepRegion,Number=.,Type=String,Description="Repetitive region">' + '\n' + \
        '##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth">' + '\n' + \
        '##INFO=<ID=UMT,Number=1,Type=Integer,Description="Total used UMI depth">' + '\n' + \
        '##INFO=<ID=VMT,Number=.,Type=Integer,Description="Variant UMI depth">' + '\n' + \
        '##INFO=<ID=VMF,Number=.,Type=Float,Description="Variant UMI allele frequency">' + '\n' + \
        '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' + '\n' + \
        '##FORMAT=<ID=AD,Number=.,Type=Integer,Description="Filtered allelic UMI depths for the ref and alt alleles">' + '\n' + \
        '##FORMAT=<ID=VF,Number=.,Type=Float,Description="Variant UMI allele frequency, same as VMF">' + '\n' + \
        '\t'.join(['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']+ [args.s]) + '\n'\

        fileOut.write(headerVcf)
        liste=['A', 'C', 'G', 'T']
        with open(args.i, 'r') as inFile:
                next(inFile)
                for i in inFile:
                        col=i.rstrip().split('\t')
                        if col[2] in liste and col[3] in liste:
                            chrom=col[0]
                            pos=col[1]
                            ID='.'
                            ref=col[2]
                            alt=col[3]
                            qual=col[37]
                            filtre=col[38]
                            info='TYPE='+str(col[4])+';'+'RepRegion='+str(col[25])+';'+'DP='+str(col[29])+';'+'UMT='+str(col[5])+';'+'VMT='+str(col[8])+';'+'VMF='+str(float(col[11])/100)
                            form='GT:AD:VF'
                            if float(col[11]/100)>0.95:
                                sample='1/1'+':'+str(float(col[5])-float(col[8]))+','+str(col[8])+':'+str(float(col[11])/100)
                            else:
                                sample='0/1'+':'+str(float(col[5])-float(col[8]))+','+str(col[8])+':'+str(float(col[11])/100)
                            fileOut.write(chrom+'\t'+pos+'\t'+ID+'\t'+ref+'\t'+alt+'\t'+qual+'\t'+filtre+'\t'+info+'\t'+form+'\t'+sample+'\n')

if __name__=="__main__":
        main(sys.argv)
