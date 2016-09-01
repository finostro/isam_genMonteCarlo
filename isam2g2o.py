#!/usr/bin/python3
#
# This script will plot the distribution of the noise in the cityTrees10000 dataset and try to extract its paremeters.
# License: GPLv3
# author: Felipe Inostroza 2016

import sys
import os.path
import numpy as np
import argparse
import progressbar

parser = argparse.ArgumentParser(description='Convert a folder from isam style datasets to g2o style.')


parser.add_argument('datasetFolder', metavar='folder',
                    help='The folder to read datasets')

parser.add_argument('resultsFolder', metavar='results',
                    help='The folder to store converted datasets')
parser.add_argument('-n','--numposes',type=int, default=-1,
                    help='The maximum number of trayectory poses to read (truncate dataset)')
args = parser.parse_args()
if not os.path.isdir(args.datasetFolder):
    print(args.datasetFolder+ '  is not a folder!')
    sys.exit(0);
if not os.path.isdir(args.resultsFolder):
    print(args.resultsFolder+ '  is not a folder!')
    sys.exit(0);

files = os.listdir(args.datasetFolder)
bar = progressbar.ProgressBar()

for f in bar(files):
    infile = os.path.join(args.datasetFolder,f)
    filename, extention = os.path.splitext(os.path.basename(infile))
    outfile =  os.path.join(args.resultsFolder, filename +'.g2o');

    isamFile = open(infile, "r")

    g2oFile = open(outfile , "w")

    for line in isamFile:
      if line.startswith('EDGE2'):
         g2oline  = 'EDGE_SE2' + line[5:]
      if line.startswith('LANDMARK'):
         data = np.fromstring(line[8:] , sep=' ');

         if int(args.numposes) >0 and int(data[0]) > int(args.numposes):
            break
         data[1] = data[1] +100000
         g2oline  =  'EDGE_SE2_XY'
         g2oline = g2oline + ' ' + str( int(data[0]) ) + ' ' + str(int(data[1]))
         for s in data[2:]:
           g2oline = g2oline + ' ' +str(s)
         g2oline = g2oline + '\n'

      g2oFile.write(g2oline)
    g2oFile.write('FIX 0\n')
    isamFile.close()
    g2oFile.close()
