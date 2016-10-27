#!/usr/bin/python3

import os, sys, subprocess
from shutil import copy

all_amino_dir = '/home/genome/joseph7e/gene_16S/files_faas/'

input_list = open('/home/genome/joseph7e/gene_16S/analysis_housekeeping/clustering/house_clusters/current_needed_compairons.txt', 'r')
#input_list = open('/home/genome/joseph7e/gene_16S/analysis_orthofinder/still_need', 'r')
#input_list = open('/home/genome/joseph7e/gene_16S/final_analysis_stuff/all_shuffled.csv', 'r')

all_amino_files = os.listdir(all_amino_dir)

#output_list = open('zee_ortho_list.csv', 'w')

count = 0

for line in input_list:
    if line.startswith("#"):
        cluster_numer = line[1:]
    else:
        first,second = line.split("-")
        second = second.replace('\n', '')
        current_orth_dir = first + "-" + second + '/'
        count_match = 0; count_unmatch = 0
        if not os.path.exists(current_orth_dir): #checks to see if that one has been done
            os.mkdir(current_orth_dir)
            count += 1
            for amino in all_amino_files:
                if first in amino:
                    copy(all_amino_dir + amino, current_orth_dir)
                    #os.symlink(all_amino_dir + amino, current_orth_dir)
                if second in amino:
                    #os.symlink(all_amino_dir + amino, current_orth_dir)
                    copy(all_amino_dir + amino, current_orth_dir)
            command = ['orthofinder.py', '-f', current_orth_dir, '-t', '4']
            # if count % 10:
            #     sp = subprocess.Popen(command)
            if count < 2:
                sp = subprocess.Popen(command)
                count +=1
            else:
                sp = subprocess.Popen(command).wait()
                count = 0
        else:
            continue
        # list_results = os.listdir(current_orth_dir)
        # current_dir = ''
        # for file in list_results:
        #     if file.startswith("Results"):
        #         current_dir = file
        # orth_file = open(current_orth_dir + current_dir + '/' + 'OrthologousGroups.txt', 'r')
        # print (orth_file)
        # unmatched_orth_file = open(current_orth_dir + current_dir + '/' + 'OrthologousGroups_UnassignedGenes.csv', 'r')
        # for line in orth_file.readlines():
        #     count_match += 1
        # for line in unmatched_orth_file.readlines():
        #     count_unmatch += 1
        # output_list.writelines(cluster_numer + "\t" + first  + "\t" + second + str(count_match) + "\t" + str(count_unmatch) + "\n")
