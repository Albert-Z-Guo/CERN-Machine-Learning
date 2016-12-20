# ROOT paths configuration
# make sure to run 'source setup.sh' beforehand
import os
import sys
import math

ROOTLIB, PATH_OnePlot_MODULE1, PATH_OnePlot_MODULE2 = "", "", ""

if os.getenv("ROOTLIB"):
    ROOTLIB = os.getenv("ROOTLIB")
if os.getenv("PATH_OnePlot_MODULE1"):
    PATH_OnePlot_MODULE1 = os.getenv("PATH_OnePlot_MODULE1")
if os.getenv("PATH_OnePlot_MODULE2"):
    PATH_OnePlot_MODULE2 = os.getenv("PATH_OnePlot_MODULE2")

# import ROOT modules
from ROOT import TFile, TCanvas, TColor, gStyle, TLegend, TLatex, TH1F, TTree, TGraph

# import user's modules
import numpy as np
from oneplot import oneplot
from module_syst import systPDFCT10, systEnvelope, syst1v1, systCombine
from module_style import atlas_style

EFF_SIGNAL_PRE_SELECTION = (209752./890100)
EFF_BACKGROUND_PRE_SELECTION = (115629./1014200)

FILE_PATH = "/atlas/data19/zuguo/data"

# axes titles map
AXES_TITLES = {
    "zz_m": ["M_{ZZ} [GeV]", "events"],
    "jj_m": ["M_{jj} [GeV]", "events"],
    "delta_eta_jj": ["#Delta#eta_{jj}", "events"],
    "z1_pt": ["Pt_{Z1} [GeV]", "events"],
    "z2_pt": ["Pt_{Z2} [GeV]", "events"],
}

# legends map
LEGENDS = {
    "zz_m": ["M_{ZZ} final selection", "M_{ZZ} pre-selection"],
    "jj_m": ["M_{jj} final selection", "M_{jj} pre-selection"],
    "delta_eta_jj": ["#Delta#eta_{jj} final selection ", "#Delta#eta_{jj} pre-selection"],
    "z1_pt": ["Pt_{Z1} final selection", "Pt_{Z1} pre-selection"],
    "z2_pt": ["Pt_{Z2} final selection", "Pt_{Z2} pre-selection"],
}

# binning setting of histograms map referred from tree2hist.cxx
BINNING = {
    "zz_m": np.arange(0, 500, 10).tolist(),
    "jj_m": np.arange(0, 3000, 60).tolist(),
    "delta_eta_jj": np.arange(0, 10, 0.25).tolist(),
    "z1_pt": np.arange(0, 500, 10).tolist(),
    "z2_pt": np.arange(0, 500, 10).tolist(),
}

# output file name map
FIGURE_NAME = {
    "zz_m": "zz_m_distribution_by_BDT_classification_cut",
    "jj_m": "jj_m_distribution_by_BDT_classification_cut",
    "delta_eta_jj": "delta_eta_jj_distribution_by_BDT_classification_cut",
    "z1_pt": "z1_pt_distribution_by_BDT_classification_cut",
    "z2_pt": "z2_pt_distribution_by_BDT_classification_cut",
}

# plot histograms of each process and each variable
def plot_histograms(process, variable_name, normalization_option):
    # read histograms from the signal files
    if process == 'signal':
        root_file_1 = TFile(FILE_PATH + "/BDT/BDT_Signal_histogram_3.root")
        root_file_2 = TFile(FILE_PATH + "/210_eeee_fid_preselected_histograms.root")
        signals = root_file_1.Get(variable_name)
        backgrounds = root_file_2.Get(variable_name)

        # specify the output png file name in different cases
        # no normalization
        if normalization_option == 0:
            figname = "signal_" + FIGURE_NAME[variable_name]
        # normalize the histograms to 40fb-1 with their respective cross-section
        elif normalization_option == 1:
            signals.Scale(0.18 * 40 * EFF_SIGNAL_PRE_SELECTION / signals.Integral(0, -1))
            backgrounds.Scale(1.85 * 40 * EFF_BACKGROUND_PRE_SELECTION / backgrounds.Integral(0, -1))
            figname = "signal_" + FIGURE_NAME[variable_name] + "_normalized_to_40fb-1"
        # normalize the histograms to unity area
        elif normalization_option == 2:
            signals.Scale(1. / signals.Integral(0, -1))
            backgrounds.Scale(1. / backgrounds.Integral(0, -1))
            figname = "signal_" + FIGURE_NAME[variable_name] + "_normalized_to_unity_area"

    elif process == 'background':
        root_file_1 = TFile(FILE_PATH + "/BDT/BDT_Background_histogram_3.root")
        root_file_2 = TFile(FILE_PATH + "/3210_eeee_fid_preselected_histograms.root")
        signals = root_file_1.Get(variable_name)
        backgrounds = root_file_2.Get(variable_name)

        print "signal events:", signals.Integral(0, -1)
        print "background events", backgrounds.Integral(0, -1)

        # if there is no signal or backround event, do not normalize the histograms
        if(signals.Integral(0, -1)==0 or backgrounds.Integral(0, -1)==0):
            normalization_option = 0

        # specify the output png file name in different cases
        # no normalization
        if normalization_option == 0:
            figname = "background_" + FIGURE_NAME[variable_name]
        # normalize the histograms to 40fb-1 with their respective cross-section
        elif normalization_option == 1:
            signals.Scale(0.18 * 40 * EFF_SIGNAL_PRE_SELECTION / signals.Integral(0, -1))
            backgrounds.Scale(1.85 * 40 * EFF_BACKGROUND_PRE_SELECTION / backgrounds.Integral(0, -1))
            figname = "background_" + FIGURE_NAME[variable_name] + "_normalized_to_40fb-1"
        # normalize the histograms to unity area
        elif normalization_option == 2:
            signals.Scale(1. / signals.Integral(0, -1))
            backgrounds.Scale(1. / backgrounds.Integral(0, -1))
            figname = "background_" + FIGURE_NAME[variable_name] + "_normalized_to_unity_area"


    histograms = []
    histograms.append(signals)
    histograms.append(backgrounds)

    names = []
    names.append("final selection")
    names.append("pre-selection")

    xtitle = AXES_TITLES[variable_name][0]
    ytitle = AXES_TITLES[variable_name][1]
    legends = LEGENDS[variable_name]

    options = ["HIST", "HIST"]
    opt_legends = ["L", "L"]
    marker_types = [26, 32]
    marker_sizes = [1, 3]
    line_sizes = [2, 2]
    marker_colors = line_colors = fill_colors = [30, 38]
    fill_types = [0, 0]

    # call oneplot.py for plotting in ATLAS style
    theone = oneplot()
    theone._figtype = ["png"]
    theone.initialize(list_histo=histograms, names=names, legends=legends, opt_legends=opt_legends,
                      xtitle=xtitle, ytitle=ytitle,
                      figname=figname,
                      #   binning= [i*0.25 for i in range(40)],
                      binning = BINNING[variable_name],
                      options=options, marker_types=marker_types, marker_colors=marker_colors, marker_sizes=marker_sizes,
                      line_colors=line_colors, line_sizes=line_sizes,
                      fill_colors=fill_colors, fill_types=fill_types)
    theone.plot1DHistogram()
    theone.finish()

    # close the read files
    root_file_1.Close()
    root_file_2.Close()


if __name__ == "__main__":
    variables = ["zz_m", "jj_m", "delta_eta_jj", "z1_pt", "z2_pt"]
    for var in variables:
        print "current variable:", var
        for normalization_option in range(3):
            plot_histograms("signal", var, normalization_option)
            plot_histograms("background", var, normalization_option)
