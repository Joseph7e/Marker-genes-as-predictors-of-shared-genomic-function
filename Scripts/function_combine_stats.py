#!/usr/bin/python3


import sys

swiss = open(sys.argv[1], 'r')
trem = open(sys.argv[2], 'r')

out = open(sys.argv[3], 'w')


new_dict = {}


def add2dict(filename):
    for line in filename:
        id, match, unmatch = line.split('\t')
        id = id.replace(" ", "_")
        if id in new_dict.keys():
            new_dict[id][0] += int(match)
            new_dict[id][1] += int(unmatch)
        else:
            new_dict[id] = [int(match), int(unmatch)]


add2dict(swiss)
add2dict(trem)

def save_dict_stats(dictionary, out):
    for key, value in dictionary.items():
        out.writelines(key + '\t' + str(value[0]) + '\t' + str(value[1]) + '\n')

save_dict_stats(new_dict,out)


