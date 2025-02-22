import sys
import os

def read_result(result_file):   # total teh frequence of go terms in funfam

    f = open(result_file, "r")
    text = f.read()
    f.close()

    line_set = text.splitlines()
    all_number = len(line_set)-1
    number_dict = dict()

    for line in line_set[1:]:

        values = line.strip().split()[1:]
        for value in values:

            term = value[0:len(value)-1]

            if(term not in number_dict):
                number_dict[term] = 1
            else:
                number_dict[term] = number_dict[term] + 1

    return number_dict, all_number