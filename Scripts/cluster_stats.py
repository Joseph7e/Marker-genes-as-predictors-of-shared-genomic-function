#!/usr/bin/python3

import os, sys, re


growing_pairwise_set = []

all_dirs = ['seperate_100/','seperate_99/','seperate_98/','seperate_97/','seperate_96/','seperate_95/', 'seperate_94/', 'seperate_93/']

output_all = open("all_needed_comparisons.txt", 'w')



for input_dir in all_dirs:
    all_pairwise = []
    input_csv = input_dir + 'clustInfo.csv'
    input_clusts = input_dir + 'clustSummary.csv'
    output_table = open(input_dir[:-1] + ".csv", 'w')
    output_data = open(input_dir[:-1] + 'data.csv', 'w')
    with open(input_clusts, 'r') as r:
        for line in r.readlines():
            if line.startswith("num"):
                continue
            else:
                num_members,num_clusters,hundred,nine_nine,nine_eight,nine_seven,nine_six,nine_five =  line.split(',')
                output_table.writelines(num_members + "\t" + num_clusters + '\n')

    output_list = open(input_dir[:-1] + 'pairwise_list.txt', 'w')
    for file in os.listdir(input_dir):
        output_data.writelines('#' + file + "\n")
        current_pairwise = []
        current_list_of_GCF = []
        if "CLU_" in file:
            with open(input_dir + file, 'r') as o:
                for line in o.readlines():
                    if line.startswith(">"):
                        GCF = re.findall(r"(GCF_[0-9]*)", line)
                        current_list_of_GCF.append(GCF[0])
            for g in current_list_of_GCF:
                pair = []
                for r in current_list_of_GCF:
                    if g == r:
                        continue
                    else:
                        pair = [g,r]
                        pair = sorted(pair)
                        if pair in all_pairwise:
                            continue
                        else:
                            current_pairwise.append(pair)
                            if pair in all_pairwise:
                                continue
                            else:
                                all_pairwise.append(pair)
                            if pair in growing_pairwise_set:
                                continue
                            else:
                                growing_pairwise_set.append(pair)
            current_pairwise = sorted(current_pairwise)
            for c in current_pairwise:
                output_data.writelines(c[0]+ '\t' + c[1] + '\n')
            output_list.writelines(file + '\t' + str(len(current_list_of_GCF)) + '\t' + str(current_pairwise) + '\n')
    output_list.writelines('#' + str(len(all_pairwise)) + '\t' + str(all_pairwise))

growing_pairwise_set = sorted(growing_pairwise_set)
for p in growing_pairwise_set:
    output_all.writelines(p[0] + "\t" + p[1] + "\n")


