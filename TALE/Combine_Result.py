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

def combine_result(result_dir1, result_dir2, result_dir3, w, obo_dict):

    type_list = ["MF"]
    data_type_list = ["evaluate", "test"]
    for type in type_list:
        for data_type in data_type_list:

            name_list = os.listdir(result_dir1 + "/" + type + "/" + data_type + "/")

            for name in name_list:

                if (os.path.exists(result_dir3 + "/" + type + "/" + data_type + "/" + name) == True):
                    os.system("rm -rf " + result_dir3 + "/" + type + "/" + data_type + "/" + name)
                os.makedirs(result_dir3 + "/" + type + "/" + data_type + "/" + name)

                result_file1 = result_dir1 + "/" + type + "/" + data_type + "/" + name + "/DIOMAND_" + type
                result_file2 = result_dir2 + "/" + type + "/" + data_type + "/" + name + "/tale_" + type
                result_file3 = result_dir3 + "/" + type + "/" + data_type + "/" + name + "/tale_plus_" + type
                combine_result_single(result_file1, result_file2, result_file3, type, w, obo_dict)

    os.system("python /data/yihengzhu/GOA/resource/benchmark/pythonfile/Evaluate_All_Pipelines.py " + result_dir3)

if __name__ == '__main__':

    for w in range(1, 100):

        print(w)

        workdir = sys.argv[1]

        result_dir1 = workdir + "/diamond/"
        result_dir2 = workdir + "/tale/dataset/"
        result_dir3 = workdir + "/tale_plus/"
        obo_dict = fp.get_obo_dict()

        combine_result(result_dir1, result_dir2, result_dir3, w/100.0, obo_dict)






