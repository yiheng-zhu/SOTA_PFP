import os
import sys
import Find_Parents as fp

def read_result(result_file):

    if(os.path.exists(result_file)==False):
        return dict()

    f = open(result_file, "r")
    text = f.read()
    f.close()

    result_dict = dict()
    for line in text.splitlines():
        line = line.strip()
        values = line.split()
        result_dict[values[0]] = values[2]

    return result_dict

def combine_result_single(result_file1, result_file2, result_file3, type, w, obo_dict):

    result_dict1 = read_result(result_file1)
    result_dict2 = read_result(result_file2)


    term_list = []
    term_list1 = result_dict1.keys()
    term_list2 = result_dict2.keys()

    term_list.extend(term_list1)
    term_list.extend(term_list2)
    term_list = list(set(term_list))

    result_dict = dict()
    for term in term_list:
        value1 = 0
        value2 = 0
        if(term in result_dict1):
            value1 = float(result_dict1[term])
        if(term in result_dict2):
            value2 = float(result_dict2[term])

        value = w * value1 + (1-w) * value2
        result_dict[term] = value

    f = open(result_file3, "w")
    for term in term_list:
        f.write(term + " " + type[1] + " " + str(result_dict[term]) + "\n")
    f.flush()
    f.close()

    new_file = result_file3 + "_new"
    fp.find_parents_from_file(result_file3, new_file, obo_dict)
    fp.sort_result(new_file)

def combine_result(result_dir1, result_dir2, result_dir3, w, obo_dict):

    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]
    for type in type_list:
        for data_type in data_type_list:

            name_list = os.listdir(result_dir1 + "/" + type + "/" + data_type + "/")

            for name in name_list:

                if (os.path.exists(result_dir3 + "/" + type + "/" + data_type + "/" + name) == True):
                    os.system("rm -rf " + result_dir3 + "/" + type + "/" + data_type + "/" + name)
                os.makedirs(result_dir3 + "/" + type + "/" + data_type + "/" + name)

                result_file1 = result_dir1 + "/" + type + "/" + data_type + "/" + name + "/protein_Result_" + type + "_new"
                result_file2 = result_dir2 + "/" + type + "/" + data_type + "/" + name + "/final_cross_entropy_" + type + "_new"
                result_file3 = result_dir3 + "/" + type + "/" + data_type + "/" + name + "/hpgo_plus_" + type
                combine_result_single(result_file1, result_file2, result_file3, type, w, obo_dict)

    print("w=" + str(w) + ":")
    pipeline_list = ["hpgo_plus"]

    type_list = ["MF", "BP", "CC"]
    for type in type_list:

        print(type + ":")

        for pipeline in pipeline_list:
            dir = result_dir3 + "/" + type + "/"

            result_dir = dir + "/evaluate/"
            label_file = dir + "/evaluate_gene_label"
            rocfile = dir + "/evaluate_roc"

            evaluate(label_file, result_dir, rocfile, type, pipeline)

            result_dir = dir + "/test/"
            label_file = dir + "/test_gene_label"
            rocfile = dir + "/test_roc"

            evaluate(label_file, result_dir, rocfile, type, pipeline)

    print("\n")

    #os.system("python /data/yihengzhu/GOA/resource/benchmark/pythonfile/evaluate_all_sota_methods.py " + result_dir3)


import sys
import Evaluation as ev
import Get_Meatures_From_T as gf
import os

def evaluate(labelfile, result_dir, rocfile, type, pipeline):

    e = ev.evaluation(labelfile, result_dir, pipeline + "_" + type + "_new", rocfile)
    e.process()
    aupr = e.get_aupr()

    measures_list = gf.get_measures_files(rocfile, rocfile)
    line = ""
    for measures in measures_list:
        line = line + measures + " "
    line = line + "AUPR=" + str(aupr) + " AUC=" + str(e.get_auc())

    print(pipeline + ":  " + line)


if __name__ == '__main__':

    for w in range(1, 101, 1):

        workdir = sys.argv[1]

        result_dir1 = workdir + "/sagp/"
        result_dir2 = workdir + "/tale/"
        result_dir3 = workdir + "/taleplus/"
        obo_dict = fp.get_obo_dict()

        combine_result(result_dir1, result_dir2, result_dir3, w/100.0, obo_dict)






