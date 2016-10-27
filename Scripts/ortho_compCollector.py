#!/usr/local/bin/python3
#
#	compCollector.py  
#		Read two csv files under particular path and 
#		directory for comparison info, collect and count 
#		the number of assigned and unassigned gene in each round
#
#   @Ying Zhang
#   04/18/16
import os
import sys
import csv
import re

import string
import subprocess
import shlex

# ----------- switches --------------
# total number of round
TotalRound = 4
# a switch to decide if use simple mode of gene prefix.
SimplePrefix = True
# a switch to print process. Can be turn off
PrintProcess = False 


#----------- global variables -----------------------
# two input file names as static variables
ort_unassigned = "OrthologousGroups_UnassignedGenes.csv"
ort_assigned = "OrthologousGroups.csv"

# other directory names need to be static
dir_list = "_dir_list" 	# file name of saving all comparison dir is round_dir+dir_list
round_dir = "round" 	# round dirname = "round" + number, eg,"round1"
result_dir_prefix = "Results"

# 1 output csv files for all rounds
round_csv = csv.writer(open('all_round_comparsion_result.csv', "w"), lineterminator='\n')
round_csv.writerow(["file name", "total expected", "num of assigned genes", "num of unassigned genes","ratio of assigned genes"])


usageMsg = '''
Usage: compCollector.py N [options]
		Read pair of two csv files under particular path and 
		directory for comparison info, collect and count 
		the number of assigned and unassigned gene in each round
		
		N:		number of rounds. 
				Default value: 1
		
		-c:		use complete gene prefix, search all combination of 
				2 upper letters. It might take very long time.
				Default value: False
					Use simple mode. 
					Only search['WP_','NP_','YP_']
		
		-p:		print process.
				Default value: false
'''

def usage():
	if len( sys.argv ) > 1 and sys.argv[ 1 ] == "-h":
		print( usageMsg )
		exit( 0 )

#-----------------------------------------------------------------------      
#--------------------------- main --------------------------------------
# check argument usage correctness
usage()
# check arguments.
if len( sys.argv ) > 1:
	if not sys.argv[1].startswith('-') and sys.argv[1].isdigit:
		TotalRound = int(sys.argv[1])
	if '-c' in sys.argv:
		SimplePrefix = False
	if '-p' in sys.argv:
		PrintProcess = True

round_dirs = [""]*TotalRound
round_dir_lists = [""]*TotalRound

# produce the direct list with contains 
# all directory names in each round
for i in range(0,TotalRound):
	round_dirs[i] = "./" + round_dir + str(i+1)
	round_dir_lists[i] = round_dir  + dir_list + str(i+1)
	produce_dir_list_cmd = "ls " + round_dirs[i] +" >" + round_dir_lists[i]
	os.system(produce_dir_list_cmd)
	

if SimplePrefix:
	genePrefixList = ['WP_','NP_','YP_'] # prefix combination 
else:
	genePrefixList = []
	for x in string.ascii_uppercase:
		for y in string.ascii_uppercase:
			if x!='C' and y!='F':	#exclude "GCF_"
				genePrefixList.append(x+y+"_")

# for rounds
print("============= START =============")
for i in range(0,TotalRound):
	print("============= round "+str(i+1)+" =============")
	rounf_dir_file = open( round_dir_lists[i], 'r' )
	dir_list = rounf_dir_file.read().splitlines()

	# count for processing
	count = 0
	totalfiles = subprocess.check_output("ls -l " + round_dirs[i] + "| wc -l", shell=True).replace('\n','')
	
	for line in dir_list:
		prog = "r" + str(i+1) + ":" + str(count) + "/" + str(totalfiles)
		if(PrintProcess):
			print("processing: " + line + "...("+prog+")")
		count+=1
		comp_dir =  round_dirs[i] + "/" + line
		
		# get result file name that start with "Result" prefix
		flag = -1;
		for dirs in os.walk(comp_dir):
			for d in dirs[1]:
				if d.startswith(result_dir_prefix):
					result_dir = comp_dir + "/" + d
					flag = 0
					
		if flag == -1:
			print("-------------------------------------")
			print("***! ERROR !***: no Results_* directory! ")
			if not PrintProcess:
				print("	Path:  " + comp_dir)
			print("-------------------------------------")
			round_csv.writerow([line, '-', '-', '-', '-'])
			line = rounf_dir_file.readline()
			continue;
			
		ort_uss_name = result_dir + "/" + ort_unassigned
		ort_ass_name = result_dir + "/" + ort_assigned
		# check if this two file is available
		uss_exist = os.path.isfile(ort_uss_name)
		ass_exist = os.path.isfile(ort_ass_name)
		if not uss_exist or not ass_exist:
			print("-------------------------------------")
			print("***! ERROR !***: file does not exist! ")
			if not uss_exist:
				print("	No such file: " + ort_uss_name)
			if not ass_exist:
				print("	No such file: " + ort_ass_name)
			print("-------------------------------------")
			round_csv.writerow([line, '-', '-', '-', '-'])
			line = rounf_dir_file.readline()
			continue;
			
		total_expected = 0;
		num_ass_gene = 0;
		num_uss_gene = 0;
		ration = 0;
		
		# this is the two original faa file name.
		# save for check total number later
		ort_faa1 = comp_dir + "/"
		ort_faa2 = comp_dir + "/"
		
		# calculate number of unassigned gene
		with open(ort_uss_name, 'rb') as ort_uss:
			eachline = re.split( '\t|,', ort_uss.readline())
			ort_faa1 += eachline[1]
			ort_faa2 += eachline[2].translate(None, '\r\n')
			
			while eachline != "":
				eachline = ort_uss.readline()
				num_uss_gene += 1
			num_uss_gene -= 1  # last loop of line is empty
			
		# calculate expected total
		#output1 = subprocess.check_output("grep -c '>' " + ort_faa1, shell=True)
		#output2 = subprocess.check_output("grep -c '>' " + ort_faa2, shell=True)
		#total_expected = int(output1)+int(output2)

		# calculate number of assigned gene
		cmdlist=[]
		for prefix in genePrefixList:
			cmd = "grep -o '" + prefix + "' " + ort_ass_name +" | wc -l"
			out = subprocess.check_output(cmd, shell=True)
			num_ass_gene += int(out)
			
		if num_ass_gene:#total_expected == num_ass_gene + num_uss_gene:
			#print("total: "+ str(total_expected)+" found ass: "+ str(num_ass_gene)+ " found uss: " +str(num_uss_gene))
			ratio = (float)(num_ass_gene/((num_ass_gene + num_uss_gene)*1.0))
			round_csv.writerow([line, total_expected, num_ass_gene, num_uss_gene, ratio])
		else:
			print("-------------------------------------")
			print("***! ERROR !***: total expected number didn't match")
			if not PrintProcess:
				print("	Path:  " + comp_dir)
			print("-------------------------------------")
		line = rounf_dir_file.readline()

	rounf_dir_file.close()

# remove the direct lists
for i in range(0,TotalRound):
	os.remove(round_dir_lists[i])

print("============= FINISH ============")


