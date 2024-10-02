import os
import sys
from decimal import Decimal
import numpy as np
import Find_Parents as fp

diamond_dir = "/data/yihengzhu/toolbars/sequence_homology_tools/DIOMAND/"

def format_database(sequence_file, database_file):

    os.system(diamond_dir + "/diamond makedb --in " + sequence_file + " -d " + database_file)


def read_name_list(name_file):

    f = open(name_file, "r")
    text = f.read()
    f.close()

    return text.splitlines()

def read_go(gofile):

    f = open(gofile, "r")
    text = f.read()
    f.close()

    go_dict = dict()

    for line in text.splitlines():
        line = line.strip()
        values = line.split()
        go_dict[values[0]] = values[1].split(",")

    return go_dict

def read_name_list_from_sequence_file(sequence_file):

    name_list = []

    f = open(sequence_file, "r")
    text = f.read()
    f.close()

    for line in text.splitlines():
        line = line.strip()
        if (line.startswith(">")):
            name_list.append(line[1:])

    return name_list

def predict_diamond(test_sequence_file, database_file, train_label_file, term_file, result_dir, go_type, obo_dict):

    os.system("rm -rf " + result_dir)

    output = os.popen(diamond_dir + "/diamond blastp -d " + database_file + " -q " + test_sequence_file + " --more-sensitive --outfmt 6 qseqid sseqid bitscore").readlines()
    test_bits = {}
    test_train = {}

    for lines in output:
        line = lines.strip('\n').split()
        if line[0] in test_bits:
            test_bits[line[0]].append(float(line[2]))
            test_train[line[0]].append(line[1])
        else:
            test_bits[line[0]] = [float(line[2])]
            test_train[line[0]] = [line[1]]

    train_go_dict = read_go(train_label_file)
    term_list = read_name_list(term_file)
    label_dict = dict()
    
    for name in train_go_dict:
        current_term_list = train_go_dict[name]
        temp_list = []
        for term in current_term_list:
            temp_list.append(term_list.index(term))

        label_dict[name] = temp_list

    nlabels = len(term_list)

    test_name_list = read_name_list_from_sequence_file(test_sequence_file)

    for name in test_name_list:
        probs = np.zeros(nlabels)
        if name in test_bits:
            weights = np.array(test_bits[name]) / np.sum(test_bits[name])

            for j in range(len(test_train[name])):
                temp = np.zeros(nlabels)
                temp[label_dict[test_train[name][j]]] = 1.0
                probs += weights[j] * temp

        result_list = []
        for i in range(len(probs)):
            if(probs[i]>=0.01):
                result_list.append([probs[i], term_list[i]])

        result_list = sorted(result_list, reverse=True)

        os.makedirs(result_dir + "/" + name + "/")

        resultfile = result_dir + "/" + name + "/DIOMAND_" + go_type
        f = open(resultfile, "w")
        for value, term in result_list:
            f.write(term + " " + go_type[1] + " " + str(Decimal(value).quantize(Decimal("0.000"))) + "\n")
        f.close()

        fp.find_parents_from_file(resultfile, resultfile + "_new", obo_dict)
        fp.sort_result(resultfile)


def diomand_process(workdir, go_type, data_type, obo_dict):

    train_sequence_file = workdir + "/" + go_type + "/train_sequence.fasta"
    database_file = workdir + "/" + go_type + "/train_sequence.dmnd"
    format_database(train_sequence_file, database_file)

    test_sequence_file = workdir + "/" + go_type + "/" + data_type + "_sequence.fasta"
    term_file = workdir + "/" + go_type + "/term_list"
    train_label_file = workdir + "/" + go_type + "/train_gene_label"
    result_dir = workdir + "/" + go_type + "/" + data_type + "/"

    predict_diamond(test_sequence_file, database_file, train_label_file, term_file, result_dir, go_type, obo_dict)




if __name__ == "__main__":

    workdir = sys.argv[1]
    go_type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]
    obo_dict = fp.get_obo_dict()

    for go_type in go_type_list:
        for data_type in data_type_list:
            diomand_process(workdir, go_type, data_type, obo_dict)
