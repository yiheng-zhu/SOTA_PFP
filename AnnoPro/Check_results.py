import os
import sys


def check_results(workdir):
    name_list = os.listdir(workdir)
    for name in name_list:
        resultfile = workdir + "/" + name + "/output/mf_result.csv"
        if(os.path.exists(resultfile)==False):
            os.system("rm -rf " + workdir + "/" + name + "/output/")
            f = open(workdir + "/" + name + "/seq.fasta", "r")
            line = f.readline()
            line = f.readline().strip()
            f.close()

            new_line = ""
            while(len(new_line)<50):
                new_line = new_line + line

            f = open(workdir + "/" + name + "/seq.fasta", "w")
            f.write(">" + name + "\n" + new_line + "\n")
            f.close()

            print(name)

def read_sequence(sequence_file):  # read sequence

    sequence_dict = dict()

    f = open(sequence_file, "r")
    text = f.read()
    f.close()

    for line in text.splitlines():
        if (line.startswith(">")):
            name = line
        else:
            sequence_dict[name[1:]] = line

    return sequence_dict

def remove_results(sequence_file, workdir):

    sequence_dict = read_sequence(sequence_file)
    name_list = os.listdir(workdir)
    for name in name_list:
        f = open(workdir + "/" + name + "/seq.fasta", "r")
        f.readline()
        sequence = f.readline().strip()
        f.close()
        if(sequence!=sequence_dict[name]):
            print(name)
            os.system("rm -rf " + workdir + "/" + name + "/output/")
            f = open(workdir + "/" + name + "/seq.fasta", "w")
            f.write(">" + name + "\n" + sequence_dict[name] + "\n")
            f.close()







if __name__ == '__main__':

    remove_results(sys.argv[1], sys.argv[2])
    check_results(sys.argv[2])


