#!/usr/bin/python3

import os, sys, seqIOtools
from Bio import SeqIO
# from shutil import copyfile


#
# os.mkdir('housekeeping/' + sys.argv[1])
#
# for fasta in os.listdir(sys.argv[1]):
#     count = 0
#     with open(sys.argv[1] + fasta, 'r') as f:
#         for line in f:
#             if line.startswith(">"):
#                 count += 1
#
#         if count == 1:
#             copyfile(sys.argv[1] + fasta, 'housekeeping/' + sys.argv[1] + fasta)



#### Determine genomes that contain all the genes we want to use
output = open("full_table.tsv", 'w')
output2 = open("best_table.tsv", 'w')
dict = {} # genome: value
all_output = open('house_keeping_genes.fasta', 'w')


dir_list = ('gene_extract_initiation_factor','gene_extract_gyrase','gene_extract_ctp_synthase','gene_extract_ribosomal_protein_S12','gene_extract_ribosomal_protein_S15')

def list_dir_grab_id(dir):
    list = os.listdir(dir)
    for g in list:
        g = g[:13]
        if g in dict.keys():
            dict[g].append(dir[13:])
        else:
            dict[g] = [dir[13:]]


for dir in dir_list:
    list_dir_grab_id(dir)

best_list = []
for key, value in dict.items():
    output.writelines(key + "\t" +  str(value) + '\n')
    if len(value) == 5:
        output2.writelines(key + '\n')
        best_list.append(key)


print (len(best_list))

for genome in best_list:
    sequence = ''
    out = open("concatenated_housekeepers/" + genome + ".fasta", 'a')
    for dir in dir_list:
        file_list = os.listdir(dir)
        for f in file_list:
            if genome in f:
                fasta_dict = seqIOtools.read_fasta(dir + '/' + f)
                count = 0
                for header, seq in fasta_dict.items():
                    while count == 0:
                        sequence += seq
                        out.writelines(header.rstrip() + dir + '\n' + seq + "\n")
                        count = 1
                    continue
    head = ">" + genome + "_" + str(len(sequence))
    all_output.writelines(head + '\n' + seq + '\n')
                #                 with open (writeable_mito_contig_file, 'w') as cfo:
                # for seq_record in SeqIO.parse(contig, "fasta"):
                #     if current_node in str(seq_record.id):
                #         cfo.write(">" + contig + str(seq_record.id) + "\n")
                #         cfo.write(str(seq_record.seq) + "\n")

# headers = []
#
# for seq_record in SeqIO.parse(file_names, "fasta"):
#     print (seq_record.id[5:15])
#     headers.append(seq_record.id[5:30])
#

# for header in headers:
#     count = 0
#     output.writelines(">" + header + "\n")
#     for file in file_names:
#          for seq_record in SeqIO.parse(file, "fasta"):
#              if header in seq_record.id:
#                  output.writelines(str(seq_record.seq))
#                  count += 1
#     output.writelines("\n")
#     if count < gene_count:
#         print (header + "\t<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
#     if count > gene_count:
#         print (header + "\t>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     print (count)
#     # for seq_record in SeqIO.parse(contig, "fasta"):
#     #                 if current_node in str(seq_record.id):
#     #                     cfo.write(">" + contig + str(seq_record.id) + "\n")
#     #                     cfo.write(str(seq_record.seq) + "\n")