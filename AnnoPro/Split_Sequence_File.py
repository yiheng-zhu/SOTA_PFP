import sys
import os

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


def split(sequence_file, outputdir): #split

    sequence_dict = read_sequence(sequence_file)

    for name in sequence_dict:
        os.makedirs(outputdir+ "/" + name + "/")
        f = open(outputdir + "/" + name + "/seq.fasta", "w")
        f.write(">" + name + "\n")
        f.write(sequence_dict[name] + "\n")
        f.flush()
        f.close()

if __name__ == '__main__':

    split(sys.argv[1], sys.argv[2])


