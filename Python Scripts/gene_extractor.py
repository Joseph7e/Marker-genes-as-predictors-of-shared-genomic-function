#!/usr/bin/python3

#Affiliation: HCGS - mcbs913
#Author: Joseph Sevigny
#Date: 04/20/2016
#Purpose: Extract a specified gene from a set of fastas and gffs and
#         output a gene stats_file and directory containing gene fastas

from Bio import SeqIO
import os, sys, gzip, seqIOtools, re


#######     Global variables
output_dir = 'gene_extract_' + sys.argv[1]
FASTA_dir = '/home/mcbs913kd/mcbs913sh/downloaded_genomes/fastas/'
GFF_dir = '/home/mcbs913kd/mcbs913sh/downloaded_genomes/gffs/'
FASTA_dir = './'
GFF_dir = './'
# output_dir = sys.argv[1]
# FASTA_dir = sys.argv[2] # fasta must be unzipped. gff can be either
# GFF_dir = sys.argv[3] # matching gff must have identical names (extensions = .fasta or .fa or .fna and .gff)


#######     Construct output pathways
if not os.path.exists(output_dir.replace(" ", "_")):
    os.mkdir(output_dir.replace(" ", "_"))
output_log = open("gene_extract_log_" + sys.argv[1], 'w')
#output_stats = open("gene_stats_" + sys.argv[1], 'w')


#######   Configurations
flanking = 0 #change to grab flanking regions on either side of the gene


###### 16S configurations
unique_gene_identifiers = ['16S'] # gff line must contain this
#positive_check = ("Rrna", "rrna","rRNA") # gff entry must be of one of these types
#negative_check = ("CDS", "product=16S", "exon", "region", "tRNA", "gene") # not this gene type

###### HOUSE-KEEPING GENES configurations
#unique_gene_identifiers = ["30S ribosomal protein S12"]
#unique_gene_identifiers = ["30S ribosomal protein S15"]
#unique_gene_identifiers = ["GTPase Der"]
#unique_gene_identifiers = ["ATP synthase subunit delta"]
#unique_gene_identifiers = ["CTP synthase"]
#unique_gene_identifiers = ["DNA gyrase subunit B"] # straight gene identifier
#unique_gene_identifiers = ['translation initiation factor IF-2']
#positive_check = ("CDS", "gene") # ensure these are not in line --> leave as [] for nothing
negative_check = False # make sure this is not in line --> leave as [] for nothing

#unique_gene_identifiers = ['CRISPR spacer']

positive_check = ("exon", "rRNA") # ensure these are not in line --> leave as [] for nothing
#negative_check = ("exon","XXXXXXXX") # make sure this is not in line --> leave as [] for nothing


#output_log.writelines("#Fasta Dir -->\t" + FASTA_dir + "\n#GFF Dir -->\t" + GFF_dir + "\n#unique gene ids -->\t" + str(unique_gene_identifiers) + "\n#positive check -->\t" + str(positive_check) + "\n#negative check -->\t" + str(negative_check) + "\n")
output_log.writelines("#GCF_file\tNode_name\tstart\tstop\tlength\n")

print ("#Fasta Dir -->\t" + FASTA_dir + "\n#GFF Dir -->\t" + GFF_dir + "\n#unique gene ids -->\t" + str(unique_gene_identifiers) + "\n#positive check -->\t" + str(positive_check) + "\n#negative check -->\t" + str(negative_check))

#Obtain gffs and fastas using the extract_file_names definition
gffs = seqIOtools.extract_file_names("gff", GFF_dir)
fastas = seqIOtools.extract_file_names(".fa", FASTA_dir)
if len(fastas) == 0:
    fastas = seqIOtools.extract_file_names(".fna", FASTA_dir)


#create a dictionary of fastas and matching annotations:
fa_gff_dict = seqIOtools.match_fasta_and_gff(fastas,gffs) ##dictionary containing all fastas:gffs

print ("number of starting fastas = {}\tnumber of starting gffs = {} \ntotal matching = {}".format(len(fastas), len(gffs), len(fa_gff_dict)))

#output_log.writelines("#number of starting fastas = {}\tnumber of starting gffs = {} \n#total matching = {}".format(len(fastas), len(gffs), len(fa_gff_dict)))

output_set = set() #gather potential gene types for troubleshooting

for current_fasta, current_gff in fa_gff_dict.items():
    current_sample = current_fasta[:15]
    gene_count = 0 #in case more than one gene is enetered at a time
    #output_log.writelines("#" + current_fasta + "\t" + current_gff + '\n')

    if current_gff.endswith(".gz"):
        g = gzip.open(GFF_dir+current_gff, 'rt') #checks for zipped gff file
    else:
        g = open(GFF_dir + current_gff, 'r')

    print (seqIOtools.mess_with_font.Green + "\nWorking on details for each gene in the file --> " + seqIOtools.mess_with_font.ENDC, current_fasta)
    for line in g.readlines():
        if line[0] == "#":
            continue
        else:
            for gene in unique_gene_identifiers:
                negative_flag = "off"
                positive_flag = "off"
                if gene in line:
                    header, program, gene_identity, start, stop, tmp, direction, tmp2, product = line.split("\t")
                    output_set.add(gene_identity)
                    current_gene_file = output_dir + "/" +  current_fasta[:13] + '_' + gene.replace(" ", "_") + '_' + gene_identity + ".fasta"
                    if negative_check:
                        for n in negative_check:
                            if n in gene_identity:
                                negative_flag = "on"
                            else:
                                continue

                    if positive_check:
                        for p in positive_check:
                            if p in gene_identity:
                                positive_flag = "on"
                            else:
                                continue
                    else:
                        positive_flag = "on"
                        continue

                    if positive_flag == "on" and negative_flag == "off":
                        gene_count += 1
                        #output_log.writelines(line)
                        start = int(start); stop = int(stop)
                        output_log.writelines(current_sample + '\t' + header + '\t' + gene_identity + '\t' + str(start) + '\t' + str(stop) + '\t' + direction + '\t' + str(stop - start) + "\n")
                        seqIOtools.extract_region(FASTA_dir + current_fasta, header, start-flanking, stop+flanking, current_gene_file, direction, str(gene_count)+ "_" + gene_identity+ "_" + current_fasta+"_"+str(start)+"_"+str(stop)+"_" +direction)
                        print (gene, header, gene_identity, str(start), str(stop), direction)
                    else:
                        output_log.writelines("filtered_out__" + line)
    #create a definition in seqio to gather sequence statistics or keep track and print now
    #####remove gene_stats

print ("gene types that contain specified gene name", output_set)