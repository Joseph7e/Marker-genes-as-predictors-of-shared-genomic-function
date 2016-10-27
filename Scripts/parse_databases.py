#!/usr/bin/python

import os, sys, gzip, re, io, pickle

swiss = gzip.open(sys.argv[1], 'rt')
#swiss = io.BufferedReader(gzip.open(sys.argv[1], 'rt'))
swiss_dict = {}


web = 'http://downloads.sourceforge.net/project/mugsy/mugsy_x86-64-v1r2.2.tgz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fmugsy%2Ffiles%2F&ts=1456242384&use_mirror=iweb'


ID = ''
uniprot = ''
refseqs = []
gos = []
count = 0; real_count = 0

for line in swiss:
    count += 1
    real_count += 1
    if count == 500000:
        print (real_count)
        count = 0
    if line.startswith("ID"):
        if refseqs:
            swiss_dict[ID] = [refseqs, gos]
        ID = ''; uniprot = ''; refseqs = []; gos = []
        ID = re.findall(r"ID\s*(.*?)\s", line)[0]
    if line.startswith("AC"):
        uniprot = re.findall(r"AC\s*(.*?);", line)
        uniprot = uniprot[0]
    if line.startswith("DR") and "RefSeq" in line:
        refseq = re.findall(r"RefSeq;\s*(.*?);", line)
        refseqs.append(refseq[0])
    if line.startswith("DR") and "GO" in line:
        go = re.findall(r"GO;(.*);", line)
        try:
            gos.append(go[0])
        except IndexError:
            continue

print (len(swiss_dict))

with open('go_dict2.pickle', 'wb') as handle:
    pickle.dump(swiss_dict, handle)