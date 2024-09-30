import sys
import os
import Find_Parents as fp

def read_results(result_file):

    f = open(result_file, "r")
    line = f.readline()
    line = f.readline()
    line = f.readline()

    term_list_dict = dict()
    term_list_dict["MF"] = line.strip().split(";")
    line = f.readline()
    line = f.readline()
    line = f.readline()

    term_list_dict["BP"] = line.strip().split(";")
    line = f.readline()
    line = f.readline()
    line = f.readline()

    term_list_dict["CC"] = line.strip().split(";")
    line = f.readline()

    term_number_dict = dict()

    term_number_dict["MF"] = len(term_list_dict["MF"])
    term_number_dict["BP"] = len(term_list_dict["BP"])
    term_number_dict["CC"] = len(term_list_dict["CC"])

    #print(term_list_dict["MF"])
    #print(term_list_dict["BP"])
    #print(term_list_dict["CC"])
    line = f.readline()

    pro_list_dict = dict()
    while(line):

        line = f.readline()
        protein_id = line.strip()
        if(len(protein_id)==0):
            break

        pro_list_dict[protein_id] = dict()

        line = f.readline()
        go_type = line.strip()[0:2]
        line = f.readline()
        pro = line.strip().split(";")
        pro_list_dict[protein_id][go_type] = pro
        if(len(pro)!=term_number_dict[go_type]):
            print("term error")
            exit()

        line = f.readline()
        go_type = line.strip()[0:2]
        line = f.readline()
        pro = line.strip().split(";")
        pro_list_dict[protein_id][go_type] = pro
        if (len(pro) != term_number_dict[go_type]):
            print("term error")
            exit()

        line = f.readline()
        go_type = line.strip()[0:2]
        line = f.readline()
        pro = line.strip().split(";")
        pro_list_dict[protein_id][go_type] = pro
        if (len(pro) != term_number_dict[go_type]):
            print("term error")
            exit()

        line = f.readline()

    return term_list_dict, pro_list_dict


def deal_results(origin_result_file, deal_result_dir, term_list_file, obo_dict, type):

    f = open(term_list_file, "r")
    text = f.read()
    f.close()

    all_term_list = text.splitlines()
    term_list_dict, pro_list_dict = read_results(origin_result_file)

    for protein_id in pro_list_dict:

        current_dir = deal_result_dir + "/" + protein_id + "/"
        os.makedirs(current_dir)
        result_file = current_dir + "/sprofgo_" + type

        f = open(result_file, "w")
        term_list = term_list_dict[type]
        pro_list = pro_list_dict[protein_id][type]

        for i in range(len(term_list)):
            if(term_list[i].strip() in all_term_list and float(pro_list[i])>=0.01):
                f.write(term_list[i] + " " + type[1] + " " + pro_list[i] + "\n")
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
            origin_result_file = workdir + "/" + data_type + "_result.txt"
            deal_result_dir = workdir + "/benchmark/" + type + "/" + data_type + "/"
            os.system("rm -rf " + deal_result_dir)
            term_list_file = workdir + "/" + type + "_term_list"
            deal_results(origin_result_file, deal_result_dir, term_list_file, obo_dict, type)
