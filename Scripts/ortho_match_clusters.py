#!/usr/bin/python3

import os

#output_dir = "amplified_16S_clusters_new/"
output_dir = "housekeeper_clusters_new/"


if not os.path.exists(output_dir):
    os.mkdir(output_dir)

#cluster_dir = 'amplified_16S_clusters/'
cluster_dir = 'house_clusters/'


graph_output = open(output_dir + 'all_clusters_unique.tsv', 'w')
#cluster_files = os.listdir(cluster_dir)

cluster_files = ['data_100.tsv', 'data_99.tsv', 'data_98.tsv', 'data_97.tsv', 'data_96.tsv', 'data_95.tsv', 'data_94.tsv', 'data_93.tsv']
#cluster_files = ['data_100.tsv', 'data_99.tsv', 'data_98.tsv', 'data_97.tsv', 'data_96.tsv', 'data_95.tsv']

matched_sets = set([])

for line in open('final_compCollector_results.csv','r').readlines():
    file_name, total_expected, asigned, unassigned, ratio = line.split(',')
    ratio = ratio.rstrip()
    for cluster in cluster_files:
        tbl_output = open(output_dir + cluster[:-4] + '_orthocluster.tsv', 'a')
        with open(cluster_dir + cluster, 'r') as c:
            for name in c.readlines():
                name = name.rstrip()
                if name == file_name:
                    if name not in matched_sets:
                        graph_output.writelines(cluster[5:-4] + '\t' + ratio + '\n')
                        matched_sets.add(name)
                    else:
                        continue
                    tbl_output.writelines(cluster[:-4] + '\t' + ratio + '\t' + total_expected + '\t' + name + '\n')

print ("total number of clusters matched to orthos\t", str(len(matched_sets)))

print ("grep -v '-' all_clusters_unique.tsv | sort -nr | cat -n > 16S_cluster_ortho.xls")