#!/usr/bin/python3

import sys, re

#input = open('/home/genome/joseph7e/gene_16s_redo_all/new_functional_analysis/trying_other_program/best_functional_list.txt', 'r')
#input = open('/home/genome/joseph7e/gene_16s_redo_all/new_functional_analysis/ninety_nine_analysis/joined_stats_best_ones.txt','r')
input = open(sys.argv[1], 'r')
bio_output = open('functional_bio.tsv', 'w')
mol_output = open('functional_mol.tsv', 'w')
cell_output = open('functional_cell.tsv', 'w')

for line in input.readlines():
    line = line.rstrip().replace("'", "")
    stuff = re.findall(r'\[(.*?)\]', line)
    other_stuff = line.split(" ")
    acc = other_stuff[0]; matched = other_stuff[1]; unmatched = other_stuff[2]
    bio = stuff[0]; mol = stuff[1]; cell = stuff[2]; cogs = stuff[3]; kos = stuff[4]
    if bio:
        if ',_' in bio:
            bios = bio.split(',_')
            for b in bios:
                bio_output.writelines(b+'\t'+acc+'\t'+matched+'\t'+unmatched+'\t'+str(int(matched)-int(unmatched))+'\n')
        else:
            bio_output.writelines(bio+'\t'+acc+'\t'+matched+'\t'+unmatched+'\t'+str(int(matched)-int(unmatched))+'\n')
    if mol:
        if ',_' in mol:
            mols = mol.split(',_')
            for m in mols:
                mol_output.writelines(m+'\t'+acc+'\t'+matched+'\t'+unmatched+'\t'+str(int(matched)-int(unmatched))+'\n')
        else:
            mol_output.writelines(mol+'\t'+acc+'\t'+matched+'\t'+unmatched+'\t'+str(int(matched)-int(unmatched))+'\n')
    if cell:
        if ',_' in cell:
            cells = cell.split(',_')
            for c in cells:
                cell_output.writelines(c+'\t'+acc+'\t'+matched+'\t'+unmatched+'\t'+str(int(matched)-int(unmatched))+'\n')
        else:
            cell_output.writelines(cell+'\t'+acc+'\t'+matched+'\t'+unmatched+'\t'+str(int(matched)-int(unmatched))+'\n')

print ("sed -e 's/^[ \t]*//' functional_significance_cell.tsv | sort | uniq > sorted_functional_significance_cell.tsv")