import sys
import pandas as pd
import torch

interpro_dir = "/data/yihengzhu/toolbars/sequence_homology_tools/InterPro/temps/entry_name/"
esm2_dir = "/data/yihengzhu/GOA/resource/esm2_features/"

def read_name_list(name_list_file):

    f = open(name_list_file, "r")
    text = f.read()
    f.close()

    return text.splitlines()

def read_go(gofile):  # read GO Terms

    f = open(gofile, "rU")
    text = f.read()
    f.close()

    go_dict = dict()

    for line in text.splitlines():
        line = line.strip()
        values = line.split()
        go_dict[values[0]] = values[1].split(",")

    return go_dict

def create_label_array(name_list, label_file):

    label_dict = read_go(label_file)
    prop_annotations = []

    for name in name_list:
        prop_annotations.append(label_dict[name])

    return prop_annotations

def create_interpro_array(name_list):

    interpros = []

    for name in name_list:

        interpro_file = interpro_dir + "/" + name

        f = open(interpro_file, "r")
        text = f.read()
        f.close()

        interpros.append(text.splitlines())

    return interpros

def read_sequence(sequence_file):

    f = open(sequence_file, "r")
    text = f.read()
    f.close()

    sequences = []
    for line in text.splitlines():
        line = line.strip()
        if(line.startswith(">")==False):
            sequences.append(line)

    return sequences


def create_esm2_array(name_list):

    data = []

    for name in name_list:

        esm2_file = esm2_dir + "/" + name + ".pt"
        data.append(torch.load(esm2_file)["mean_representations"][36].numpy())
    #data = torch.stack(data).reshape(-1, 2560)

    return list(data)

def create_dataset(sequence_file, name_list_file, label_file, data_file):

    sequences = read_sequence(sequence_file)

    name_list = read_name_list(name_list_file)

    prop_annotations = create_label_array(name_list, label_file)
    interpros = create_interpro_array(name_list)
    esm2_data = create_esm2_array(name_list)

    print(len(prop_annotations))
    print(len(interpros))
    print(len(esm2_data))

    df = pd.DataFrame({

        'sequences': sequences,
        'prop_annotations': prop_annotations,
        'interpros': interpros,
        'esm2':esm2_data
    })
    df.to_pickle(data_file)


if __name__ == '__main__':

    workdir = sys.argv[1]

    type_list = ["mf", "bp", "cc"]
    data_type_list = ["train", "valid", "test"]

    for type in type_list:
        for data_type in data_type_list:
            sequence_file = workdir + "/" + type + "/" + data_type + "_sequence.fasta"
            name_list_file = workdir + "/" + type + "/" + data_type + "_gene_list"
            label_file = workdir + "/" + type + "/" + data_type + "_gene_label"
            data_file = workdir + "/" + type + "/" + data_type + "_data.pkl"
            create_dataset(sequence_file, name_list_file, label_file, data_file)


