import pickle
import sys


def extract(data_file, sequence_file):

    pic = open(data_file, "rb")
    data = pickle.load(pic)

    f = open(sequence_file, "w")

    for i in range(len(data)):
        if (data[i]["mode"]) == "test":
            f.write(">" + str(i) + "\n")
            f.write(data[i]["seq"] + "\n")
    f.flush()
    f.close()

if __name__=='__main__':

    workdir = sys.argv[1]
    type_list = ["mf", "bp", "cc"]

    for type in type_list:

        data_file = workdir + "/test_seq_" + type
        sequence_file = workdir + "/test_seq_" + type + ".fasta"
        extract(data_file, sequence_file)



