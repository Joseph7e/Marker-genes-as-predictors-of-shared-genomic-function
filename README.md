# Metabarcodes as predictors of shared genomic function
Supplementary materials and scripts for paper




## Prokaryote genome dataset and gene extraction

link to NCBI prokaryote tables: https://www.ncbi.nlm.nih.gov/genome/browse#!/prokaryotes/

link to genome reports FTP: ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/

* Download the genome report file for all all of prokaryotes

```bash
# download the file
wget "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt"
```

Column 2: Taxonomy information
Column 20: Is it a reference genomes
Column 21: ftp download path

All genomes and annotation files denoted "REPR" in column 20 were downloaded following the ftp links.

## Marker Gene Extraction

The script [gene_extractor.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/gene_extractor.py) was used to extract genes sequences from genomes based on gff annotations.

Annotations for 16S rRNA and each housekeeping genes used in this study are hard coded into the script. For example, the 16S genes must contain "16S" in the annotation and be of type ("Rrna", "rrna","rRNA").


### V4 dataset specific method

The V4 region of the 16S rRNA was extracted in silico using [fasta_amplify](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/fasta_amplify.py)


### MLSA dataset specific method

Single-copy genes used in the MLSA-like dataset were concatenated together using [concat_housekeeping_genes.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/concat_housekeeping_genes.py)




