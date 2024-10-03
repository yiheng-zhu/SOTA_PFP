import sys
import os
import Find_Parents as fp

def post_deal(result_file):

    f = open(result_file, "r")
    text = f.read()
    f.close()

    result_dict = dict()
    for line in text.splitlines():
        line = line.strip()
        values = line.split("(")
        name = values[0].strip()
        term = values[1]
        values1 = term.split(")")
        pro = line[len(line)-5: ]

        term = values1[0].split(",")[0].split("'")[1]

        if(name not in result_dict):
            result_dict[name] = []

        result_dict[name].append(term + " " + pro)

    return result_dict

def create_result(result_file, deal_dir, method, type, data_type, obo_dict):

    result_dict = post_deal(result_file)

    for name in result_dict:

        tempdir = deal_dir + "/" + data_type + "/" + name + "/"
        os.system("rm -rf " + tempdir)
        os.makedirs(tempdir)

        result_file = tempdir + "/" + method + "_" + type
        f = open(result_file, "w")
        for line in result_dict[name]:

            values = line.strip().split()
            term = values[0]
            pro = values[1]

            f.write(term +" " + type[1] + " " + pro + "\n")
        f.flush()
        f.close()

        result_file_new = tempdir + "/" + method + "_" + type + "_new"
        fp.find_parents_from_file(result_file, result_file_new, obo_dict)
        fp.sort_result(result_file)
        fp.sort_result(result_file_new)


if __name__ == '__main__':

    workdir = sys.argv[1]
    type_list = ["MF"]
    data_type_list = ["evaluate", "test"]
    method = "tale"

    obo_dict = fp.get_obo_dict()

    for type in type_list:
        for data_type in data_type_list:
            result_file = workdir + "/" + data_type + "_result" + "_" + type.lower()
            deal_dir = workdir + "/benchmark/" + type + "/"
            create_result(result_file, deal_dir, method, type, data_type, obo_dict)





