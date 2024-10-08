import pandas as pd
import sys

def create_term(originfile, dealfile):

    f = open(originfile, "r")
    text = f.read()
    f.close()

    term_list = text.splitlines()

    df = pd.DataFrame({
        'gos': term_list
    })

    df.to_pickle(dealfile)

if __name__ == '__main__':

    workdir = sys.argv[1]
    type_list = ["mf", "bp", "cc"]

    for type in type_list:
        originfile = workdir + "/" + type + "/term_list"
        dealfile = workdir + "/" + type + "/terms.pkl"
        create_term(originfile, dealfile)

