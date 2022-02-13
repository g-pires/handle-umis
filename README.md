Handle-umis - These tools are compatible with the pipeline SAIP using UMIs and smcounter2

-----------------------------------------------------------------------------------
-----------------------------------------------------------------------------------

This module has 4 packages :
 
	- add_umi
		*Add UMIs to the read_id.*
		This is useful for the pipeline SAIP using UMIs after the read-trimming.

	- add_tags
		*Add primer and UMI tags to all reads.*
		This is useful for the pipeline SAIP using UMIs after the clustering with umi_tools group.

	- txt_to_fasta
		*Convert the primer file into fasta.*
		This is used with cutadapt for the gene specific primer clipping.
	
	- txt_to_vcf
		*Convert the variants file into vcf.*
		This is used after smCounter2 before the annotations with SNPEff et SNPSift.
