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
from time import gmtime, strftime

g2oIterations = 100
xi = 0
infoOdomPos = 50
infoOdomAng = 100
infoPointSen = 10
dataSkip = 1
interOpt = 100
dataSize = 1000000
disTest = 2.0
kernelWidth = 3
poseSkip = 1


parser = argparse.ArgumentParser(description='This script will run standard g2o on all the files on a folder and store the results on a separate folder.')


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
    anonfile= os.path.join(args.datasetFolder, filename +'_anon'+extention);
    outfile =  os.path.join(args.resultsFolder, filename +'_g2oNNDAresult'+extention);
    guessfile = os.path.join(args.resultsFolder, filename +'_guess'+extention);
    plotfile = os.path.join(args.resultsFolder, filename +'_plot');
    FNULL = open(os.devnull, 'w')
    call(["g2o_anonymize_observations","-o", filename+"anon.g2o", infile ])
    call(["awk", "{if ($1 == \"EDGE_SE2_XY\") sub(\" -1 \", \" \" 100000+i++ \" \" );print}",filename+"anon.g2o"],stdout=open(anonfile,"w"))
    call(['rm', filename+'anon.g2o'])


    # get initial guess
    call(["g2o", "-i", "0", "-guessOdometry",
                     "-o", guessfile, anonfile])

    buildPath = "/home/finostro/Code/GraphSLAM/src/graphSLAM/build/"


    # optimize

    call(["env", "CPUPROFILE=./my_slam_prof.prof",
                    buildPath+"./my_slam",
                     "-i", str(g2oIterations),
                     "-t", str(xi),
                     "-robustKernel", "Huber",
                     "-robustKernelWidth", str(kernelWidth),
                     "-poseSkip", str(poseSkip),
                     "-interOpt", str(interOpt),
                     "-disTest", str(disTest),
                     "-o", outfile, guessfile])
