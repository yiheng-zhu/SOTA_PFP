import pandas as pd
import sys

def create_interpro(originfile, dealfile):

    f = open(originfile, "r")
    text = f.read()
    f.close()

    line_set = text.splitlines()
    line_set = line_set[1:]

    interpro_list = []

    for line in line_set:
        values = line.strip().split()
        interpro_list.append(values[0])

    df = pd.DataFrame({
        'interpros': interpro_list
    })

    df.to_pickle(dealfile)

if __name__ == '__main__':

    workdir = sys.argv[1]
    type_list = ["mf", "bp", "cc"]

    for type in type_list:
        originfile = "/data/yihengzhu/toolbars/sequence_homology_tools/InterPro/interproscan-5.69-101.0/entry.list"
        dealfile = workdir + "/" + type + "/interpros.pkl"
        create_interpro(originfile, dealfile)
