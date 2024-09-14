import sys
import os
import Find_Parents as fp

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
        values = line.strip().split(",")
        if(values[1] in term_list):
            f.write(values[1] + " " + type[1] + " " + values[2] + "\n")

    f.close()

    fp.find_parents_from_file(deal_result_file, deal_result_file + "_new", obo_dict)
    fp.sort_result(deal_result_file)


if __name__ == '__main__':

    dir = sys.argv[1]
    obo_dict = fp.get_obo_dict()
    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]

    for data_type in data_type_list:
        workdir = dir + "/" + data_type + "/"
        name_list = os.listdir(workdir)
        for type in type_list:
            term_list_file = dir + "/" + type + "_term_list"
            for name in name_list:
                origin_result_file = workdir + "/" + name + "/output/" + type.lower() + "_result.csv"
                deal_result_file = workdir + "/" + name + "/output/annopro_" + type
                deal_results(origin_result_file, deal_result_file, term_list_file, obo_dict, type)







