#!/bin/bash

# Set up ROOT path for python plotting scripts
# Should be a valid ROOT version with PyROOT setup
export ROOTLIB='/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/root/6.04.14-x86_64-slc6-gcc49-opt/lib/'

# Path for Python Modules
# This is set automatically
export PATH_OnePlot_MODULE1=`pwd`
export PATH_OnePlot_MODULE2=$PATH_OnePlot_MODULE1"/modules/"

# Path for atlas plotting style
export PATH_AtlasStyle=`pwd`"/atlas-style/"

# enable the use of root-numpy
export LCGENV_PATH=/cvmfs/sft.cern.ch/lcg/releases
/cvmfs/sft.cern.ch/lcg/releases/lcgenv/latest/lcgenv -p LCG_85swan2 --ignore Grid x86_64-slc6-gcc49-opt root_numpy > lcgenv.sh
echo 'export PATH=$HOME/.local/bin:$PATH' >> lcgenv.sh
source lcgenv.sh
