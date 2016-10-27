#!/usr/bin/python3

import sys, os, subprocess, re
import urllib,urllib2



page = ''
file = sys.argv[1] # needed_protein_ontologies
uniprot_out_file = open(file + "_uniprots", 'w')
output = open(file + '_gene_ontology.tsv', 'w')

def uniprot_convert(space_seperated_accessions):
    ids = space_seperated_accessions
    url = 'http://www.uniprot.org/mapping/'

    params = {
    'from':'P_REFSEQ_AC',
    'to':'ACC',
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
        add = 'accession:' + uniprot + '%20OR%20'
        query += add
    query = query[:-8]
    url = 'http://www.uniprot.org/uniprot/?sort=score&desc=&compress=no&query='+ query + '&fil=&force=no&format=tab&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length,annotation%20score,go(biological%20process),go(molecular%20function),go(cellular%20component)'
    command = ["curl", url]
    try:
        sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        standard_out = str(sp.communicate()[0].decode('ascii'))
    except OSError:
        print command
    for line in standard_out.splitlines():
        try:
            Entry, Entry_name, Status, Protein_names, Gene_names, Organism, Length, Annotation, GO_Bio, GO_Mol, GO_Cell = line.split("\t")
            output.writelines(Entry + '\t' + GO_Bio + '\t' + GO_Mol + '\t' + GO_Cell + '\n')
        except ValueError:
            continue
    uniprot_out_file.writelines(page)

count = 0
with open(file) as f:
    block = bytearray()
    counter = 0
    for line in f:
        block.extend(line.replace("\n", " "))
        counter += 1
        if counter >= 100:
            counter = 0
            id = (str(block))
            uniprot_convert(str(block))
            block = bytearray()
            count += 100
            print ("completed files", count)
    uniprot_convert(str(block))


