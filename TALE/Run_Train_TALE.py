import os

for i in range(1, 6):
    cmd = "python train.py --data_path ../data/benchmark/MF/ --save_path ../data/benchmark/MF/models/model" + str(i) + " --batch_size 32"
    os.system(cmd)

