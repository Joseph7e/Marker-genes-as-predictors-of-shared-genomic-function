#!/usr/bin/python3

import gzip, os, sys, re

output = open('protein_uni_prot.csv', 'w')


gpff_dir = 'gpff_files/'


all_files = os.listdir(gpff_dir)


for gpff_file in all_files:
    print ('gpff file =====> ', gpff_file + '\n')
    genome = gpff_file[:15]
    protein_info = {}
    current_file = gzip.open(gpff_dir + gpff_file, 'rt')
    # product = ''
    # function = ''
    # uniprot = ''
    #accession = ''
    flag = 'off'
    count = 0
    for line in current_file:
        # if flag == on:
        #     if "LOCUS" in line:
        #         flag = off
        if "LOCUS" in line and flag == 'on':
            flag = 'off'
            output.writelines(genome + "\t" + accession + "\t" + product + "\t" + function + "\t" + uniprot + '\n')
            accession = 'NONE'
            product = 'NONE'
            function = 'NONE'
            uniprot = 'NONE'
        if flag == 'off':
            if line.startswith("ACCESSION"):
                count = 1
                my_search = re.findall(r"ACCESSION   (\w*)\n", line)
                try:
                    accession = my_search[0]
                except IndexError:
                    print (line)
                    accession = "NONE"
            if '/product=' in line:
                product_search = re.findall(r'/product=(.*)\n', line)
                try:
                    product = product_search[0]
                except IndexError:
                    print (line)
                    product = "NONE"
            if '/function=' in line:
                function_search = re.findall(r'/function=(.*)\n', line)
                try:
                    function = function_search[0]
                except IndexError:
                    print (line)
                    function = "NONE"
            if 'UniProtKB/Swiss-Prot' in line:
                uniprot_search = re.findall(r'"UniProtKB/Swiss-Prot:(.*)"\n', line)
                try:
                    uniprot = uniprot_search[0]
                except IndexError:
                    print (line)
                    uniprot = "NONE"

            if 'LOCUS' in line and count == 1:
                flag = 'on'
                count = 0