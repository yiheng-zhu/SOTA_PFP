import sys
import os
import numpy as np
from module import obo2csv
obo_url="/data/yihengzhu/GOA/go-basic.obo"
excludeGO = "GO:0003674,GO:0008150,GO:0005575"

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
        return []
    else:
        if(obo_dict.is_a(GOterm, direct=False, name=False, number=False)==""):
            return []
        parent_term_list = obo_dict.is_a(GOterm, direct=False, name=False, number=False).split()
        parent_list = list(set(parent_term_list)-set(excludeGO.split(",")))

        return parent_list

def read_term_list(term_file):

    f = open(term_file, "r")
    text = f.read()
    f.close()

    return text.splitlines()

def create(term_file, label_matrix_file):

    obo_dict = get_obo_dict()
    term_list = read_term_list(term_file)
    number = len(term_list)

    label_matrix = np.zeros([number, number])
    for i in range(len(term_list)):
        term = term_list[i]
        parent_list = find_parents(obo_dict, term)
        for parent in parent_list:
            label_matrix[i][term_list.index(parent)] = 1

    np.save(label_matrix_file, label_matrix)


def sparse(originfile, dealfile):

    label_matrix = np.load(originfile)
    m, n = label_matrix.shape
    sparse_matrix = []
    max_len = 0
    for i in range(len(label_matrix)):
        a = []
        #print(i, len(label_matrix))
        for j in range(len(label_matrix)):
            if label_matrix[i][j] == 1:
                a.append(j)

        sparse_matrix.append(a)
        if max_len < (len(a)):
            max_len = len(a)

    print("max_len:", max_len)

    for i in range(len(sparse_matrix)):
        for j in range(len(sparse_matrix[i]), max_len):
            sparse_matrix[i].append(m)
    # print (sparse_matrix[i])
    print(np.array(sparse_matrix).shape)
    print(len(sparse_matrix[0]))

    np.save(dealfile, np.array(sparse_matrix))


if __name__=='__main__':

    workdir = sys.argv[1]
    type_list = ["MF", "BP", "CC"]

    for type in type_list:

        term_file = workdir + "/" + type + "/term_list"
        label_matrix_file = workdir + "/" + type + "/label_matrix"
        sparse_matrix_file = workdir + "/" + type + "/sparse_label_matrix"
        create(term_file, label_matrix_file)
        sparse(label_matrix_file+".npy", sparse_matrix_file)
