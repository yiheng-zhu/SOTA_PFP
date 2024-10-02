import sys
import os

def read_sequence(sequence_file):

    f = open(sequence_file, "r")
    text = f.read()
    f.close()

    sequence_dict = dict()

    for line in text.splitlines():
        line = line.strip()
        if(line.startswith(">")):
            name = line
        else:
            sequence = line
            sequence_dict[name[1:]] = sequence

    return sequence_dict

def extract(sequence_dict, name_file, extract_file):

    f = open(name_file, "r")
    text = f.read()
    f.close()

    name_list = text.splitlines()

    f = open(extract_file, "w")
    for i in range(len(name_list)):
        f.write(">" + name_list[i] + "\n" + sequence_dict[name_list[i]] + "\n")
    f.flush()
    f.close()


if __name__ == '__main__':

    workdir = sys.argv[1]
    type_list = ["MF", "BP", "CC"]
    data_type_list = ["train", "evaluate", "test"]

    for type in type_list:
        for data_type in data_type_list:
            sequence_dict = read_sequence(workdir + "/" + data_type + "_sequence.fasta")
            extract(sequence_dict, workdir + "/" + type + "/" + data_type + "_gene_list", workdir + "/" + type + "/" + data_type + "_sequence.fasta")







