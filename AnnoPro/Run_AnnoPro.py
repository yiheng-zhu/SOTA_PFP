import sys
import os


def run_annopro(workdir):

    name_list = os.listdir(workdir)
    for name in name_list:

        output_dir = workdir + "/" + name + "/output/"
        if(os.path.exists(output_dir)):
            continue
        cmd = "annopro -i " + workdir + "/" + name + "/seq.fasta -o " + workdir + "/" + name + "/output/"
        os.system(cmd)

run_annopro(sys.argv[1])