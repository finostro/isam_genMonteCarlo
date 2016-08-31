#!/usr/bin/python3
#
# This script will plot the distribution of the noise in the cityTrees10000 dataset and try to extract its paremeters.
# License: GPLv3
# author: Felipe Inostroza 2016



import sys
import os.path
import numpy as np

import matplotlib
matplotlib.use("TkAgg");

import matplotlib.pyplot as plt
import argparse



# ============= Parsing Args ========================
parser = argparse.ArgumentParser(description='This script will plot the distribution of the noise in the cityTrees10000 dataset and try to extract its paremeters.')
parser.add_argument('gtFilename',
                    help='The Ground Truth cityTrees10000 dataset')

parser.add_argument('datasetFilename', metavar='filename',
                    help='The cityTrees10000 dataset')

parser.add_argument('-p','--plot', help='plot stuff', action='store_true')

args = parser.parse_args()



# ================ Read Files ==================



if os.path.exists(args.gtFilename):
    print('Opening ' + args.gtFilename);
else:
    print(args.gtFilename + ' does not exist')
    sys.exit(0);

if os.path.exists(args.datasetFilename):
    print('Opening ' + args.datasetFilename);
else:
    print(args.datasetFilename + ' does not exist')
    sys.exit(0);


# edges
gtedges = np.genfromtxt(args.gtFilename, comments='LANDMARK')
edges = np.genfromtxt(args.datasetFilename, comments='LANDMARK')

#landmarks
gtlandmarks = np.genfromtxt(args.gtFilename, comments='EDGE2')
landmarks = np.genfromtxt(args.datasetFilename, comments='EDGE2')


landmarkError= landmarks - gtlandmarks
if args.plot :

    plt.plot(landmarkError[:,3],landmarkError[:,4], 'b.')
    plt.show()

print 'landmark cov'
print np.cov(landmarkError[:,3:5],rowvar=False)

#edges
edgesError =edges - gtedges

if args.plot :

    plt.plot(edgesError[:,3],edgesError[:,4], 'b.')
    plt.show()

print 'edges cov'
print np.cov(edgesError[:,3:6], rowvar=False)
