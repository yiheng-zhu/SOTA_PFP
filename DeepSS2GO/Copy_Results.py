import sys
import os


def read_go(gofile):  # read GO Terms

    f = open(gofile, "rU")
    text = f.read()
    f.close()

    name_list = []

    for line in text.splitlines():
        line = line.strip()
        values = line.split()
        name_list.append(values[0])

    return name_list

def copy_results(origindir, copydir):

    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]

    for type in type_list:
        for data_type in data_type_list:
            label_file = copydir + "/" + type + "/" + data_type + "_gene_label"
            name_list = read_go(label_file)
            for name in name_list:
                originfile = origindir + "/" + type + "/" + data_type + "/" + name + "/deepssgo_" + type + "_new"
                currentdir = copydir + "/" + type + "/" + data_type + "/" + name + "/"
                if(os.path.exists(currentdir)==False):
                    os.makedirs(currentdir)
                os.system("cp " + originfile + " " + currentdir)

if __name__ == '__main__':

    copy_results(sys.argv[1], sys.argv[2])