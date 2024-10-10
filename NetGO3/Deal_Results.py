import sys
import os
import Find_Parents as fp

def read_results(result_file):

    f = open(result_file, "r")
    text = f.read()
    f.close()

    result_dict = dict()

    result_dict["MF"] = dict()
    result_dict["BP"] = dict()
    result_dict["CC"] = dict()


    for line in text.splitlines():
        line = line.strip()
        if(len(line)==0):
            continue
        if(line.startswith("=")):
            continue

        values = line.split("\t")
        protein_id = values[0]
        term = values[1]
        score = values[2]
        go_type = values[3].upper()

        if(protein_id not in result_dict[go_type]):
            result_dict[go_type][protein_id] = []
        result_dict[go_type][protein_id].append(term + " " + go_type[1] + " " + score)

    return result_dict






def deal_results(result_dict, result_dir, term_list_file, obo_dict, type):

    f = open(term_list_file, "r")
    text = f.read()
    f.close()
    term_list = text.splitlines()

    for name in result_dict[type]:
        current_dir = result_dir + "/" + name + "/"
        os.makedirs(current_dir)

        result_file = current_dir + "/netgo_" + type
        f = open(result_file, "w")
        for line in result_dict[type][name]:
            term = line.split()[0]
            if(term in term_list):
                f.write(line + "\n")
        f.close()

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
            result_dict = read_results(workdir + "/" + data_type + "_result.txt")
            result_dir = workdir + "/benchmark/" + type + "/" + data_type + "/"
            os.system("rm -rf " + result_dir)
            term_list_file = workdir + "/" + type + "_term_list"
            deal_results(result_dict, result_dir, term_list_file, obo_dict, type)








