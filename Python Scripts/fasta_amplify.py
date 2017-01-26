#!/usr/local/bin/python3
#
#	fasta_amplify.py fastafile
#		Read a fasta file and extract variable regions from  
#		16S genes by two input: Forward primer and Reverse primer 
#
#   @Ying Zhang
#   04/28/16
import os
import sys
import csv
import re
import string


# forward primer and reverse primer
#forwoardPrimer = 'GTG[CT]CAGC[CA]GCCGCGGTAA'
#reversePrimer = 'AAACT[TC]AAA[GT][GA]AATTG[GA]CGG'

forwoardPrimer = reversePrimer = ''
forwoardPrimer_len = reversePrimer_len = 0

# dictionary for reverse and complement sequences
ATGC=['A','T','G','C']
Base = {'R':"AG", 'Y':"CT", 'M':"CA", 'K':"TG", 'W':"TA",
	'S':"CG", 'B':"CTG", 'D':"ATG", 'H':"ATC", 'V':"ACG", 
	'N':"ACGT",'A':"A", 'C':"C", 'G':"G", 'T':"T"}
comp_dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}


# an output file save header and variable regions
outFile = open("fasta_amplified_rrna", 'w')
# an output summary counting number of extracted seq
outSum = open("fasta_amplified_rrna_summary",'w')
outSum.write("GCF_number	original_count	extracted_count\n")

#-------------------------- usage() ---------------------------------------
#----- usage test 
#      If we have no arguments or the first argument is -h
#      print some "usage" information and quit.
usageMsg = '''
Usage:
	fasta_amplify.py fastafile forwoardPrimer reversePrimer
	Read a fasta file and extract variable regions from  
	16S genes by two input: Forward primer and Reverse primer 
'''
def usage():
    if len( sys.argv ) < 4 or sys.argv[ 1 ] == "-h":  # command 
        print( usageMsg )
        exit(0)

def Degeneracy(seq):
	ret_seq = ''
	for x in seq:
		if x in ATGC:
			tmp = Base[x]
		else:
			tmp = '['+ Base[x] +']'
		ret_seq += tmp
	return ret_seq

def comp_seq(seq):
	'''
		complement sequences.
	'''
	ret_seq = ''
	for x in seq:
		if x in ATGC:
			ret_seq += comp_dict[x]
		else:
			ret_seq += x
	return ret_seq


def createRegExp():
	'''
		read in forwoardPrimer and reversePrimer and return
		a regular expression for searching
	'''
	ret = ''
	# 'GTG[CT]CAGC[CA]GCCGCGGTAA(.*)AAACT[TC]AAA[GT][GA]AATTG[GA]CGG'
	forwoardPrimer_len = len(forwoardPrimer)
	reversePrimer_len = len(reversePrimer)
	
	# forwoardPrimer/reversePrimer reverse and complement
	fp = Degeneracy(forwoardPrimer)
	rp = comp_seq( Degeneracy(reversePrimer[::-1]) )
	
	ret = fp + '(.*)' + rp
	return ret


#-----------------------------------------------------------------------      
#--------------------------- main --------------------------------------
# check argument usage correctness
usage()

#----- open input file
inFile = sys.argv[ 1 ]
try:
	inFile = open( inFile, 'r' )
except ( OSError, IOError ) as e:
	print( 'Unable to open ', inFile )


# regular expression
forwoardPrimer = sys.argv[2]
reversePrimer = sys.argv[3]
regExp = createRegExp()

#regExp = forwoardPrimer+'(.*)'+reversePrimer
pat = re.compile(regExp)

orig_count = 0
ext_count = 0
header = inFile.readline()
lastGCF = (header.split("_")[0]+"_"+header.split("_")[1])[1:]

orig_total = 0
ext_total = 0 

while header != '':
	# check if it is correct header line
	if not header.startswith('>'):
		header = inFile.readline()
		continue
	# get current GCF number according to header
	curGCF = (header.split("_")[0]+"_"+header.split("_")[1])[1:]
	if lastGCF == curGCF:
		orig_count += 1
	else:
		line = lastGCF+"	"+str(orig_count)+"	"+str(ext_count)
		if(orig_count != ext_count):
			line = "*" + line
		outSum.write(line+"\n")
		
		orig_total += orig_count
		ext_total += ext_count
		
		# clean counts
		orig_count = 1
		ext_count = 0
		lastGCF = curGCF
	
	# search for match part
	seq = inFile.readline()
	result = pat.search(seq)
	if result != None:
		start_pos =result.span()[0]
		end_pos =result.span()[1]
		matchPart = seq[start_pos+forwoardPrimer_len:end_pos-reversePrimer_len]
		
		outFile.write(header)
		outFile.write(matchPart+"\n")
		ext_count +=1
	
	#read a new header line for next loop
	header = inFile.readline()

# print statical output:
print("total number of original rRNA:", orig_total)
print("total number of captured rRNA:", ext_total)
print("total number of lost rRNA:", orig_total-ext_total)
print("missing percentage: ", (orig_total-ext_total)/orig_total)	
