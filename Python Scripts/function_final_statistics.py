#!/usr/bin/python3

#Author: JOseph Sevigny
#Purpose: Input large list of from function_convert_uniprot, output final docs with siginificance measures

import sys, os
from scipy.stats import ttest_ind
import numpy as np

sig_value = 0.01

input_file = sys.argv[1] #sorted_functional_significance_mol.tsv
output_dir = 'final_statistics_99ers/'
output_file_matched = open(output_dir + input_file.replace('sorted', 'matched_99_sig'+str(sig_value)), 'w')
output_file_unmatched = open(output_dir + input_file.replace('sorted', 'unmatched_99_sig'+str(sig_value)), 'w')
output_file_insig = open(output_dir + input_file.replace('sorted', 'insignificant_99_sig'+str(sig_value)), 'w')



current_term = ''
matched_list = []
unmatched_list = []

total_count = 0
sig_count = 0
matched_count = 0
unmatched_count = 0

for line in open(input_file, 'r'):
    line = line.rstrip()
    term, a, m, u, r = line.split('\t')
    term = term.lstrip().rstrip().replace(' ','_').replace("+","").replace('"','').replace('(','').replace(')','')
    if current_term != '':
       if term == current_term:
           matched_list.append(float(m))
           unmatched_list.append(float(u))
       else:
           total_count += 1
           t,p = ttest_ind(matched_list, unmatched_list)
           matched_mean = float(np.mean(matched_list)) ; unmatched_mean = float(np.mean(unmatched_list))
           n = str(len(matched_list))
           if p <= sig_value and int(n) > 5:
               sig_count += 1
               if matched_mean > unmatched_mean:
                   matched_count += 1
                   output_file_matched.writelines(current_term + '\t' + str(n) + '\t' +  str(matched_mean) + '\t' + str(unmatched_mean) + '\t' + str(t)  + '\t' + str(p) + '\n')
               else:
                   unmatched_count += 1
                   output_file_unmatched.writelines(current_term + '\t' + str(n) + '\t' +  str(matched_mean) + '\t' + str(unmatched_mean) + '\t' + str(t)  + '\t' + str(p) + '\n')
           else:
               output_file_insig.writelines(current_term + '\t' + str(n) + '\t' +  str(matched_mean) + '\t' + str(unmatched_mean) + '\t' + str(t)  + '\t' + str(p) + '\n')
           #print (current_term)
           current_term = term
           matched_list = []
           unmatched_list = []
           matched_list.append(float(m))
           unmatched_list.append(float(u))
           print ('total count = {}   sig count = {}   matched_count = {}   unmatched count = {}'.format(total_count,sig_count,matched_count,unmatched_count))
    else:
        current_term = term
        matched_list.append(float(m))
        unmatched_list.append(float(u))