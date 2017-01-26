#!/usr/local/bin/python3
#
#	genomePharser.py fastafile 
#		Read a fasta file(result_aligned.fasta) and output each block that 
#		contains more than one genome (i.e. more than one GCF_000762875 
#		identifier in the block) into a separate file labelled on the cluster 
#		number from original file.
#
#   @Ying Zhang
#   04/03/16
import os
import sys
import csv
import re
import numpy as np
import matplotlib.pyplot as plt

#----------- global variables -----------------------

# dataList: a dictionary to store the number of clusters with n genomes.
dataList = {}
# an output csv files as database
data_csv = csv.writer(open('clustInfo.csv', "w"), lineterminator='\n')
data_csv.writerow(["Cluster_NO", "GCF_host", "Number of members in cluster", "GCF_member","diff percent"])
# an output csv file as summary
summary_csv = csv.writer(open('clustSummary.csv', "w"), lineterminator='\n')
summary_csv.writerow(["num of members in one cluster", "num of clusters", "num of 100%ID", "num of 99%ID","num of 98%ID","num of 97%ID","num of 96%ID","num of 95%ID"])

class ClustData:
	def __init__(self, no_of_mem, c):
		self.numberOfMembers = no_of_mem
		self.count = c
		self.count_95pcent = 0	# number of member with 95.0%~95.9%
		self.count_96pcent = 0	# number of member with 96.0%~96.9%
		self.count_97pcent = 0	# number of member with 97.0%~97.9%
		self.count_98pcent = 0	# number of member with 98.0%~98.9%
		self.count_99pcent = 0	# number of member with 99.0%~99.9%
		self.count_100pcent = 0	# number of member with 100.0%


usageMsg = '''
Usage: genomePharser fastafile
		Read a fasta file(result_aligned.fasta)and output each block that 
		contains more than one genome into a separate file labelled on the cluster 
		number from original file with two summary files("clustSummary.csv", 
		"clustInfo.csv")
'''

def usage():
	if len( sys.argv ) != 2 or sys.argv[ 1 ] == "-h":
		print( usageMsg )
		exit( 0 )

def parseHeader(header):
	"""	check if input line is valid header.
		If is, return cluster number in this header."""
	if not header.startswith( '>' ):
		print( "****** ERROR: Expecting sequence header. Wrong fasta file. *******" ) 
		print( "Error line:" )
		print( header )
		print( "**************")
		sys.exit()
	else:
		headerInfo = []
		temp = header.split('|')
		headerInfo.append(temp[0][1:])	# cluster No
		headerInfo.append(temp[1])		# %
		headerInfo.append(temp[2].split(".")[0][8:21])	# GCF No # make sure that header is unique here!!!
		return headerInfo

#-----------------------------------------------------------------------      
#--------------------------- main --------------------------------------
# check argument usage correctness
usage()
print("============= START ==================")
alignedClusterFasta = sys.argv[ 1 ]

#----- open file -----
try:
    inFile = open( alignedClusterFasta, 'r' )
except ( OSError, IOError ) as e:
    print( 'Unable to open ', alignedClusterFasta )

#----- read file and process -----
# file format: 1 line header followed by 1 line sequence
# every time reads 2 lines from the file(1 header and 1 seq line)

header = inFile.readline()
sequence = inFile.readline()
curCLusterNo = "-1"
GCFlist = []
difflist = []

while header != '' and sequence != '':
	# parse header and get an string array[clusterNo, %, GCFNo]
	headerInfo = parseHeader(header)
	clusterNo = headerInfo[0]
	diffpercent = headerInfo[1]
	GCFNo = headerInfo[2]

	# check if the cluster number remains unchanged.
	# If it is a new cluster number, create a new output with cluster number
	if curCLusterNo == "-1":  # first line
		curCLusterNo = clusterNo
		outfile = open('CLU_' + curCLusterNo, "w")

	# write into output file
	outfile.write(header)
	outfile.write(sequence)
	# put GCF number into GCFlist
	if GCFNo not in GCFlist:
		GCFlist.append(GCFNo)
		difflist.append(diffpercent)
	
	if diffpercent == '*':		# last line of cluster
		print(".....processing cluster" + curCLusterNo)
		c_name = len(GCFlist)
		if c_name in dataList:
			dataList[c_name].count +=1
		else:
			dataList[c_name] = ClustData(len(GCFlist), 1)
		
		data_csv.writerow([curCLusterNo, GCFNo, len(GCFlist), "",""])
		for memGCF,memdiff in zip(GCFlist,difflist):
			if memGCF != GCFNo:
				data_csv.writerow(["", "", "", memGCF,memdiff])
				temp_diff = float(memdiff.strip('%'))
				if temp_diff == 100:
					dataList[c_name].count_100pcent += 1
				if temp_diff > 99 and temp_diff < 100:
					dataList[c_name].count_99pcent += 1
				if temp_diff > 98 and temp_diff < 99:
					dataList[c_name].count_98pcent += 1
				if temp_diff > 97 and temp_diff < 98:
					dataList[c_name].count_97pcent += 1
				if temp_diff > 96 and temp_diff < 97:
					dataList[c_name].count_96pcent += 1
				if temp_diff > 95 and temp_diff < 96:
					dataList[c_name].count_95pcent += 1
		
		
		
		GCFlist = [] 		# clean the GCFlist
		difflist = []		# clean the difflist
		outfile.close()		# close current output file
		curCLusterNo = str(int(clusterNo) + 1) # update clusterNo
		outfile = open('CLU_' + curCLusterNo, "w") #open a new file for next cluster

	# read following 2 lines
	header = inFile.readline()
	sequence = inFile.readline()
	
# write into output file
for keys,values in sorted(dataList.items()):
	summary_csv.writerow([values.numberOfMembers, values.count, values.count_100pcent, values.count_99pcent,
	values.count_98pcent,values.count_97pcent, values.count_96pcent,values.count_95pcent])

# print plot
numberOfmem = []
clustercount = []
diff_100 = []
diff_99 = []
diff_98 = []
diff_97 = []
diff_96 = []
diff_95 = []

for keys,values in sorted(dataList.items()):
	numberOfmem.append(values.numberOfMembers)
	clustercount.append(values.count)
	diff_100.append(values.count_100pcent)
	diff_99.append(values.count_99pcent)
	diff_98.append(values.count_98pcent)
	diff_97.append(values.count_97pcent)
	diff_96.append(values.count_96pcent)
	diff_95.append(values.count_95pcent)

plt.plot(numberOfmem, diff_100, 'r-', label = "100%", lw=1)
plt.plot(numberOfmem, diff_100, 'r-', label = "100%", lw=1)
plt.plot(numberOfmem, diff_99, 'g-', label = "99%", lw=1)
plt.plot(numberOfmem, diff_98, 'y-', label = "98%", lw=1)
#plt.plot(numberOfmem, diff_97, 'm-', label = "97%", lw=1)
#plt.plot(numberOfmem, diff_96, 'c-', label = "96%", lw=1)
#plt.plot(numberOfmem, diff_95, 'b-', label = "95%", lw=1)
plt.xlabel(r'number of members in one cluster')
plt.ylabel(r'number of clusters)')
plt.axis([1, np.amax(numberOfmem), 1, np.amax(clustercount)])

plt.savefig("plot.pdf")
	
print("============= FINISH ==================")
inFile.close()





