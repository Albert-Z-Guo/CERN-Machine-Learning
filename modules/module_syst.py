#!/usr/bin/python2.6

# / / /
# \ \ \
# / / /
# Y.Wu <wyusheng@umich.edu>

############################################################
# Python module to calculate systematics based on histograms
############################################################

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
Calculate CT10 PDF uncertainty:  systPDFCT10()
Calculate MSTW PDF uncertainty:  systPDFMSTW()
Calculate NNPDF PDF uncertainty: systPDFNNPDF() 
Calculate Envelope uncertainty:  systEnvelope()
Calculate 1v1 uncertainty:       syst1v1()
Calculate combined uncertainty:  systCombine()

General information:
    - each function will return a list of histograms of nominal, +1sigma and -1sigma.
    - function inputs are usually histograms and some control parameters
    - for the detailed usages and descriptions see each individual functions
"""


########################
# Function systPDFCT10()
########################
# Get PDF uncertainty for CT10
# prescription from Formula 5 of http://arxiv.org/pdf/1007.2241.pdf
# Input: list of histograms from nominal, CT10-1 ... CT10-52 (in total: 53)
# Option: symmetrize: symmetrize errors (True) or not (False)
# Option: ratio: error histograms calculated as fractional (True) or absolute (False)
# Output: a dictionary of {"NOM": histo_nom, "UP": +1sigma, "DN": -1sigma}

def systPDFCT10(list_histo=[], symmetrize=True, ratio=False):

    print("INFO: calculate CT10 PDF error")
    print("INFO: scale the 90% CL to 68% CL by 1.65")
    scale=1.65

    # STEP1: 
    # perform strict check on input histograms
    # 53 histograms, 1st: nominal, 2-53th: CT10 error sets
    if len(list_histo)!=53:
        print("ERROR: expect in total 53 histograms!")
        sys.exit(-1)
    for index in range(53):
        if not list_histo[index]:
            print("ERROR: histogram has a problem: {0}-th".format(index))
            sys.exit(-1)
    nbins=list_histo[0].GetNbinsX()
    for index in range(53):
        this_nbins=list_histo[index].GetNbinsX()
        if this_nbins!=nbins:
            print("ERROR: expect number of bins to be {0}: {1}-th".format(nbins, index))
            sys.exit(-1)
        
    # STEP2:
    # initialize two arrays to store Up/Down errors
    # scan histograms and do the calculations
    sys_up = []
    sys_dn = []
    for num in range(nbins):
        bin = num + 1
        err_up, err_dn = 0., 0.
        # if bin content = 0
        nomcon=list_histo[0].GetBinContent(bin)
        if nomcon==0.:
            sys_up.append(0.)
            sys_dn.append(0.)
            continue
        # loop PDF error sets 52/2=26,
        # for each pair up variation = max(f+ - f0, f- - f0, 0)
        # for each pair down variation = max(f0 - f+, f0 - f-, 0)
        for set in range(26):
            setp = set+1
            setm = set+2
            pcon = list_histo[setp].GetBinContent(bin)
            mcon = list_histo[setm].GetBinContent(bin)
            devp = pcon - nomcon
            devm = mcon - nomcon
            temp_up = max([devp, devm, 0])
            temp_dn = max([-1.*devp, -1.*devm, 0])
            err_up = sqrt(pow(err_up,2) + pow(temp_up,2))
            err_dn = sqrt(pow(err_dn,2) + pow(temp_dn,2))
        # store the up/down error into array
        # provide the fractional uncertainty
        average=(err_up+err_dn)/2.
        if symmetrize: 
            sys_up.append(1.*average/nomcon)
            sys_dn.append(1.*average/nomcon)
        else:
            sys_up.append(1.*err_up/nomcon)
            sys_dn.append(1.*err_dn/nomcon)
    
    # STEP3:
    # make output histograms
    dict={}
    dict["NOM"]=list_histo[0]
    histo_up = list_histo[0].Clone("CT10_UP")
    histo_dn = list_histo[0].Clone("CT10_DN")
    for num in range(nbins):
        bin = num + 1
        nomcon = list_histo[0].GetBinContent(bin)
        if ratio:
            upcon = 1 + sys_up[num]/scale
            dncon = 1 - sys_dn[num]/scale
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
            histo_up.SetBinError(bin, 0.)
            histo_dn.SetBinError(bin, 0.)
        else:
            upcon = nomcon * (1 + sys_up[num]/scale)
            dncon = nomcon * (1 - sys_dn[num]/scale)
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
    dict["UP"]=histo_up
    dict["DN"]=histo_dn
            
    # Return
    return dict
    
    
#########################
# Function systEnvelope()
#########################
# Get the uncertainty as envelope of input histograms
# Input: list of histograms as nominal (0-th), variation-1 (1-th), ..., variation-n (n-th)
# Option: symmetrize: symmetrize errors (True) or not (False)
# Option: ratio: error histograms calculated as fractional (True) or absolute (False)
# Output: a dictionary of {"NOM": histo_nom, "UP": +1sigma, "DN": -1sigma}

def systEnvelope(list_histo=[], symmetrize=True, ratio=False):
    
    print("INFO: calculate uncertainty as envelope of the inputs")

    # STEP1: 
    # perform check on input histograms
    nhisto = len(list_histo)
    if nhisto<2:
        print("ERROR: expect at lease 2 histograms")
        sys.exit(-1)
    for index in range(nhisto):
        if not list_histo[index]:
            print("ERROR: histogram has a problem: {0}-th".format(index))
            sys.exit(-1)
    nbins=list_histo[0].GetNbinsX()
    for index in range(nhisto):
        this_nbins=list_histo[index].GetNbinsX()
        if this_nbins!=nbins:
            print("ERROR: expect number of bins to be {0}: {1}-th".format(nbins, index))
            sys.exit(-1)
        
    # STEP2:
    # initialize two arrays to store Up/Down errors
    # scan histograms and do the calculations
    sys_up = []
    sys_dn = []
    for num in range(nbins):
        bin = num + 1
        err_up, err_dn = 0., 0.
        # if bin content = 0
        nomcon=list_histo[0].GetBinContent(bin)
        if nomcon==0.:
            sys_up.append(0.)
            sys_dn.append(0.)
            continue
        # loop all the sets
        for set in range(nhisto):
            thiscon = list_histo[set].GetBinContent(bin)
            dev = thiscon - nomcon
            err_up = max([dev, err_up])
            err_dn = min([dev, err_dn])
        # store the up/down error into array
        # provide the fractional uncertainty
        average=fabs(err_up-err_dn)/2.
        if symmetrize: 
            sys_up.append(1.*average/nomcon)
            sys_dn.append(1.*average/nomcon)
        else:
            sys_up.append(1.*fabs(err_up)/nomcon)
            sys_dn.append(1.*fabs(err_dn)/nomcon)
    
    # STEP3:
    # make output histograms
    dict={}
    dict["NOM"]=list_histo[0]
    histo_up = list_histo[0].Clone("Envelope_UP")
    histo_dn = list_histo[0].Clone("Envelope_DN")
    for num in range(nbins):
        bin = num + 1
        nomcon = list_histo[0].GetBinContent(bin)
        if ratio:
            upcon = 1 + sys_up[num]
            dncon = 1 - sys_dn[num]
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
            histo_up.SetBinError(bin, 0.)
            histo_dn.SetBinError(bin, 0.)
        else:
            upcon = nomcon * (1 + sys_up[num])
            dncon = nomcon * (1 - sys_dn[num])
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
    dict["UP"]=histo_up
    dict["DN"]=histo_dn
            
    # Return
    return dict
 

####################
# Function syst1v1()
#################### 
# Get the uncertainty as 1v1 comparison of two histograms
# the difference will be quoted as the uncertainty
# Input: list of histograms as nominal (0-th), alternative (1-th)
# Option: ratio: error histograms calculated as fractional (True) or absolute (False)
# Output: a dictionary of {"NOM": histo_nom, "UP": +1sigma, "DN": -1sigma}
 
def syst1v1(list_histo=[], ratio=False):

    print("INFO: calculate uncertainty as 1v1 comparison of the inputs")

    # STEP1: 
    # perform check on input histograms
    nhisto = len(list_histo)
    if nhisto!=2:
        print("ERROR: expect exactly 2 histograms")
        sys.exit(-1)
    for index in range(nhisto):
        if not list_histo[index]:
            print("ERROR: histogram has a problem: {0}-th".format(index))
            sys.exit(-1)
    nbins=list_histo[0].GetNbinsX()
    for index in range(nhisto):
        this_nbins=list_histo[index].GetNbinsX()
        if this_nbins!=nbins:
            print("ERROR: expect number of bins to be {0}: {1}-th".format(nbins, index))
            sys.exit(-1)
        
    # STEP2:
    # initialize two arrays to store Up/Down errors
    # scan histograms and do the calculations
    syst = []
    for num in range(nbins):
        bin = num + 1
        err = 0.
        # if bin content = 0
        nomcon=list_histo[0].GetBinContent(bin)
        if nomcon==0.:
            syst.append(0.)
            continue
        # loop all the sets
        altercon = list_histo[1].GetBinContent(bin)
        dev = fabs(altercon - nomcon)
        err = max([dev, err])
        # store the error into array
        # provide the fractional uncertainty
        syst.append(1.*err/nomcon)
    
    # STEP3:
    # make output histograms
    dict={}
    dict["NOM"]=list_histo[0]
    histo_up = list_histo[0].Clone("1v1_UP")
    histo_dn = list_histo[0].Clone("1v1_DN")
    for num in range(nbins):
        bin = num + 1
        nomcon = list_histo[0].GetBinContent(bin)
        if ratio:
            upcon = 1 + syst[num]
            dncon = 1 - syst[num]
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
            histo_up.SetBinError(bin, 0.)
            histo_dn.SetBinError(bin, 0.)
        else:
            upcon = nomcon * (1 + syst[num])
            dncon = nomcon * (1 - syst[num])
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
    dict["UP"]=histo_up
    dict["DN"]=histo_dn
            
    # Return
    return dict

    
#########################
# Function systCombine()
#########################
# Get the uncertainty as quadratic sum of input histograms
# Input: list_histo_sysup: list of histograms as nominal (0-th), up systematics-set 1 (1-th), ..., up systematics- set n (n-th)
# Input: list_histo_sysdn: list of histograms as nominal (0-th), down systematics-set 1 (1-th), ..., down systematics- set n (n-th)
# Option: symmetrize: symmetrize errors (True) or not (False)
# Option: ratio: error histograms calculated as fractional (True) or absolute (False)
# Output: a dictionary of {"NOM": histo_nom, "UP": +1sigma, "DN": -1sigma}    

def systCombine(list_histo_sysup=[], list_histo_sysdn=[], symmetrize=True, ratio=False):

    print("INFO: calculate uncertainty quadratic sum of the input sources")
    
    # STEP1: 
    # perform check on input histograms
    nhisto_up = len(list_histo_sysup)
    nhisto_dn = len(list_histo_sysdn)
    if nhisto_up!=nhisto_dn:
        print("ERROR: expect exactly same number of histograms between up and down systematics")
        sys.exit(-1)
    nhisto=nhisto_up
    if nhisto<2:
        print("ERROR: expect at lease 2 histograms")
        sys.exit(-1)
    for index in range(nhisto):
        if not list_histo_sysup[index] or not list_histo_sysdn[index]:
            print("ERROR: histogram has a problem: {0}-th".format(index))
            sys.exit(-1)
    nbins=list_histo_sysup[0].GetNbinsX()
    for index in range(nhisto):
        this_nbins_up=list_histo_sysup[index].GetNbinsX()
        this_nbins_dn=list_histo_sysdn[index].GetNbinsX()
        if this_nbins_up!=nbins or this_nbins_dn!=nbins:
            print("ERROR: expect number of bins to be {0}: {1}-th".format(nbins, index))
            sys.exit(-1)
        
    # STEP2:
    # initialize two arrays to store Up/Down errors
    # scan histograms and do the calculations
    sys_up = []
    sys_dn = []
    for num in range(nbins):
        bin = num + 1
        err_up, err_dn = 0., 0.
        # if bin content = 0
        nomcon=list_histo_sysup[0].GetBinContent(bin)
        if nomcon==0.:
            sys_up.append(0.)
            sys_dn.append(0.)
            continue
        # loop all the sets
        for set in range(nhisto):
            upcon = list_histo_sysup[set].GetBinContent(bin)
            dncon = list_histo_sysdn[set].GetBinContent(bin)
            devup = upcon-nomcon
            devdn = dncon-nomcon
            err_up = sqrt(pow(devup,2)+pow(err_up,2))
            err_dn = sqrt(pow(devdn,2)+pow(err_dn,2))
        # store the up/down error into array
        # provide the fractional uncertainty
        average=(err_up+err_dn)/2.
        if symmetrize: 
            sys_up.append(1.*average/nomcon)
            sys_dn.append(1.*average/nomcon)
        else:
            sys_up.append(1.*err_up/nomcon)
            sys_dn.append(1.*err_dn/nomcon)
    
    # STEP3:
    # make output histograms
    dict={}
    dict["NOM"]=list_histo_sysup[0]
    histo_up = list_histo_sysup[0].Clone("COM_UP")
    histo_dn = list_histo_sysup[0].Clone("COM_DN")
    for num in range(nbins):
        bin = num + 1
        nomcon = list_histo_sysup[0].GetBinContent(bin)
        if ratio:
            upcon = 1 + sys_up[num]
            dncon = 1 - sys_dn[num]
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
            histo_up.SetBinError(bin, 0.)
            histo_dn.SetBinError(bin, 0.)
        else:
            upcon = nomcon * (1 + sys_up[num])
            dncon = nomcon * (1 - sys_dn[num])
            histo_up.SetBinContent(bin, upcon)
            histo_dn.SetBinContent(bin, dncon)
    dict["UP"]=histo_up
    dict["DN"]=histo_dn
            
    # Return
    return dict    
    
    
    