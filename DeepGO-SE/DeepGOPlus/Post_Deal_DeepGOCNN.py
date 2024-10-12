import sys
import os
import pandas as pd
import Find_Parents as fp

def read_name_list(name_file):

    f = open(name_file, "r")
    text = f.read()
    f.close()

    return text.splitlines()

def post_deal(name_list_file, resultdir, obo_dict, type):

    name_list = read_name_list(name_list_file)
    for i in range(len(name_list)):

        temp_dir = resultdir + "/" + name_list[i] + "/"
        result_file = temp_dir + "/deepgocnn_" + type

        fp.find_parents_from_file(result_file, result_file + "_new", obo_dict)
        fp.sort_result(result_file)
        fp.sort_result(result_file + "_new")


if __name__ == '__main__':

    workdir = sys.argv[1]
    obo_dict = fp.get_obo_dict()
    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]

    for type in type_list:
        for data_type in data_type_list:

            result_file = workdir + "/" + type + "/" + data_type + "_predictions_deepgocnn.pkl"
            result_dir = workdir + "/" + type + "/" + data_type + "/"
            name_list_file = workdir + "/" + type + "/" + data_type + "_gene_list"

            post_deal(name_list_file, result_dir, obo_dict, type)






