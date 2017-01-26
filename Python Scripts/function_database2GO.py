import os, sys, gzip, re
#Author: Joseph Sveigny
#Purpose: Given list of matched and unmatched counts with accession, provide GO information and total counts for the terms.



accession_dict = {} #accession:[match,unmatch]
print ("building accession dictionary")

#accession_file = open('/home/genome/joseph7e/gene_16S/analysis_orthofinder/cluster_99_accession_matches', 'r')
#accession_file = open('/home/genome/joseph7e/gene_16S/analysis_orthofinder/matched_unmatched_proteins.tsv', 'r')
accession_file = open('/home/genome/joseph7e/gene_16s_redo_all/new_functional_analysis/matched_unmatched_proteins97_good.tsv','r')
for line in accession_file:
    line = line.rstrip()
    accession, match, unmatch = line.split("\t")
    accession_dict[accession] = [match,unmatch]


#### Construct Dictionaries
print ("importing data and creating Gene Ontology Dictionaries")
swiss = gzip.open(sys.argv[1], 'rt') #gzipped database file


bio_dict = {} #P --> go: [accessions]
mol_dict = {} #F --> go: [accessions]
cell_dict = {} #C --> go: [accessions]
ID = ''
uniprot = ''
accessions = [] # accessions?
gos = []
count = 0; real_count = 0; acc_count = 0



for line in swiss:
    count += 1
    real_count += 1
    if count == 5000:
        print (real_count, acc_count)
        count = 0
    if line.startswith("ID"):
        if len(accessions) > 0 and len(gos) > 0:
            # for acc, score in accession_dict.items():
            for a in accessions:
                if a in accession_dict.keys():
                    acc_count += 1
                    score = accession_dict[a]
                # if acc in a: # could be if acc in accessions
                    bios = re.findall(r"P:(.*?)[,']", str(gos))
                    mols = re.findall(r"F:(.*?)[,']", str(gos))
                    cells = re.findall(r"C:(.*?)[,']", str(gos))
                    for b in bios:
                        if b in bio_dict.keys():
                            bio_dict[b][0] += int(score[0])
                            bio_dict[b][1] += int(score[1])
                        else:
                            bio_dict[b] = [int(score[0]), int(score[1])]
                    for m in mols:
                        if m in mol_dict.keys():
                            mol_dict[m][0] += int(score[0])
                            mol_dict[m][1] += int(score[1])
                        else:
                            mol_dict[m] = [int(score[0]), int(score[1])]
                    for c in cells:
                        if c in cell_dict.keys():
                            cell_dict[c][0] += int(score[0])
                            cell_dict[c][1] += int(score[1])
                        else:
                            cell_dict[c] = [int(score[0]), int(score[1])]


            #swiss_dict[ID] = [refseqs, gos]
        ID = ''; accessions = []; gos = []#; uniprot = ''
        ID = re.findall(r"ID\s*(.*?)\s", line)[0]
    # if line.startswith("AC"):
    #     uniprot = re.findall(r"AC\s*(.*?);", line)
    #     uniprot = uniprot[0]
    if line.startswith("DR") and "RefSeq" in line:
        refseq = re.findall(r"RefSeq;\s*(.*?);", line)
        accessions.append(refseq[0][:-2])
    if line.startswith("DR") and "GO;" in line:
        go = re.findall(r"GO;(.*);", line)
        try:
            gos.append(go[0])
        except IndexError:
            continue


print ("Saving information to output")

output_bio = open('gene_ontology_enrichment_Bio.tsv','w')
output_mol = open('gene_ontology_enrichment_Mol.tsv','w')
output_cell = open('gene_ontology_enrichment_Cell.tsv','w')


def save_dict_stats(dictionary, out):
    for key, value in dictionary.items():
        out.writelines(key + '\t' + str(value[0]) + '\t' + str(value[1])+ '\n')

save_dict_stats(bio_dict, output_bio)
save_dict_stats(mol_dict, output_mol)
save_dict_stats(cell_dict, output_cell)