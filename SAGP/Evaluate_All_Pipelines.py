import sys
import Evaluation as ev
import Get_Meatures_From_T as gf
import os


def evaluate(labelfile, result_dir, rocfile, type, pipeline):

    e = ev.evaluation(labelfile, result_dir, pipeline + "_" + type + "_new", rocfile)
    e.process()
    train_aupr = e.get_aupr()

    measures_list = gf.get_measures_files(rocfile, rocfile)
    line = ""
    for measures in measures_list:
        line = line + measures + " "
    line = line + "AUPR=" + str(train_aupr) + " "

    print(pipeline + ":  " + line)

if __name__=="__main__":



    workdir = sys.argv[1]
    type_list = ["MF", "BP", "CC"]
    pipeline_list = ["protein_Result"]

    for type in type_list:

        print(type+":")

        for pipeline in pipeline_list:

            dir = workdir + "/" + type + "/"

            result_dir = dir + "/evaluate/"
            label_file = dir + "/evaluate_gene_label"
            rocfile = dir + "/evaluate_roc"

            evaluate(label_file, result_dir, rocfile, type, pipeline)

            result_dir = dir + "/test/"
            label_file = dir + "/test_gene_label"
            rocfile = dir + "/test_roc"

            evaluate(label_file, result_dir, rocfile, type, pipeline)

        print()



