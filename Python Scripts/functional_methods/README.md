
# Usage Examples:


## function_combine_stats.py

This program combines uniprots swiss-prot and tremble protein databases. Entries are cross checked and redundant entires are removed.
Databases can be installed from https://www.uniprot.org/downloads
```
wget "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"
wget "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.dat.gz"
```

Usage: python3 function_combine_stats.py uniprot_sprot.dat.gz uniprot_trembl.dat.gz <output_file.txt>


## function_pcg_shared_unshared.py

This script is used to parse a directory of results from 'Orthofinder.py' and construct lists of accessions that are found with shared and unshared files. The input to the program is a list of paths to orthofinder results files. this file must be in the current directory and be calles 'all_amplified_99_comparisons.txt'. which is hardcoded into the script.

Usage: python3 function_pcg_shared_unshared.py


## function_convert_uniprot_parsing.py

Given the output from 'function_pcg_shared_unshared.py' this script parses the dataa and constructs output tables with numbers of matched and unmatched counts for GO terms in each of the three GO categories, 'Biological process', 'Molecular function', and 'Cellular Component.' 


## function_final_statistics.py

Input lists output from function_convert_uniprot, output final docs with siginificance measures used for paper. Three output files are produced. One for significantly matched GO terms, one for significanty unmatched terms, and one with all terms with a p-value < 0.01.

Usage: python3 function_final_statistics.py <sorted_functional_significance_mol.tsv>


## function_database2GO

An extra script that can be used to link GO accessions (typicaly parsed from the script above) to the swiss prot or tremble database. The output from 'function_convert_uniprot_parsing.py' is hardcoded into the script. The datbase (tremble or swiss-prot) is given as a command line argument.


## function_final_clouds.py

Takes two files and constructs word cloud figures, one for each. The input files are tsvs where the first two columns must be a term (typically a GO term) and a count for that term. The count is used as the weight for the size of the term in the word cloud.


## mycloud.py

Functions used for the 'functional_final_clouds.py' script.
