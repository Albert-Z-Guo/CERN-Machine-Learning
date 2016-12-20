# ROOT paths configuration
# make sure to run 'source setup.sh' beforehand
import os
import sys
import math

ROOTLIB = ""
if os.getenv("ROOTLIB"):
    ROOTLIB = os.getenv("ROOTLIB")
sys.path.append(ROOTLIB)

# import ROOT modules
from ROOT import TFile, TCanvas, TColor, gStyle, TLegend, TLatex, TH1F, TTree, TGraph

# import user's modules
import numpy as np
from oneplot import oneplot

EFF_SIGNAL_PRE_SELECTION = (209752./890100)
EFF_BACKGROUND_PRE_SELECTION = (115629./1014200)
EFF_SIGNAL_DIRECT_CUT = (167093./209752)
EFF_BACKGROUND_DIRECT_CUT = (12342./115629)

# plot two histograms on the same canvas
def plot_two_histograms(normalization_option, file_name_portion):
    histograms = []

    # no noramlization
    if normalization_option == 0:
        pass
    # normalize the histograms to 40fb-1 with their respective cross-section
    if normalization_option == 1:
        # print "'signals' has type: ", type(signals)
        signals.Scale(0.18 * 40 * EFF_SIGNAL_PRE_SELECTION / signals.Integral(0, -1))
        backgrounds.Scale(1.85 * 40 * EFF_BACKGROUND_PRE_SELECTION / backgrounds.Integral(0, -1))

    # normalize the histograms to unity area
    if normalization_option == 2:
        signals.Scale(1. / signals.Integral(0, -1))
        backgrounds.Scale(1. / backgrounds.Integral(0, -1))

    histograms.append(signals)
    histograms.append(backgrounds)

    names = []
    names.append("VBS signal")
    names.append("QCD background")

    xtitle = "BDT Score"
    ytitle = "events scaled"
    legends = ["VBS signal", "QCD background"]

    options = ["HIST", "HIST"]
    opt_legends = ["L", "L"]
    marker_types = [26, 32]
    marker_sizes = [1, 3]
    line_sizes = [2, 2]
    marker_colors = line_colors = fill_colors = [30, 38]
    fill_types = [0, 0]

    if normalization_option == 0:
        figname = "BDT_classification_cut_"  + file_name_portion + "_rebinned"
    elif normalization_option == 1:
        figname = "BDT_classification_cut_"  + file_name_portion + "_normalized_to_40fb-1_rebinned"
    elif normalization_option == 2:
        figname = "BDT_classification_cut_"  + file_name_portion + "_normalized_to_unity_area_rebinned"

    # call oneplot.py for plotting in ATLAS style
    theone = oneplot()
    theone._figtype = ["png"]
    theone.initialize(list_histo=histograms, names=names, legends=legends, opt_legends=opt_legends,
                      xtitle=xtitle, ytitle=ytitle,
                      figname=figname,
                    #   binning=np.arange(-1, 1.03, 0.03).tolist(),
                      options=options, marker_types=marker_types, marker_colors=marker_colors, marker_sizes=marker_sizes,
                      line_colors=line_colors, line_sizes=line_sizes,
                      fill_colors=fill_colors, fill_types=fill_types)
    theone.plot1DHistogram()
    theone.finish()

# plot the ROC curve
def plot_ROC_curve(ROC_curve, file_name_portion):

    gStyle.SetOptStat(0)
    gStyle.SetLabelSize(0.03, "xy")
    gStyle.SetTitleSize(0.03, "xy")
    gStyle.SetTitleOffset(1.2, "xy")
    gStyle.SetPadLeftMargin(0.15)
    gStyle.SetPadRightMargin(0.1)
    gStyle.SetPadTopMargin(0.1)
    gStyle.SetPadBottomMargin(0.15)

    canvas = TCanvas("c1", "c1", 800, 800)
    canvas.SetTickx()
    canvas.SetTicky()

    ROC_curve.GetYaxis().SetTitle('Background rejection')
    ROC_curve.GetXaxis().SetTitle('Signal efficiency')
    ROC_curve.SetLineColor(TColor.kAzure)
    ROC_curve.SetFillColor(TColor.kAzure - 2)
    ROC_curve.SetLineWidth(2)
    ROC_curve.SetFillStyle(0)

    from array import array
    x, y = array( 'd' ), array( 'd' )
    x.append(EFF_SIGNAL_DIRECT_CUT)
    y.append(1 - EFF_BACKGROUND_DIRECT_CUT)
    dot = TGraph(1, x, y)
    dot.SetMarkerColor(8)
    dot.SetMarkerSize(3)
    dot.SetMarkerStyle(21)

    legend = TLegend(0.2, 0.2, 0.4, 0.4)
    legend.SetTextSize(0.04)
    legend.SetTextFont(42)
    legend.SetFillColor(10)
    legend.SetLineColor(10)
    legend.SetBorderSize(0)
    legend.AddEntry(ROC_curve, "BDT 500 trees", "l")
    legend.AddEntry(dot, "m_{jj} > 500 GeV and |#Delta#eta_{jj}| > 3 cut", "P")

    ROC_curve.Draw("HIST")
    legend.Draw("same")
    dot.Draw("LPsame")
    canvas.RedrawAxis()
    canvas.Print(file_name_portion + "_ROC" + ".png")

if __name__ == "__main__":
    file_list = [
                    # "/atlas/data19/zuguo/data/BDT/jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj_dtop.root",
                    # "/atlas/data19/zuguo/data/BDT/jj_m_zz_m_z_pt_delta_eta_jj_l_pt_dtop.root",
                    "/atlas/data19/zuguo/data/BDT/jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal_dtop.root"
                ]

    for file_name in file_list:
        # read the root file in list
        root_file = TFile(file_name)

        # extract histograms from the root file
        file_name_portion = file_name.split("/")[-1].split(".")[0][0:(len(file_name.split("/")[-1].split(".")[0])-5)]
        signals = root_file.Get("Method_BDT/dtop_" + file_name_portion +  "/MVA_dtop_" + file_name_portion + "_S")
        backgrounds = root_file.Get("Method_BDT/dtop_" + file_name_portion +  "/MVA_dtop_" + file_name_portion + "_B")
        ROC_curve = root_file.Get("Method_BDT/dtop_" + file_name_portion +  "/MVA_dtop_" + file_name_portion + "_rejBvsS")

        # plot histograms in different normalization options
        for normalization_option in range(3):
            plot_two_histograms(normalization_option, file_name_portion)

        # plot ROC curves
        plot_ROC_curve(ROC_curve, file_name_portion)

        # close the read file
        root_file.Close()
