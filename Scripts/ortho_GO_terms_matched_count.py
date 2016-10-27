#!/usr/bin/python3

#input GO_stuff, accession_counts, and uniprot_converts

#output, GO_term    total_matched   total_unmatched

#anyway to get COG or KEGG from GO

output = open("GO_matched_unmatched.tsv", 'w')
output.writelines("GO_term\tmatched\tunmatched\t[accession_list]\n")

accession_file = open(sys.argv[1], 'r') # accession \t matched \t unmatched
uniprots_file = open(sys.argv[2], 'r') # accession \t uniprot
go_file = open(sys.argv[3], 'r') #uniprot \t bio \t mol \t cell

for line in go_file:
    if line.startswith("Entry"):
        continue
    else:
        line = line.rstrip()
        uniprot_go, go_bio, go_mol, go_cell = line.split("\t")
        try:
            bios = go_bio.split(;):

        for line in uniprots_file:
            line = line.rstrip()
            accession_un, uniprot = line.split("\t")
            for line in accession_file:
                accession, matched, unmatched = line.split("\t")
                if accession == accession_un and uniprot == uniprot_go:

