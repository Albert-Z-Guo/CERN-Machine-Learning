#!/usr/bin/python2.6

# / / /
# \ \ \
# / / /
# Y.Wu <wyusheng@umich.edu>

######################################################
# Python module to define some external plotting style 
######################################################

########################
# Libraries and Includes
########################

# Python System Modules
import os,sys,glob
import logging

# Python Paths
ROOTLIB, PATH_OnePlot_MODULE1, PATH_OnePlot_MODULE2 = "", "", ""

if os.getenv("ROOTLIB"): ROOTLIB=os.getenv("ROOTLIB")
if os.getenv("PATH_OnePlot_MODULE1"): PATH_OnePlot_MODULE1=os.getenv("PATH_OnePlot_MODULE1")
if os.getenv("PATH_OnePlot_MODULE2"): PATH_OnePlot_MODULE2=os.getenv("PATH_OnePlot_MODULE2")

sys.path.append(ROOTLIB)
sys.path.append(PATH_OnePlot_MODULE1)
sys.path.append(PATH_OnePlot_MODULE2)

# Python Math Modules
import array
from math import sqrt,fabs,sin,pow

# ROOT Modules
from ROOT import TFile,TTree,TChain,TBranch,TH1F,TH2F
from ROOT import TCanvas,TPad
from ROOT import TLorentzVector
from ROOT import gROOT, gDirectory,gStyle
from ROOT import TPaveText, TLegend
import ROOT


#########################
# The list of functions #
#########################

"""
atlas_style(): simple function to setup atlas plotting style
"""

########################
# Function atlas_style()
########################
# Will read environmental variables for the path of Style package
# otherwise use a dummy path

def atlas_style():
    # Set Atlas Style
    if os.getenv("PATH_AtlasStyle"): PATH_AtlasStyle=os.getenv("PATH_AtlasStyle")
    else: PATH_AtlasStyle="/atlas/data18a/wyusheng/atlas/analysis/tools/AtlasPlotStyle/atlasstyle-00-03-05/"
    gROOT.SetMacroPath(PATH_AtlasStyle)
    gROOT.LoadMacro("AtlasStyle.C+")
    gROOT.ProcessLine("SetAtlasStyle()")


    
    
    
    
    
    