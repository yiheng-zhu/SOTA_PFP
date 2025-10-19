import os
import sys

def copy_results(origindir, targetdir, data_type, method, round_index, iteration):

    if(round_index==-1):
        workdir = origindir + "/final_" + method + "_result/" + data_type + "/result" + str(iteration) + "/"
    else:
        workdir = origindir + "/" + method + "_result/" + data_type + "/round" + str(round_index) + "/result" + str(iteration) + "/"

    if(os.path.exists(targetdir + "/" + data_type + "/")==False):
        os.makedirs(targetdir + "/" + data_type + "/")

    os.system("cp -r " + workdir + "/* " + targetdir + "/" + data_type + "/")

    origin_label = origindir + "/" + data_type + "_gene_label"
    target_label = targetdir + "/" + data_type + "_gene_label"
    os.system("cp " + origin_label + " " + target_label)

    f = open(target_label, "r")
    text = f.read()
    f.close()

    for line in text.splitlines():
        protein_name = line.strip().split()[0]
        result_dir = targetdir + "/" + data_type + "/"
        if(os.path.exists(result_dir + "/" + protein_name)==False):
            os.makedirs(result_dir + "/" + protein_name)

if __name__=="__main__":

    dir1 = sys.argv[1]
    dir2 = sys.argv[2]

    go_type_dict = {}
    go_type_dict["MF"] = 1
    go_type_dict["BP"] = 1
    go_type_dict["CC"] = 1

    go_type_list = go_type_dict.keys()

    data_type_list = ["evaluate", "test"]
    method = "cross_entropy"
    round_index = -1

    for go_type in go_type_list:
        for data_type in data_type_list:
            origindir = dir1 + "/" + go_type + "/"
            targetdir = dir2 + "/" + go_type + "/"

            copy_results(origindir, targetdir, data_type, method, round_index, go_type_dict[go_type])



