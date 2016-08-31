#!/usr/bin/python3
#
# This script will plot the distribution of the noise in the cityTrees10000 dataset and try to extract its paremeters.
# License: GPLv3
# author: Felipe Inostroza 2016




import argparse
import progressbar
import os
import os.path
from subprocess import call

parser = argparse.ArgumentParser(description='This script will run standard isam on all the files on a folder and store the results on a separate folder.')


parser.add_argument('datasetFolder', metavar='folder',
                    help='The folder to read datasets')

parser.add_argument('resultsFolder', metavar='results',
                    help='The folder to store results')



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
    outfile =  os.path.join(args.resultsFolder, filename +'_isamresult'+extention);
    FNULL = open(os.devnull, 'w')
    call(["isam", infile, '-W', outfile], stdout=FNULL)
