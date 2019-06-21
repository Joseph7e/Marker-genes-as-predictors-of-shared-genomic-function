# Metabarcodes as predictors of shared genomic function
Supplementary materials and scripts.

Release: https://doi.org/10.5281/zenodo.1309979

[Link to data sheets](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/tree/master/Data)




## Prokaryote genome dataset

link to NCBI prokaryote tables: https://www.ncbi.nlm.nih.gov/genome/browse#!/prokaryotes/

link to genome reports FTP: ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/

* Download the genome report file for all all of prokaryotes

```bash
# download the file
wget "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt"
```

Column 2: Taxonomy information,
Column 20: Reference Genome flag, and
Column 21: ftp download path

All genomes and annotation files denoted "REPR" in column 20 were downloaded following the ftp links.

## Marker Gene Extraction

The script [gene_extractor.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/gene_extractor.py) was used to extract genes sequences from genomes based on gff annotations.

Annotations for 16S rRNA and each housekeeping genes used in this study are hard coded into the script. For example, the 16S genes must contain "16S" in the annotation and be of type ("Rrna", "rrna","rRNA").

* V4 dataset specific method

The V4 region of the 16S rRNA was extracted in silico using [fasta_amplify](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/fasta_amplify.py)

* MLSA dataset specific method

Single-copy genes used in the MLSA-like dataset were concatenated together using [concat_housekeeping_genes.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/concat_housekeeping_genes.py)


## Intra Organism 16S rRNA variation

The script [variation_stats.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/variation_stats.py) was used to output gene copy number, lengths, and variation stats from each genome.


## Sequence clustering

Marker gene clustering was completed using [uclustPipeline.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/uclustPipeline.py)

UCLUST is available from https://drive5.com/usearch/manual/uclust_algo.html

Parsing clustering data was completeed using [parse_uclust.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/parse_uclust.py)

Python scripts beginning with "clustering" were used to construct input tables for "marker gene clustering" figures (currently Figure 4).


## Percent shared genes

Given a list of genomes to compare the script [auto_orthofinder.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/auto_orthofinder.py) runs orthofinder on all genomes.

The program orthofinder.py is available from https://github.com/davidemms/OrthoFinder

The script [orthofinder_parse_for_percent_shared_genes.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/orthofinder_parse_for_percent_shared_genes.py) is used to parse orthofinder output and provide a table of percent shared genes.


## Comparing percent shared genes with marker gene identity

Given parsed output from "Sequencing clustering" and "Percent shared genes" the script [combine_ortho_and_uclust.py](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/blob/master/Python%20Scripts/combine_ortho_and_uclust.py) constructs a table with the columns percent identity, and percent shared genes.



## Functional analysis

All scripts used to construct figures and data tables for the functional analysis are available in the [functional_methods/](https://github.com/Joseph7e/Marker-genes-as-predictors-of-shared-genomic-function/tree/master/Python%20Scripts/functional_methods)
