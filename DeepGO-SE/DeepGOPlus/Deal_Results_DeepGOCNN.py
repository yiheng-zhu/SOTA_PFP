import sys
import os
import pandas as pd

def read_name_list(name_file):

    f = open(name_file, "r")
    text = f.read()
    f.close()

    return text.splitlines()

def post_deal(result_file, name_list_file, term_list_file, resultdir, type):

    name_list = read_name_list(name_list_file)
    term_list = read_name_list(term_list_file)

    df = pd.read_pickle(result_file)
    pro_array = df["preds"]

    for i in range(len(pro_array)):

        temp_dir = resultdir + "/" + name_list[i] + "/"
        os.makedirs(temp_dir)
        result_file = temp_dir + "/deepgocnn_" + type
        f = open(result_file, "w")
        for j in range(len(term_list)):
            if(pro_array[i][j]>=0.01):
                f.write(term_list[j] + " " + type[1] + " " + str(pro_array[i][j]) + "\n")
        f.close()



if __name__ == '__main__':

    workdir = sys.argv[1]
    obo_dict = None
    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]

    for type in type_list:
        for data_type in data_type_list:

            result_file = workdir + "/" + type + "/" + data_type + "_predictions_deepgocnn.pkl"
            result_dir = workdir + "/" + type + "/" + data_type + "/"
            name_list_file = workdir + "/" + type + "/" + data_type + "_gene_list"
            os.system("rm -rf " + result_dir)
            term_list_file = workdir + "/" + type + "/term_list"

            post_deal(result_file, name_list_file, term_list_file, result_dir, type)






