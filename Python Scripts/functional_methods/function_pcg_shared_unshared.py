#!/usr/local/bin/python3
#Auhtor: Joseph Sevigny
#Purpose: Parse Orthofinder results and construct lists of accessions that are found with shared and unshared files.


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


# for rounds
print("============= START =============")
# for line in open('all_rounds_list.txt', 'r'): # change to input_dir_list for all
for line in open('all_amplified_99_comparisons.txt', 'r'):
    folder = '1'
    try:
        dirs = os.listdir('round1/' + line.rstrip())
        folder = '1'
    except FileNotFoundError:
        try:
            dirs = os.listdir('round2/' + line.rstrip())
            folder = '2'
        except FileNotFoundError:
            try:
                dirs = os.listdir('round3/' + line.rstrip())
                folder = '3'
            except FileNotFoundError:
                try:
                    dirs = os.listdir('round4/' + line.rstrip())
                    folder = '4'
                except FileNotFoundError:
                    print ("cant find" + line)
    for current_dir in dirs:
        flag = -1
        # for inside_dir in os.listdir(input_dir + current_dir):
        if current_dir.startswith(result_dir_prefix):
            result_dir = 'round' + folder + '/' +  line.rstrip() + '/' + current_dir
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
                    all_genes = re.findall(r"([A-Z][A-Z]_[0-9]*).", line)
                    if type(all_genes) is list:
                        for g in all_genes:
                            if g.lstrip() in gene_dict.keys():
                                gene_dict[g.lstrip()] += 1
                            else:
                                gene_dict[g.lstrip()] = 1
                    else:
                        if all_genes.lstrip() in gene_dict.keys():
                            gene_dict[all_genes.lstrip()] += 1
                        else:
                            gene_dict[all_genes.lstrip()] = 1

        with open(unmatched_gene_file, 'r') as u:
            for line in u:
                if line.startswith('\t'):
                    continue
                else:
                    all_genes = re.findall(r"([A-Z][A-Z]_[0-9]*).", line)

                    if type(all_genes) is list:
                        for g in all_genes:
                            if g.lstrip() in un_gene_dict.keys():
                                un_gene_dict[g.lstrip()] += 1
                            else:
                                un_gene_dict[g.lstrip()] = 1
                    else:
                        if all_genes.lstrip() in un_gene_dict.keys():
                            un_gene_dict[all_genes.lstrip()] += 1
                        else:
                            un_gene_dict[all_genes.lstrip()] = 1
    print (len(gene_dict), len(un_gene_dict))
print (len(gene_dict), len(un_gene_dict))


print("============= FINISH ============")


output_file = open("matched_unmatched_proteins99.tsv", 'w')
protein_file = open('uniq_all_proteins_and_annotations.tsv', 'r')
for line in protein_file.readlines():
    line = line.rstrip()
    acc_l= line.split('\t')
    matched = 0
    unmatched = 0
    acc = acc_l[0]
    if acc in gene_dict:
        matched = gene_dict[acc]
    if acc in un_gene_dict:
        unmatched = un_gene_dict[acc]
    output_file.writelines(acc + "\t" + str(matched) + "\t" + str(unmatched) + "\n")
print("awk '($2 + $3 > 0)' <-- removes any protein that doesnt match or unmatch somehting")

output_file2 = open("matched_unmatched_proteins_V2_99.tsv", 'w')

for key, value in gene_dict.items():
    output_file2.writelines(str(key) + '\t' + str(value) + '\n')

output_file2.writelines('###unmatched')
for key, value in un_gene_dict.items():
    output_file2.writelines(str(key) + '\t' + str(value) + '\n')
