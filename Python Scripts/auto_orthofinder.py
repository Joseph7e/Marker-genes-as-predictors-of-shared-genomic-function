#!/usr/bin/python3
#Author: Joseph Sevigny
#Purpose: run Orthofinder pairwise. Run muliple at a time


import os, sys, subprocess
from shutil import copy


#path to all amino acid fastas
all_amino_dir = '/home/genome/joseph7e/gene_16S/files_faas/'

# List of genomes to compare (from uclust)
input_list = open('/home/genome/joseph7e/gene_16S/analysis_housekeeping/clustering/house_clusters/current_needed_compairons.txt', 'r')


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
            command = ['orthofinder.py', '-f', current_orth_dir, '-t', '4'] # run orthofinder
            if count < 2:
                sp = subprocess.Popen(command)
                count +=1
            else:
                sp = subprocess.Popen(command).wait() # wait if too many are running
                count = 0
        else:
            continue
