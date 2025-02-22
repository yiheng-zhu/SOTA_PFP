import sys
import os
import Create_Term_Frequence as cf
import Find_Parents as fp

def read_protein_list(protein_list_file):   # read protein list

    f = open(protein_list_file, "r")
    text = f.read()
    f.close()

    return text.splitlines()

def read_map(map_file):  #read map file

    f = open(map_file, "r")
    text = f.read()
    f.close()

    map_dict = dict()

    for line in text.splitlines():

        line = line.strip()
        values = line.split()
        map_dict[values[0]] = values[1:]

    return map_dict

def create_protein_result_one_aspect(result_dict, type, data_type):   # create result_dict for one aspcet

    source_dir = "/data/yihengzhu/GOA/resource/SOTA/FunFams/cath-tools-genomescan-master/"
    map_file = source_dir + "/" + data_type + "_results/" + data_type + "_sequence.map"
    family_dir = source_dir + "/" + data_type + "_family/"

    all_term_list_file = "/data/yihengzhu/GOA/resource/SOTA/FunFams/cath-tools-genomescan-master/workspace/"+ type + "_term_list"

    all_term_list = read_protein_list(all_term_list_file)

    map_dict = read_map(map_file)

    for protein in map_dict:

        family_name_list = map_dict[protein]

        final_number_dict = dict()
        all_number = 0

        for family in family_name_list:

            family = family.split("/")[0] + "." + family.split("/")[2]

            family_go_file = family_dir + "/" + family + ".GO.anno"
            number_dict, number = cf.read_result(family_go_file)

            all_number = all_number + number

            for term in number_dict:
                if(term in all_term_list):

                    if (term not in final_number_dict):
                        final_number_dict[term] = number_dict[term]
                    else:
                        final_number_dict[term] = final_number_dict[term] + number_dict[term]

        for term in final_number_dict:
            final_number_dict[term] = final_number_dict[term]/float(all_number)

        if(protein not in result_dict):
            result_dict[protein] = dict()

        result_dict[protein][type] = []
        for term in final_number_dict:
            result_dict[protein][type].append(term+" "+" "+str(final_number_dict[term]))

    return result_dict


def create_protein_result(data_type):   # read result

    type_list = ["MF", "BP", "CC"]
    result_dict = dict()

    for type in type_list:
        result_dict = create_protein_result_one_aspect(result_dict, type, data_type)

    return result_dict



def create_final_result(workdir, data_type, type, obo_dict): # create results for DeepGO

    name_list_file = workdir + "/" + type + "/" + data_type + "_gene_list"
    name_list = read_protein_list(name_list_file)
    result_dict = create_protein_result(data_type)

    for name in name_list:

        current_dir = workdir + "/" + type + "/" + data_type + "/" + name + "/"
        if(os.path.exists(current_dir)==False):
            os.makedirs(current_dir)

        originfile = current_dir+"/funfam_" + type
        dealfile = current_dir+"/funfam_" + type + "_new"

        f = open(originfile, "w")

        if(name in result_dict and type in result_dict[name]):

            for line in result_dict[name][type]:
                values = line.strip().split()
                f.write(values[0] + " " + type[1] + " " + values[1] + "\n")

        f.flush()
        f.close()

        fp.find_parents_from_file(originfile, dealfile, obo_dict)


if __name__ == '__main__':

    workdir = sys.argv[1]
    type_list = ["MF", "BP", "CC"]
    obo_dict = fp.get_obo_dict()

    for type in type_list:

        create_final_result(workdir, "evaluate", type, obo_dict)
        create_final_result(workdir, "test", type, obo_dict)












