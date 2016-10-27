#!/usr/bin/python3
##Author: Joseph Sevigny

import sys


matches_input = open(sys.argv[1],'r') #data_99_orthoclusters
outname = ''
if '/' in sys.argv[1]:
    outname = 'matching_info_' + sys.argv[1].split('/')[-1]
else:
    outname = 'matching_info_' + sys.argv[1]

output = open(outname,'w')
matches_input = open(sys.argv[1],'r') #data_99_orthoclusters
taxonomy_input = open('/genome/joseph7e/gene_16S/analysis_phylogeny/organism_tax.csv','r')

taxonomy_dict = {}
for line in taxonomy_input.readlines():
    info = line.rstrip()[:-1].split(',') #removing trailing comma and newline
    gcf_id = info[0][:-2]
    taxonomy_stuff = info[1:] #seperate gcf and taxonomy info
    #print (gcf_id)
    #print (taxonomy_stuff)
    taxonomy_dict[gcf_id] = taxonomy_stuff

print (len(taxonomy_dict))

for line in matches_input.readlines():
    value, ortho, tmp, match = line.rstrip().split('\t')
    match1, match2 = match.split('-')
    match1_tax = taxonomy_dict[match1]
    match2_tax = taxonomy_dict[match2]
    if match1_tax[-2] == match2_tax[-2]:
        #print ('direct match', match1_tax[-2])
        output.writelines(value + '\t' + ortho + '\t' + match + '\t' + match1_tax[-2]+'\t'+match1_tax[-1]+','+match2_tax[-1]+'\t'+str(match1_tax)+','+str(match2_tax)+'\n')
    else:
        one = match2_tax[-1]
        two = match1_tax[-1]
        if one[1:8] == two[1:8]:
            output.writelines(value + '\t' + ortho + '\t' + match + '\t' + match1_tax[-2]+'\t'+match1_tax[-1]+','+match2_tax[-1]+'\t'+str(match1_tax)+','+str(match2_tax)+'\n')
        else:
            output.writelines(value + '\t' + ortho + '\t' + match + '\t' + match1_tax[-2]+','+match2_tax[-2]+'\t'+match1_tax[-1]+','+match2_tax[-1]+'\t'+str(match1_tax)+','+str(match2_tax)+'\n')
        #print ('nooooooooo', match1_tax[-2], match2_tax[-2])
        #print (set(taxonomy_dict[match1])&set(taxonomy_dict[match2]))