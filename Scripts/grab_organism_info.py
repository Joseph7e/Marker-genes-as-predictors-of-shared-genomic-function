#!/usr/bin/python3

import gzip, os, sys

list = ['Nanoarchaeota', 'Crenarchaeota', 'Euryarchaeota', 'Betaproteobacteria', 'Gammaproteobacteria', 'Alphaproteobacteria', 'Acidobacteria', 'Cyanobacteria', 'Campyolobacterales', 'Deltaproteobacteria', 'Deinococci', 'Chloroflexi', 'Aquificae', 'Thermotogae','Fusobacteria', 'Chlamydiae', 'Bacteroidetes', 'Chlorobi', 'Fibrobacteres', 'Actinobacteria', 'Spirochaetes', 'Planctomycetes', 'Firmicutes']

for l in list:
    print (l + ', ')

sys.exit()

output = open('organism_info.tsv', 'w')
output.writelines("file\ttaxonomy\n")
output2 = open('organism_tax.csv', 'w')

gpff_dir = 'gbffs_files/'


all_files = os.listdir(gpff_dir)


for gpff_file in all_files:
    print ('gpff file =====> ', gpff_file + '\n')
    flag = 'off'
    Flag = True
    organism_info = ''
    organism = ''
    current_file = gzip.open(gpff_dir + gpff_file, 'rt')
    for line in current_file:
        if flag == 'on':
            if ';' not in line and "." not in line:
                break
            else:
                #print (line)
                line  = line.rstrip()
                organism_info += line
        if "ORGANISM" in line:
            flag = 'on'
            line = line.replace("ORGANISM", '').rstrip().lstrip()
            organism = line.replace(' ', '_')
    organism_info = organism_info.replace('.','').replace(' ', '')
    organism_info = organism_info.lstrip(); organism_info = organism_info.rstrip() + ',' +  organism
    #organism_info = organism_info.replace("Bacteria;", '')
    taxonomy = organism_info.split(';')
    print (taxonomy)
    output.writelines(gpff_file + '\t')
    output2.writelines(gpff_file[:15] + ',')
    for tax in taxonomy:
        output.writelines(tax + '\t')
        output2.writelines(tax + ',')
    output.writelines("\n")
    output2.writelines("\n")