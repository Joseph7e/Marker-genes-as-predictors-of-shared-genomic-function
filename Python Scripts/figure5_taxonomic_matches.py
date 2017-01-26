#!/usr/bin/python3
##Author: Joseph Sevigny
##Purpose: Examine taxonomic assignments for genomes that matched in orthofinder (fig 5)


import sys


#INPUTS
matches_input = open(sys.argv[1],'r') #data_99_orthoclusters
taxonomy_input = open('/genome/joseph7e/gene_16S/analysis_phylogeny/organism_tax.csv','r')

outname = '' # construct output name
if '/' in sys.argv[1]:
    outname = 'matching_info_' + sys.argv[1].split('/')[-1]
else:
    outname = 'matching_info_' + sys.argv[1]

output = open(outname,'w')


taxonomy_dict = {} # grab taxonomic info from input
for line in taxonomy_input.readlines():
    info = line.rstrip()[:-1].split(',') #removing trailing comma and newline
    gcf_id = info[0][:-2]
    taxonomy_stuff = info[1:] #seperate gcf and taxonomy info
    taxonomy_dict[gcf_id] = taxonomy_stuff


for line in matches_input.readlines():
    value, ortho, tmp, match = line.rstrip().split('\t')
    match1, match2 = match.split('-')
    match1_tax = taxonomy_dict[match1]
    match2_tax = taxonomy_dict[match2]
    if match1_tax[-2] == match2_tax[-2]:
        output.writelines(value + '\t' + ortho + '\t' + match + '\t' + match1_tax[-2]+'\t'+match1_tax[-1]+','+match2_tax[-1]+'\t'+str(match1_tax)+','+str(match2_tax)+'\n')
    else:
        one = match2_tax[-1]
        two = match1_tax[-1]
        if one[1:8] == two[1:8]: #Does it match or not
            output.writelines(value + '\t' + ortho + '\t' + match + '\t' + match1_tax[-2]+'\t'+match1_tax[-1]+','+match2_tax[-1]+'\t'+str(match1_tax)+','+str(match2_tax)+'\n')
        else:
            output.writelines(value + '\t' + ortho + '\t' + match + '\t' + match1_tax[-2]+','+match2_tax[-2]+'\t'+match1_tax[-1]+','+match2_tax[-1]+'\t'+str(match1_tax)+','+str(match2_tax)+'\n')