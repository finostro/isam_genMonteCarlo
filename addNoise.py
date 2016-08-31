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
import progressbar


# ============= Parsing Args ========================
parser = argparse.ArgumentParser(description='This script will read an isam ground truth file and create realizations by adding the noise described in the same file.')
parser.add_argument('gtFilename',
                    help='The Ground Truth dataset, in isam format')

parser.add_argument('datasetFolder', metavar='folder',
                    help='The folder to where to create realizations')

parser.add_argument('-n','--num', help='Number of realization files to create', type=int, default=1)

args = parser.parse_args()



if os.path.exists(args.gtFilename):
    print('Opening ' + args.gtFilename)
else:
    print(args.gtFilename + ' does not exist')
    sys.exit(0);

if not os.path.isdir(args.datasetFolder):
    print(args.datasetFolder+ '  is not a folder!')
    sys.exit(0);

# edges
gtedges = np.genfromtxt(args.gtFilename, comments='LANDMARK')

#landmarks
gtlandmarks = np.genfromtxt(args.gtFilename, comments='EDGE2')


bar = progressbar.ProgressBar()

for i in bar(range(args.num)):
    filename, extention = os.path.splitext(os.path.basename(args.gtFilename))
    if filename.endswith('_groundtruth'):
      filename = filename[:-12]
    outFilePath = os.path.join(args.datasetFolder, filename+'_' +str(i)+extention )
    text_file = open(outFilePath, "w")

    time=0;
    iedge=0;
    ilandmark=0;
    while (ilandmark < gtlandmarks.shape[0] and time <= int(gtlandmarks[ilandmark,1])) or (iedge < gtedges.shape[0] and time <=  int(gtedges[iedge,1])):


        while ilandmark < gtlandmarks.shape[0] and time == int(gtlandmarks[ilandmark,1]):
            mean = gtlandmarks[ilandmark,3:5]
            info_sqrt = np.matrix([[gtlandmarks[ilandmark,5],gtlandmarks[ilandmark,6]],[0, gtlandmarks[ilandmark,7]]]) #upper triangular
            info = info_sqrt.transpose()*info_sqrt
            covariance = np.linalg.inv(info)
            realization = np.random.multivariate_normal(mean,covariance)
            line = 'LANDMARK '+str(int(gtlandmarks[ilandmark,1])) +' '+str(int(gtlandmarks[ilandmark,2]))+' '+str(realization[0])+' '+str(realization[1])+' '+ str(gtlandmarks[ilandmark,5])+' '+ str(gtlandmarks[ilandmark,6])+' '+ str(gtlandmarks[ilandmark,7])+'\n'
            text_file.write(line)
            ilandmark += 1
        while iedge < gtedges.shape[0] and time == int(gtedges[iedge,1]):
            mean = gtedges[iedge, 3:6]
            info_sqrt = np.matrix([[gtedges[iedge,6],gtedges[iedge,7],gtedges[iedge,8]],[0, gtedges[iedge,9],gtedges[iedge,10]],[0,0,gtedges[iedge,11]]])#upper triangular
            info = info_sqrt.transpose()*info_sqrt
            covariance = np.linalg.inv(info)
            realization = np.random.multivariate_normal(mean,covariance)
            text_file.write('EDGE2 '+str(int(gtedges[iedge,1]))+' '+str(int(gtedges[iedge,2]))+' '+str(realization[0])+' '+str(realization[1])+' '+str(realization[2])+' '+ str(gtedges[iedge,6])+' '+ str(gtedges[iedge,7]) +' ' + str(gtedges[iedge,8])+' '+ str(gtedges[iedge,9])+' '+ str(gtedges[iedge,10])+' '+ str(gtedges[iedge,11])+'\n')
            iedge += 1
        time += 1
