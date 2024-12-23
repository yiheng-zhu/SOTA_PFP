import sys
import os
import numpy as np
import Find_Parents as fp
from decimal import Decimal

def write_results(origin_result_file, result_dir, label_file, term_list_file, obo_dict, type, method_name):

    preds = np.load(origin_result_file)

    f = open(label_file, "r")
    text = f.read()
    f.close()
    line_set = text.splitlines()

    f = open(term_list_file, "r")
    text = f.read()
    f.close()
    term_list = text.splitlines()

    for i in range(len(line_set)):
        protein_name = line_set[i].strip().split()[0]
        tempdir = result_dir + "/" + protein_name + "/"
        if(os.path.exists(tempdir)==False):
            os.makedirs(tempdir)
        result_file = tempdir + "/" + method_name + "_" + type
        f = open(result_file, "w")
        for j in range(len(term_list)):
            if(preds[i][j]>=0.01):
                f.write(term_list[j] + " " + type[1] + " " + str(Decimal(str(preds[i][j])).quantize(Decimal("0.000"))) + "\n")
        f.close()
        fp.find_parents_from_file(result_file, result_file + "_new", obo_dict)
        fp.sort_result(result_file)
        fp.sort_result(result_file + "_new")

if __name__ == '__main__':

    workdir = sys.argv[1]
    obo_dict = fp.get_obo_dict()
    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]
    method_name = "deepgozero"

    for type in type_list:
        for data_type in data_type_list:
            origin_result_file = workdir + "/final_" + data_type + "_" + method_name + "_" + type.lower() + ".npy"
            result_dir = workdir + "/" + type + "/" + data_type + "/"
            label_file = workdir + "/" + type + "/" + data_type + "_gene_label"
            term_list_file = workdir + "/" + type + "/term_list"
            write_results(origin_result_file, result_dir, label_file, term_list_file, obo_dict, type, method_name)








