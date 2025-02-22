import sys
import os
import threading

def download_single(workdir, name_list, output_dir):

    for name in name_list:
        cmd = workdir + "/apps/retrieve_FunFam_aln_GO_EC_anno_CATH-API.pl " + name + " v4_2_0 " + output_dir
        os.system(cmd)


def download_multi_thread(workdir, data_type, thread_number): # download protein sequences with information using UniProt ID from a protein list file

    family_file = workdir + "/" + data_type + "_results/" + data_type + "_sequence.family"
    output_dir = workdir + "/" + data_type + "_family/"
    if(os.path.exists(output_dir)==False):
        os.makedirs(output_dir)

    name_list_array = split_name_list(family_file, thread_number)
    threads = []

    for name_list in name_list_array:

        thread = threading.Thread(target=download_single, args=(workdir, name_list, output_dir, ))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def split_name_list(name_list_file, num_sublists):

    f = open(name_list_file, "r")
    text = f.read()
    f.close()

    name_list = text.splitlines()

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



download_multi_thread(sys.argv[1], sys.argv[2], int(sys.argv[3]))