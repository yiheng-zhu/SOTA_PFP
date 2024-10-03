import sys
import os

import blast2msa_new as bm
from decimal import Decimal
import Find_Parents as fp
import threading

blast_dir = "/data/yihengzhu/toolbars/sequence_homology_tools/BLAST/ncbi-blast-2.11.0+/bin/"

def split_sequence(sequence_file, sequence_dir):

    f = open(sequence_file, "r")
    text = f.read()
    f.close()

    for line in text.split():
        line = line.strip()
        if (line.startswith(">")):
            name = line[1:]
        else:
            sequence = line
            os.makedirs(sequence_dir + "/" + name + "/")
            f = open(sequence_dir + "/" + name + "/seq.fasta", "w")
            f.write(">" + name + "\n" + sequence + "\n")

def format_database(sequence_file, database_file):

    cmd = blast_dir + "/" + "makeblastdb -in " + sequence_file + " -dbtype prot -parse_seqids -out " + database_file
    os.system(cmd)


def run_blast(workdir, database_file):    # run blast

    seq_file = workdir + "/seq.fasta"

    if(os.path.exists(seq_file)==False or os.path.getsize(seq_file)==0):
        print("seq.fasta is not exist")
        return

    xml_file = workdir + "/blast.xml"

    cmd = blast_dir + "/blastp -query " + seq_file + \
          " -db " + database_file + \
          " -outfmt 5 -evalue 0.1 " \
          " -out " + xml_file

    os.system(cmd)

def extract_msa(workdir): # extract blast

    xml_file = workdir + "/blast.xml"
    seq_file = workdir + "/seq.fasta"
    msa_file = workdir + "/blast.msa"

    if(os.path.exists(xml_file)==False or os.path.getsize(xml_file)==0):
        print("blast.xml is not exist")
        return

    bm.run_extract_msa(seq_file, xml_file, msa_file)

def create_protein_list(workdir, go_dict):

    msa_file = workdir + "/blast.msa"

    template_list = []

    f = open(msa_file, "r")
    text = f.read()
    f.close()

    for line in text.splitlines():
        line = line.strip()
        if(line.startswith(">")):
            template = line.strip().split("\t")[0][1:]
            score = line.strip().split("\t")[1]
            if(template in go_dict):
                template_list.append([template, score])

    f = open(workdir + "/protein_list", "w")
    for template, score in template_list:
        f.write(template + " " + score + "\n")
    f.flush()
    f.close()

def read_protein_list(protein_list_file):    # read protein templates

    f = open(protein_list_file, "r")
    text = f.read()
    f.close()

    protein_list_dict = dict()

    for line in text.splitlines():
        values = line.strip().split()
        protein_list_dict[values[0]] = float(values[1])

    return protein_list_dict



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



def annotate(workdir, type, obo_dict, go_dict):  # annotate GO term

    protein_list_file = workdir+"/protein_list"
    if(os.path.exists(protein_list_file)==False or os.path.getsize(protein_list_file)==0):
        print("protein list is not exist ! ")
        return

    protein_list_dict = read_protein_list(protein_list_file)

    term_list = []
    for protein in protein_list_dict:
        term_list.extend(go_dict[protein])
    term_list = list(set(term_list))

    result_dict = dict()
    for term in term_list:
        sum1 = 0.0
        sum2 = 0.0
        for protein in protein_list_dict:
            sum1 = sum1 + protein_list_dict[protein]
            if(term in go_dict[protein]):
                sum2 = sum2 + protein_list_dict[protein]

        result_dict[term] = sum2/sum1

    result_list = [(result_dict[term], term) for term in result_dict]
    result_list = sorted(result_list, reverse=True)

    resultfile = workdir + "/protein_Result_" + type
    f = open(resultfile, "w")
    for value, term in result_list:
        if(value>=0.01):
            f.write(term+" "+type[1]+" "+str(Decimal(value).quantize(Decimal("0.000"))) + "\n")
    f.flush()
    f.close()

    fp.find_parents_from_file(resultfile, resultfile+"_new", obo_dict)
    fp.sort_result(resultfile)


def split_name_list(name_list, num_sublists):

    sublist_length = len(name_list) // num_sublists
    remainder = len(name_list) % num_sublists

    # Create the sublists
    sublists = []
    start = 0
    for i in range(num_sublists):
        if i < remainder:
            end = start + sublist_length + 1
        else:
            end = start + sublist_length
        sublists.append(name_list[start:end])
        start = end

    return sublists


def run_thread_process(sequence_dir, database_file, go_dict, obo_dict, type, sub_name_list):

    for name in sub_name_list:
        workdir = sequence_dir + "/" + name + "/"
        run_blast(workdir, database_file)
        extract_msa(workdir)
        create_protein_list(workdir, go_dict)
        annotate(workdir, type, obo_dict, go_dict)

def process(dir, obo_dict, thread_number):   # main process

    type_list = ["MF", "BP", "CC"]
    data_type_list = ["evaluate", "test"]

    for type in type_list:

        train_sequence_file = dir + "/" + type + "/train_sequence.fasta"
        database_file = dir + "/" + type + "/train_sequence"
        format_database(train_sequence_file, database_file)

        train_label_file = dir + "/" + type + "/train_gene_label"
        go_dict = read_go(train_label_file)

        for data_type in data_type_list:

            test_sequence_file = dir + "/" + type + "/" + data_type + "_sequence.fasta"
            sequence_dir = dir + "/" + type + "/" + data_type + "/"
            os.system("rm -rf " + sequence_dir)
            split_sequence(test_sequence_file, sequence_dir)

            name_list = os.listdir(sequence_dir)
            name_set = split_name_list(name_list, thread_number)

            threads = []

            for sub_name_list in name_set:
                thread = threading.Thread(target=run_thread_process, args=(sequence_dir, database_file, go_dict, obo_dict, type, sub_name_list,))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()




if __name__ == '__main__':

    dir = sys.argv[1]
    obo_dict = fp.get_obo_dict()
    process(dir, obo_dict, int(sys.argv[2]))









