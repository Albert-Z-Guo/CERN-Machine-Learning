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
EFF_SIGNAL_DIRECT_CUT = (167093./209752)
EFF_BACKGROUND_DIRECT_CUT = (12342./115629)

SIGNAL_DIRECT_UNCERTAINTY = math.sqrt(167093) / 167093
BACKGROUND_DIRECT_UNCERTAINTY = math.sqrt(12342) / 12342

def calculate_figure_of_merit(signals, backgrounds):

    # find the score cuts for maximal figure of merits
    def calculate_figure_of_merit_1(i, signals, backgrounds):
        return signals.GetBinContent(i + 1) / backgrounds.GetBinContent(i + 1)

    def calculate_figure_of_merit_2(i, signals, backgrounds):
        return signals.GetBinContent(i + 1) / math.sqrt(backgrounds.GetBinContent(i + 1))

    def calculate_figure_of_merit_3(i, signals, backgrounds):
        return math.sqrt(2 * ((signals.GetBinContent(i + 1) + backgrounds.GetBinContent(i + 1)) * math.log(1 + signals.GetBinContent(i + 1) / backgrounds.GetBinContent(i + 1)) - signals.GetBinContent(i + 1)))

    # initialize variables
    figure_of_merit_1 = 0
    score_cut_1 = 0
    bin_cut_1 = 0
    figure_of_merit_2 = 0
    score_cut_2 = 0
    bin_cut_2 = 0
    figure_of_merit_3 = 0
    score_cut_3 = 0
    bin_cut_3 = 0

    for i in range(signals.GetNbinsX()):
        # test to find the bin numbers near score 0
        # print i
        # print backgrounds.GetBinLowEdge(i)
        # if abs(backgrounds.GetBinLowEdge(i) - 0) < 0.2:
        #     print "bin number near 0: ", i
        if backgrounds.GetBinContent(i + 1) == 0:
            continue
        if figure_of_merit_1 < calculate_figure_of_merit_1(i, signals, backgrounds):
            figure_of_merit_1 = calculate_figure_of_merit_1(i, signals, backgrounds)
            bin_cut_1 = i + 1
            score_cut_1 = signals.GetBinLowEdge(i + 1)
        if figure_of_merit_2 < calculate_figure_of_merit_2(i, signals, backgrounds):
            figure_of_merit_2 = calculate_figure_of_merit_2(i, signals, backgrounds)
            bin_cut_2 = i + 1
            score_cut_2 = backgrounds.GetBinLowEdge(i + 1)
        if figure_of_merit_3 < calculate_figure_of_merit_3(i, signals, backgrounds):
            figure_of_merit_3 = calculate_figure_of_merit_3(i, signals, backgrounds)
            bin_cut_3 = i + 1
            score_cut_3 = backgrounds.GetBinLowEdge(i + 1)

    print "\n\n\nAs for ", file_name, ":"
    print "maximal S/B: {0:.1f} at score = {1:.2f}".format(figure_of_merit_1, score_cut_1)
    print "maximal S/sqrt(B): {0:.1f} at score = {1:.2f}".format(figure_of_merit_2, score_cut_2)
    print "maximal log likelihood of Poisson statistics: {0:.1f} at score = {1:.2f}".format(figure_of_merit_3, score_cut_3)

    # Yield (no selection) = luminosity (40) x cross-section (S/B)
    # Yield (after pre-selection) = luminosity (40) x cross-section (S/B) x eff(pre-selection)
    # Yield (after final selection) = luminosity (40) x cross-section (S/B) x eff(pre-selection) x eff(S/B selection)
    BDT_estimated_signal_events = 40 * 0.18 * EFF_SIGNAL_PRE_SELECTION * signals.Integral(bin_cut_3, -1) / signals.Integral(0, -1)
    BDT_estimated_background_events = 40 * 1.85 * EFF_BACKGROUND_PRE_SELECTION * backgrounds.Integral(bin_cut_3, -1) / backgrounds.Integral(0, -1)
    m_jj_delta_eta_jj_cut_estimated_signal_events = 0.18 * 40 * EFF_SIGNAL_PRE_SELECTION * EFF_SIGNAL_DIRECT_CUT
    m_jj_delta_eta_jj_cut_estimated_background_events = 1.85 * 40 * EFF_BACKGROUND_PRE_SELECTION * EFF_BACKGROUND_DIRECT_CUT
    print "BDT estimated signal events: {0:.3f}".format(BDT_estimated_signal_events)
    print "BDT estimated backgrounds events: {0:.3f}".format(BDT_estimated_background_events)
    print "m_jj_delta_eta_jj_cut estimated signal events: {0:.3f}".format(m_jj_delta_eta_jj_cut_estimated_signal_events)
    print "m_jj_delta_eta_jj_cut estimated signal uncertain events: {0:.5f}".format(m_jj_delta_eta_jj_cut_estimated_signal_events * SIGNAL_DIRECT_UNCERTAINTY)
    print "m_jj_delta_eta_jj_cut estimated backgrounds events: {0:.3f}".format(m_jj_delta_eta_jj_cut_estimated_background_events)
    print "m_jj_delta_eta_jj_cut estimated backgrounds uncertain events: {0:.5f}".format(m_jj_delta_eta_jj_cut_estimated_signal_events * BACKGROUND_DIRECT_UNCERTAINTY)

    # scan from 18th bin to 30th bin (from score around 0.21 to 0.33)
    for bin_number in range(51, 85, 2):
        BDT_estimated_signal_events = 0.18 * 40 * EFF_SIGNAL_PRE_SELECTION * signals.Integral(bin_number, -1) / signals.Integral(0, -1)
        BDT_estimated_background_events = 1.85 * 40 * EFF_BACKGROUND_PRE_SELECTION * backgrounds.Integral(bin_number, -1) / backgrounds.Integral(0, -1)

        print "signals events", signals.Integral(bin_number, -1)
        print "backgrounds events", backgrounds.Integral(bin_number, -1)

        # uncertainty = sqrt(# of events) / (# of events)
        signal_uncertainty = math.sqrt(signals.Integral(bin_number, -1)) / signals.Integral(bin_number, -1)
        background_uncertainty = math.sqrt(backgrounds.Integral(bin_number, -1)) / backgrounds.Integral(bin_number, -1)

        print "\nat score cut: {0:.3f}".format(backgrounds.GetBinLowEdge(bin_number))
        print "BDT estimated signal events: {0:.4f}".format(BDT_estimated_signal_events)
        print "BDT estimated signal uncertainty: {0:.6f}".format(signal_uncertainty)
        print "BDT estimated signal uncertain events: {0:.6f}".format(BDT_estimated_signal_events * signal_uncertainty)

        print "BDT estimated backgrounds events: {0:.6f}".format(BDT_estimated_background_events)
        print "BDT estimated background uncertainty: {0:.8f}".format(background_uncertainty)
        print "BDT estimated background uncertain events: {0:.8f}".format(BDT_estimated_background_events * background_uncertainty)


def plot_histograms(normalization_option, file_name):

    # read the root file in list
    root_file_1 = TFile(file_name)
    root_file_2 = TFile(file_name.split("_")[0] + "_Background_histogram_" + file_name.split(".")[0].split("_")[-1] + ".root")

    # read signal and background histograms from the file
    signals = root_file_1.Get("h1")
    backgrounds = root_file_2.Get("h1")

    # calculate figure of merits
    calculate_figure_of_merit(signals, backgrounds)

    # read suffix of the file
    suffix = file_name.split(".")[0].split("_")[-1]

    # no normalization
    if normalization_option == 0:
        # specify the output png file name
        figname = "BDT_signal_background_distribution_" + suffix

    # normalize the histograms to 40fb-1 with their respective cross-sections
    if normalization_option == 1:
        signals.Scale(0.18 * 40 * EFF_SIGNAL_PRE_SELECTION / signals.Integral(0, -1))
        backgrounds.Scale(1.85 * 40 * EFF_BACKGROUND_PRE_SELECTION / backgrounds.Integral(0, -1))
        # specify the output png file name
        figname = "BDT_signal_background_distribution_normalized_to_unity_area_" + suffix

    # normalize the histograms to unity area
    elif normalization_option == 2:
        print "total numebr of signal events", signals.Integral(0, -1)
        print "total numebr of background events", backgrounds.Integral(0, -1)
        signals.Scale(1. / signals.Integral(0, -1))
        backgrounds.Scale(1. / backgrounds.Integral(0, -1))
        # specify the output png file name
        figname = "BDT_signal_background_distribution_normalized_to_40fb-1_" + suffix

    histograms = []
    histograms.append(signals)
    histograms.append(backgrounds)

    names = []
    names.append("signal")
    names.append("background")

    xtitle = "BDT Score"
    if normalization_option == 0:
        ytitle = "events"
    elif normalization_option == 1:
        ytitle = "events normalized to 40 fb-1"
    elif normalization_option == 2:
        ytitle = "events normalized to unity area"
    legends = ["VBS Singal", "QCD Background"]

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
                      options=options, marker_types=marker_types, marker_colors=marker_colors, marker_sizes=marker_sizes,
                      line_colors=line_colors, line_sizes=line_sizes,
                      fill_colors=fill_colors, fill_types=fill_types)
    theone.plot1DHistogram()
    theone.finish()

    # close the read files
    root_file_1.Close()
    root_file_2.Close()


if __name__ == "__main__":
    file_list = [#"/atlas/data19/zuguo/data/BDT/BDT_Signal_histogram_1.root",
                    #"/atlas/data19/zuguo/data/BDT/BDT_Signal_histogram_2.root",
                    "/atlas/data19/zuguo/data/BDT/BDT_Signal_histogram_3.root"
                ]

    for file_name in file_list:
        plot_histograms(0, file_name)
        plot_histograms(1, file_name)
        plot_histograms(2, file_name)
