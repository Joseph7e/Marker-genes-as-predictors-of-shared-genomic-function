#!/usr/bin/python3
#Purpose: Input a fasta file with identifyable gene headers (i.e. GCF_[0-9]?)
	# and output gene copy number, lengths, and variation stats

#USAGE: python3 variation_stats.py fasta_file
#Author: Joseph Sevigny

import sys, os, re, subprocess
from Bio import SeqIO

##NOTES
            #fasta_file must have .fasta extension
            #fasta file must have identifyable gene headers (i.e. GCF_[0-9]?)
            #fasta_file must be sorted by name

fasta_file = sys.argv[1]
output = open('best_variation_table.xls', 'w')

current_fasta = ''
copy_number = 0
variation_list = []
high_variation = 0
avg_variation = 0
length_low = 0
length_high = 0
all_length = []
old_genome = ''
growing_seq = ''

output_dir = 'all_best_files_seperate/'


for line in open(fasta_file, 'r'):
    if line.startswith('>'):
        genomes = re.findall(r">(GCF_[0-9]*)", line); genome = genomes[0]
        if current_fasta == '':
            #print (genome, '1')
            current_fasta = genome
        else:
            if genome != current_fasta and current_fasta != '':
                #print (old_genome, '3')
                average_length = sum(all_length)/len(all_length)
                #print (old_genome + '\t' + str(copy_number) + '\t' + str(length_low) + '\t' + str(length_high) + '\t' + str(average_length))
                with open(output_dir + old_genome + '.fasta', 'w') as out:
                    out.writelines(growing_seq)
                if copy_number == 1:
                    output.writelines(old_genome+"\t"+str(copy_number)+"\t"+str(length_low)+"\t"+str(length_high)+"\t"+str(average_length)+"\t"+"100"+"\t"+"100" + "\n")
                else:
                    command = ['/home/genome/joseph7e/program_tcoffee/T-COFFEE_installer_Version_11.00.8cbe486_linux_x64/bin/t_coffee', '-other_pg', 'seq_reformat', '-in', output_dir + old_genome + '.fasta', '-output', 'sim_idscore']
                    sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    results = str(sp.communicate()[0].decode('ascii'))
                    high_variation = 100
                    for line in results.split("\n"):
                        if line.startswith("TOT"):
                            stuff = line.split('\t')
                            avg_variation = stuff[3].lstrip().rstrip()
                        if line.startswith("TOP") or line.startswith("BOT"):
                            stuffed = line.split('\t')
                            variation = float(stuffed[4].lstrip().rstrip())
                            if variation < high_variation:
                                high_variation = variation
                    if avg_variation == '-nan':
                        avg_variation = 100
                    output.writelines(old_genome+"\t"+str(copy_number)+"\t"+str(length_low)+"\t"+str(length_high)+"\t"+str(average_length)+"\t"+str(high_variation)+"\t"+str(avg_variation) + "\n")
                    print(old_genome+"\t"+str(copy_number)+"\t"+str(length_low)+"\t"+str(length_high)+"\t"+str(average_length)+"\t"+str(high_variation)+"\t"+str(avg_variation))

                growing_seq = ''
                current_fasta = genome
                length_low = 0
                length_high = 0
                all_length = []
                copy_number = 0
                variation_list = []
                high_variation = 0
                avg_variation = 0


        if genome == current_fasta:
            old_genome = genome
            #print (genome, '2')
            copy_number += 1
            #lister = re.findall(r"length_(.*)\n", line)
            for seq_record in SeqIO.parse(fasta_file, "fasta"):
                if line.rstrip()[1:100] in seq_record.id and old_genome in line:
                    # print (line)
                    # print (seq_record.id)
                    length = len(seq_record.seq)
                    my_seq = (str(seq_record.seq))
                    header = ('>' + str(copy_number) + '_' + seq_record.id)
                    growing_seq += (header + '\n' + my_seq + '\n')
            all_length.append(int(length))
            if int(length) <= length_low or length_low == 0:
                length_low = int(length)
            if int(length) >= length_high:
                length_high = int(length)








# for f in os.listdir(new_files_dir):
#     r = open(new_files_dir + f, 'r')
#     copy_number = 0
#     variation_list = []
#     high_variation = 0
#     avg_variation = 0
#     length_low = 0
#     length_high = 0
#     for line in r.readlines():
#         if ">" in line: # GCF_000005825_NC_013791.2_exon_+_start_97241stop_98796length_1556
#             copy_number+= 1
#             lister = re.findall(r"length_(.*)\n", line)
#             length = lister[0]
#             if int(length) <= length_low or length_low == 0:
#                 length_low = int(length)
#             if int(length) >= length_high:
#                 length_high = int(length)
#     if copy_number == 1:
#         variation_table.writelines(f+"\t"+str(copy_number)+"\t"+str(length_low)+"\t"+str(length_high)+"\t"+"100"+"\t"+"100" + "\n")
#     else:
#         command = ['blastn', '-query', new_files_dir + f, '-subject', new_files_dir + f, '-outfmt', '6']
#         sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         results = str(sp.communicate()[0].decode('ascii'))
#         for line in results.split("\n"):
#             try:
#                 query, subject, variation, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, tmp8, tmp9 = line.split("\t")
#             except ValueError:
#                 continue
#             if query == subject:
#                 continue
#             else:
#                 variation_list.append(eval(variation))
#                 if eval(variation) <= high_variation or high_variation == 0:
#                     high_variation = eval(variation)
#         # print (variation_list, f )
#         try:
#             avg_variation = sum(variation_list)/len(variation_list)
#         except ZeroDivisionError:
#             avg_variation = 0
#             print ("missing some blast results", f)
#         variation_table.writelines(f+"\t"+str(copy_number)+"\t"+str(length_low)+"\t"+str(length_high)+"\t"+str(avg_variation)+"\t"+str(high_variation) + "\n")
#         if len(variation_list) != (copy_number*copy_number-copy_number):
#             print ("missing some blast results", f)
