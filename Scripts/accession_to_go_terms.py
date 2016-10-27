#!/usr/bin/python3

#input GO_stuff, accession_counts, and uniprot_converts

#output, GO_term    total_matched   total_unmatched

#anyway to get COG or KEGG from GO

import sys, os, subprocess, re
import urllib,urllib2



page = ''
file = sys.argv[1] # needed_protein_ontologies
#uniprot_out_file = open(file + "_uniprots", 'w')
output = open(file + 'KEGG.tsv', 'w')

To = 'KEGG_ID'
From = 'P_REFSEQ_AC'

print file

def uniprot_convert(space_seperated_accessions, To, From):
    ids = space_seperated_accessions
    url = 'http://www.uniprot.org/mapping/'

    params = {
    'from':From,
    'to':To,
    'format':'tab',
    'query':ids
    }

    data = urllib.urlencode(params)
    request = urllib2.Request(url, data)
    contact = "" # Please set your email address here to help us debug in case of problems.
    request.add_header('User-Agent', 'Python %s' % contact)
    response = urllib2.urlopen(request)
    page = response.read()
    query = ''  #query = 'accession:P04839%20OR%20accession:Q15067'
    for line in page.splitlines():
        if not line or line.startswith("From"):
            continue
        line = line.rstrip()
        protein, uniprot = line.split("\t")
        query += uniprot + ' '

    output.writelines(page)
    print query

count = 0
with open(file) as f:
    block = bytearray()
    counter = 0
    for line in f:
        print (line)
        block.extend(line.replace("\n", " "))
        counter += 1
        if counter >= 200:
            counter = 0
            id = (str(block))
            uniprot_convert(str(block), To, From)
            block = bytearray()
            count += 100
            print ("completed files", count)
    do_function(str(block))


