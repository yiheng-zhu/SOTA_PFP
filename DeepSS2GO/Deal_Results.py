import sys
import os
import Find_Parents as fp

def read_results(result_file, type):

    f = open(result_file, "r")
    text = f.read()
    f.close()

    result_dict = dict()

    for line in text.splitlines():
        line = line.strip()
        if(len(line)==0):
            continue
        values = line.strip().split(",")
        if(values[0] not in result_dict):
            result_dict[values[0]] = []
        result_dict[values[0]].append(values[1].strip() + " " + type[1] + " " + values[len(values)-1])

    return result_dict


def write_results(result_dir, term_list_file, obo_dict, result_dict, type):

    for name in result_dict:

        temp_dir = result_dir + "/" + name + "/"
        if(os.path.exists(temp_dir)==False):
            os.makedirs(temp_dir)

        result_file = temp_dir + "/deepssgo_" + type
        f = open(result_file, "w")
        for value in result_dict[name]:
            f.write(value + "\n")
        f.close()

        deal_results(result_file, result_file, term_list_file, obo_dict, type)




def deal_results(origin_result_file, deal_result_file, term_list_file, obo_dict, type):

    f = open(term_list_file, "r")
    text = f.read()
    f.close()
    term_list = text.splitlines()

    f = open(origin_result_file, "r")
    text = f.read()
    f.close()

    f = open(deal_result_file, "w")

    line_set = text.splitlines()
    for i in range(1, len(line_set)):

        line = line_set[i]
        values = line.strip().split()
        if(values[0] in term_list):
            f.write(values[0] + " " + values[1] + " " + values[2] + "\n")

    f.close()

    fp.find_parents_from_file(deal_result_file, deal_result_file + "_new", obo_dict)
    fp.sort_result(deal_result_file)
    fp.sort_result(deal_result_file + "_new")



if __name__ == '__main__':

    workdir = sys.argv[1]
    obo_dict = fp.get_obo_dict()
    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]

    for type in type_list:
        for data_type in data_type_list:
            result_dict = read_results(workdir + "/" + data_type + "_results_" + type.lower() + ".csv", type)
            result_dir = workdir + "/benchmark/" + type + "/" + data_type + "/"
            os.system("rm -rf " + result_dir)
            term_list_file = workdir + "/" + type + "_term_list"
            write_results(result_dir, term_list_file, obo_dict, result_dict, type)








