import sys
import os

def extract_name(result_file, family_file, map_file):

    f = open(result_file, "r")
    text = f.read()
    f.close()

    line_set = text.splitlines()

    family_list = []
    map_dict = dict()

    for line in line_set[2:]:
        line = line.strip()
        if(len(line)>0):
            values = line.split()
            family_list.append(values[1])

            protein = values[0]
            if(protein not in map_dict):
                map_dict[protein] = []
            map_dict[protein].append(values[1])

    family_list = list(set(family_list))

    f = open(family_file, "w")
    for name in family_list:
        f.write(name+"\n")
    f.flush()
    f.close()

    f = open(map_file, "w")
    for protein in map_dict:
        line = protein
        value_list = list(set(map_dict[protein]))
        for value in value_list:
            line = line + " " + value
        f.write(line+"\n")
    f.flush()
    f.close()


extract_name(sys.argv[1], sys.argv[2], sys.argv[3])