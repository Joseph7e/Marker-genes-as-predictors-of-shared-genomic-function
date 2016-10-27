#!/usr/local/bin/python3

import os
import sys
import csv
import re, string
import subprocess


#----------- global variables -----------------------
# two input file names as static variables
ort_unassigned = "OrthologousGroups_UnassignedGenes.csv"
ort_assigned = "OrthologousGroups.csv"
result_dir_prefix = "Results"
results_dir = ''

gene_dict = {}
un_gene_dict = {}

input_dir = sys.argv[1]

#input_dir_list = os.listdir(input_dir)

certain_dir_list = []

for line in open(sys.argv[2], 'r'):
    if line.startswith("#"):
        continue
    else:
        certain_dir_list.append(line.rstrip())

# for rounds
print("============= START =============")
for dir in certain_dir_list: # change to input_dir_list for all
    print (dir)
    dirs = os.listdir(input_dir + dir)
    for current_dir in dirs:
        flag = -1
        # for inside_dir in os.listdir(input_dir + current_dir):
        if current_dir.startswith(result_dir_prefix):
            result_dir = input_dir + dir + '/' + current_dir
            flag = 0
        if flag == -1:
            # print("-------------------------------------")
            # print("***! ERROR !***: no Results_* directory! ", input_dir + dir + '/' + current_dir)
            # print("-------------------------------------")
            continue;

        matched_gene_file = result_dir + "/" + ort_assigned
        unmatched_gene_file = result_dir + "/" + ort_unassigned
        # check if this two file is available
        uss_exist = os.path.isfile(matched_gene_file)
        ass_exist = os.path.isfile(unmatched_gene_file)
        if not uss_exist or not ass_exist:
            print("-------------------------------------")
            print("***! ERROR !***: file does not exist! ")
            if not uss_exist:
                print("	No such file: " + matched_gene_file)
            if not ass_exist:
                print("	No such file: " + unmatched_gene_file)
            print("-------------------------------------")
            continue;

        # calculate number of unassigned gene
        with open(matched_gene_file, 'r') as m:
            for line in m:
                if line.startswith('\t'):
                    continue
                else:
                    genome1_genes = []; genome2_genes = []
                    gene_fam, genome1, genome2 = line.split("\t"); genome2 = genome2.rstrip()
                    if "," in genome1:
                        genome1_genes = genome1.split(",")
                    else:
                        genome1_genes.append(genome1)
                    if "," in genome2:
                        genome2_genes = genome2.split(",")
                    else:
                        genome2_genes.append(genome2)
                    all_genes = (genome1_genes + genome2_genes)
                    #print (genome1_genes, genome2_genes)
                    if type(all_genes) is list:
                        for g in all_genes:
                            if g.lstrip()[:-2] in gene_dict:
                                gene_dict[g.lstrip()[:-2]] += 1
                            else:
                                gene_dict[g.lstrip()[:-2]] = 1
                    else:
                        if all_genes.lstrip()[:-2] in gene_dict:
                            gene_dict[all_genes.lstrip()[:-2]] += 1
                        else:
                            gene_dict[all_genes.lstrip()[:-2]] = 1

        with open(unmatched_gene_file, 'r') as u:
            for line in u:
                if line.startswith('\t'):
                    continue
                else:
                    genome1_genes = []; genome2_genes = []
                    gene_fam, genome1, genome2 = line.split("\t"); genome2 = genome2.rstrip()
                    if "," in genome1:
                        genome1_genes = genome1.split(",")
                    else:
                        genome1_genes.append(genome1)

                    if "," in genome2:
                        genome2_genes = genome2.split(",")
                    else:
                        genome2_genes.append(genome2)
                    genome2_genes = genome2.split(",")
                    if genome1 == "":
                        all_genes = genome2
                    else:
                        all_genes = genome1
                    if type(all_genes) is list:
                        for g in all_genes:
                            if g.lstrip()[:-2] in gene_dict:
                                un_gene_dict[g.lstrip()[:-2]] += 1
                            else:
                                un_gene_dict[g.lstrip()[:-2]] = 1
                    else:
                        if all_genes.lstrip()[:-2] in un_gene_dict:
                            un_gene_dict[all_genes.lstrip()[:-2]] += 1
                        else:
                            un_gene_dict[all_genes.lstrip()[:-2]] = 1
    print (len(gene_dict), len(un_gene_dict))
print (len(gene_dict), len(un_gene_dict))


print("============= FINISH ============")


output_file = open("matched_unmatched_proteins_99.tsv", 'w')
protein_file = open('all_protein_ids', 'r')
for line in protein_file.readlines():
    line = line.rstrip()
    matched = 0
    unmatched = 0
    if line in gene_dict:
        matched = gene_dict[line]
    if line in un_gene_dict:
        unmatched = un_gene_dict[line]
    output_file.writelines(line + "\t" + str(matched) + "\t" + str(unmatched) + "\n")
# awk '($2 + $3 > 0)' <-- removes any protein that doesnt match or unmatch somehting