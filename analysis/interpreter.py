from collections import defaultdict
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import os
import re

class Sample:
    def __init__(self,
                 nparticles,
                 pbest,
                 gbest,
                 time):
        self.nparticles = nparticles
        self.pbest = np.array(pbest)
        self.gbest = np.array(gbest)
        self.time = time

def read_file(file_path):
    data = defaultdict(lambda : list())
    with open(file_path) as file:
        T = float(file.readline())
        N = int(file.readline())
        while True:
            try:
                pbest = [float(file.readline()) for _ in range(N)]
                gbest = file.readline().split()
                data["pbest"].append(float(sum(pbest)/N))
                data["gbest"].append(float(gbest[0]))
            except: break
        if len(data["pbest"]) != len(data["gbest"]):
            raise Exception("READ ERROR: pbest and gbest are not the same length")
        data = Sample(N, data["pbest"], data["gbest"], T)
    return data

def sorted_files(folder):
    files = sorted(os.listdir(folder),
        key = lambda filename : int(re.search(r'\d+', filename).group()))
    return list(files)

def get_data():
    data = []
    for folder in os.listdir('data/output'):
        if folder != "burma14":
            continue
        line = []
        with open(f"data/answer/{folder}") as answer_file:
            line.append(int(answer_file.readline()))
        for filename in sorted_files(f"{'data/output'}/{folder}"):
            line.append(read_file(f"{'data/output'}/{folder}/{filename}"))
        data.append(line)
        break
    return data

data = get_data()
gbest = np.empty((len(data),7))
pbest = np.empty((len(data),7))

for i in range(len(data)):
    for j in range(7):
        total = len(data[i][j+1].pbest)*data[i][0]
        pbest[i][j] = data[i][j+1].pbest.sum() / total
        gbest[i][j] = data[i][j+1].gbest.sum() / total


pbest_mean = [pbest[:,i] for i in range(len(pbest))]
gbest_mean = [gbest[:,i] for i in range(len(gbest))]

print(pbest_mean.shape())

figure = plt.figure()
plt.plot(np.arange(0.5, 2.1, 0.25), pbest_mean)
plt.plot(np.arange(0.5, 2.1, 0.25), gbest_mean)
plt.show()


#gbest = np.array([[sample.gbest for sample in line] for line in samples])
#pbest = np.array([[sample.pbest for sample in line] for line in samples])

#print(gbest)
        
#plt.plot(list(range(len(globals["pbest"]))), 
#         list(zip(globals["pbest"], globals["gbest"])), 
#         label="pbest")