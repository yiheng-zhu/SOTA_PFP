import sys
import os
obo_url="/data/yihengzhu/GOA/go-basic.obo"
excludeGO = "GO:0003674,GO:0008150,GO:0005575"
from module import obo2csv

def read_term_list(term_file):

    f = open(term_file, "r")
    text = f.read()
    f.close()

    return text.splitlines()

def get_obo_dict():  # read obo_dict

    fp = open(obo_url, 'rU')
    obo_txt = fp.read()
    fp.close()
    obo_dict = obo2csv.parse_obo_txt(obo_txt)
    return obo_dict


def get_obsolete(obo_dict): # get obsolete terms

    return obo_dict.obsolete()

def find_parents(obo_dict, GOterm): # find parents

    obsolete_list=get_obsolete(obo_dict)

    if(GOterm in obsolete_list):
        return GOterm
    else:
        if(obo_dict.is_a(GOterm, direct=True, name=False, number=False)==""):
            return GOterm
        parent_term_list = obo_dict.is_a(GOterm, direct=True, name=False, number=False).split()
        parent_term_list = list(set(parent_term_list)-set(excludeGO.split(",")))
        parent_term_list.remove(GOterm)

        return parent_term_list


def create_parent_index(term_file, index_file):

    term_list = read_term_list(term_file)
    obo_dict = get_obo_dict()

    f = open(index_file, "w")

    for term in term_list:

        parent_term_list = find_parents(obo_dict, term)

        for parent in parent_term_list:
            index1 = term_list.index(term)
            index2 = term_list.index(parent)

            if (index1 == -1 or index2 == -1):
                print(term)

            f.write(str(index1) + " " + str(index2) + "\n")
            break




    f.flush()
    f.close()

if __name__=='__main__':

    workdir = sys.argv[1]
    type_list = ["MF", "BP", "CC"]

    for type in type_list:

        term_file = workdir + "/" + type + "/term_list"
        index_file = workdir + "/" + type + "/parent_index"
        create_parent_index(term_file, index_file)
