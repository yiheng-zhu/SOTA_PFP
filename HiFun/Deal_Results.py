import sys
import os
import Find_Parents as fp



def deal_results(origin_result_file, deal_result_dir, term_list_file, obo_dict, type):

    f = open(term_list_file, "r")
    text = f.read()
    f.close()
    all_term_list = text.splitlines()

    f = open(origin_result_file, "r")
    text = f.read()
    f.close()


    line_set = text.splitlines()
    term_list = line_set[0].split(",")
    term_list = term_list[1:]

    for i in range(1, len(line_set)):

        line = line_set[i]
        values = line.strip().split(",")
        protein_id = values[0]

        current_dir = deal_result_dir + "/" + protein_id + "/"
        os.makedirs(current_dir)
        result_file = current_dir + "/hifun_" + type

        f = open(result_file, "w")

        pro_list = values[1:]
        if(len(pro_list)!=len(term_list)):
            print("error!")
            exit()

        for j in range(len(term_list)):
            if(term_list[j] in all_term_list and float(pro_list[j])>=0.01):
                f.write(term_list[j] + " " + type[1] + " " + pro_list[j] + "\n")
        f.close()

        fp.find_parents_from_file(result_file, result_file + "_new", obo_dict)
        fp.sort_result(result_file)
        fp.sort_result(result_file + "_new")

    f.close()





if __name__ == '__main__':

    workdir = sys.argv[1]
    obo_dict = fp.get_obo_dict()
    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]

    for type in type_list:
        for data_type in data_type_list:
            origin_result_file = workdir + "/" + data_type + "_result"
            deal_result_dir = workdir + "/benchmark/" + type + "/" + data_type + "/"
            os.system("rm -rf " + deal_result_dir)
            term_list_file = workdir + "/" + type + "_term_list"
            deal_results(origin_result_file, deal_result_dir, term_list_file, obo_dict, type)








