import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()
import numpy as np
import train
import sys
import pickle
import argparse

sys.path.insert(0, 'Utils/')
import hparam
import amino_acid
import metric
import os
from decimal import Decimal
os.environ["CUDA_VISIBLE_DEVICES"] = ""

seq_cut_off = 1024


def main():

    parser = argparse.ArgumentParser(description='Arguments for predict.py')
    parser.add_argument('--trained_model', default=None, type=str)
    parser.add_argument('--on', default=None, type=str)
    parser.add_argument('--fasta', default=None, type=str)
    parser.add_argument('--out', default='./output1', type=str)
    parser.add_argument('--data', default='../data/ours/', type=str)
    parser.add_argument('--result_file', default=None, type=str)

    args = parser.parse_args()

    if args.fasta == None:
        raise ValueError("Must provide the input fasta sequences.")


    args.trained_model = [args.trained_model]

    seq = {}
    s = ''
    k = ''
    with open(args.fasta, "r") as f:
        for lines in f:
            if lines[0] == ">":

                if s != '':

                    if(len(s)>seq_cut_off):
                        s = s[0:seq_cut_off]
                    seq[k] = s
                    s = ''
                k = lines[1:].strip('\n')
            else:
                s += lines.strip('\n')

    if (len(s) > seq_cut_off):
        s = s[0:seq_cut_off]

    seq[k] = s
    
    preds_tale_list = []
    for model in args.trained_model:
        preds_tale_list.append(predict_trainedmodel(model, seq, args.data))
    preds_tale = (np.array(preds_tale_list)).mean(axis=0)
    print((np.array(preds_tale_list)).shape, preds_tale.shape)

    preds_score = np.array(preds_tale)


    f = open(args.data + "/term_list", "r")
    text = f.read()
    f.close()
    term_list = text.splitlines()

    i = 0
    f = open(args.result_file, "w")

    for s in seq:

        for j in range(len(preds_score[i])):
            term = "('" + term_list[j] + "', XXXX)"
            score = str(Decimal(float(preds_score[i][j])).quantize(Decimal("0.000")))

            if (float(preds_score[i][j]) > 0.01):
                f.write(s + " " + term + " " + score + "\n")

        i = i + 1
    f.flush()
    f.close()



def predict_trainedmodel(model_path, seq_model, data_path, batch_size=None):
    # predict GO terms through trained deep learning  model
    # argvs: model_path: the path to the trained model
    #	 seq_model: a dic stores the input sequences
    # output:  a probability matrix with shape (len(seq_model), # GO_terms].

    tf.keras.backend.clear_session()
    if model_path == None:
        raise ValueError("Must specify a model to evaluate.")

    with open(model_path + ".hparam", "rb") as f:
        hparams = pickle.load(f)
    hparams['data_path'] = data_path

    if batch_size != None:
        hparams['batch_size'] = batch_size
    test_x = []
    for i in seq_model:
        test_x.append(amino_acid.to_int(seq_model[i], hparams))
    print("predicting #seq:", len(test_x))

    print("start evaluating model: " + model_path)

    def sparse_to_dense(y, length):
        out = np.zeros((len(y), length), dtype=np.int32)
        for i in range(len(y)):
            # print (y[i])
            for j in y[i]:
                out[i][j] = 1

        return out

    hparams['train'] = False
    hparams['batch_size'] = 1

    model1 = train.HMC_models(hparams)
    with tf.device('/cpu:0'):
        holder_list = model1.Main_model()  # ------------holder_list: [model_input, model_output, loss]
    # optimizer = tf.train.AdamOptimizer(learning_rate=hparams['lr'])
    # train_op = optimizer.minimize(holder_list[2])
    # init_op = tf.global_variables_initializer()

    val_list = [v for v in tf.global_variables()]
    saver = tf.train.Saver(val_list)
    batch_size = hparams['batch_size']
    with tf.Session() as sess:
        saver.restore(sess, model_path)

        pred_scores = []
        iterations = int(len(test_x))
        for ite in range(iterations):
            x = test_x[ite * batch_size: (ite + 1) * batch_size]

            pred_score = sess.run(holder_list[3], {holder_list[0]: x})
            print(np.array(pred_score).shape)
            pred_scores.extend(pred_score)
            print(f'iterations: {ite}/{iterations}')

    #  evaluate  the rest test samples after batch evaluation

    return np.array(pred_scores)


if __name__ == '__main__':
    main()
