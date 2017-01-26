#!/usr/bin/python3

#Author: Joseph Sevigny
#Purpose: Parse Significant data and creat word clouds based on number of accessions for the term.

import sys
import mycloud


unmatched_file = sys.argv[1] #matched_99_sig0.01_functional_mol.tsv
matched_file = sys.argv[2] #unmatched_99_sig0.01_functional_mol.tsv

convert = True

string_match = ''

string_unmatch = ''

with open(unmatched_file, 'r') as h:
    for line in h:
        line = line.rstrip()
        current_term,n,matched_mean,unmatched_mean,t,p = line.split('\t')
        #id, m, u = line.split('\t'); id = id.lstrip().replace(" ", "_") + " "
        current_term = current_term.lstrip().replace(" ", "_").replace('-','_') + " "
        new_id_m = (current_term * int(n))
        string_unmatch += new_id_m#.replace(" ","_")

with open(matched_file, 'r') as m:
    for line in m:
        line = line.rstrip()
        current_term,n,matched_mean,unmatched_mean,t,p = line.split('\t')
        #id, m, u = line.split('\t'); id = id.lstrip().replace(" ", "_") + " "
        current_term = current_term.lstrip().replace(" ", "_").replace('-','_') + " "
        new_id_m = (current_term * int(n))
        string_match += new_id_m#.replace(" ","_")


mycloud.generate_cloud(string_match, matched_file + "_enriched_matched_cloud")
mycloud.generate_cloud(string_unmatch, unmatched_file + "_enriched_matched_cloud")

