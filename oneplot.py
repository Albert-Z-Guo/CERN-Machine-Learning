#!/usr/bin/python2.6

# / / /
# \ \ \
# / / /
# Y.Wu <wyusheng@umich.edu>

###################################
# Python Class to plot histograms
###################################

########################
# Libraries and Includes
########################

# Python System Modules
import os
import sys
import glob
import logging

# Python Paths
ROOTLIB, PATH_OnePlot_MODULE1, PATH_OnePlot_MODULE2 = "", "", ""

if os.getenv("ROOTLIB"):
    ROOTLIB = os.getenv("ROOTLIB")
if os.getenv("PATH_OnePlot_MODULE1"):
    PATH_OnePlot_MODULE1 = os.getenv("PATH_OnePlot_MODULE1")
if os.getenv("PATH_OnePlot_MODULE2"):
    PATH_OnePlot_MODULE2 = os.getenv("PATH_OnePlot_MODULE2")

sys.path.append(ROOTLIB)
sys.path.append(PATH_OnePlot_MODULE1)
sys.path.append(PATH_OnePlot_MODULE2)

# Python Math Modules
import array
from math import sqrt, fabs, sin, pow

# ROOT Modules
from ROOT import TFile, TTree, TChain, TBranch, TH1F, TH2F
from ROOT import TCanvas, TPad
from ROOT import TLorentzVector
from ROOT import gROOT, gDirectory, gStyle
from ROOT import TPaveText, TLegend
import ROOT

# user modules
from module_style import atlas_style

#########
# OnePlot
#########


class oneplot:

    """
    To plot with input histograms
    """

    ##############
    # Initialize #
    ##############
    def __init__(self, verbose="INFO"):

        # in most cases some of the settings are not necessary to change
        # the default values are given below and variable names should be self-explanatory
        # if one wishes to change these setting, can do manually after initialization
        # e.g. oneplot._ABC = XYZ
        self._xaxis_title_size = 0.06
        self._yaxis_title_size = 0.06
        self._xaxis_title_offset = 1.2
        self._yaxis_title_offset = 1.2
        self._labelsize = 0.06
        self._lumi_in_pb = 30000.
        self._draw_text = "VBFNLO"
        self._center_mass_energy = "13 TeV"
        self._figtype = ["png"]  # or self._figtype=["png", "pdf", ...]

        # other general plotting elements
        self.dict = {}  # dictionary to store all inputs
        self.fin = None  # the TFile object for input histograms
        self.MyC = TCanvas()  # Canvas
        self.Pad1 = TPad()  # Pad1 if request a ratio plot
        self.Pad2 = TPad()  # Pad2 if request a ratio plot

        self.name = ""  # store the name of first histogram
        # store the first histogram in order to adjust axis attributes post
        # initial plotting
        self.firsthisto = None
        self.firstratio_name = ""  # store the name of first histogram to be drawn on ratio plot
        # store the first ratio histogram in order to adjust axis attributes
        self.firstratio = None
        self.denomname = ""  # store the name of histogram to be used as denominator in ratio plot

        self.max = - \
            9999.  # store the maximum y axis value needed for plotting (1D histogram)
        # store the minimum y axis value needed for plotting (1D histogram)
        self.min = 1.e9
        self.force_max = -9999.  # store the forced maximum value for plotting
        self.force_min = 1.e9  # store the forced minimum value for plotting
        self.maxbin = -1  # store the bin index where maximum happens
        self.rmax = - \
            99.  # store the maximum y axis value on ratio plot (1D histogram)
        # store the minimum  y axis value on ratio plot (1D histogram)
        self.rmin = 99.

        # initialize the necessary inputs
        # the actual values should be modified after initialization

        # >>>>>> Start of inputs

        # root file containing the histograms
        self.file = ""

        # the binning of histogram, in the case this is different from original binning, a re-binning will be performed
        # for 1D histogram, e.g. binning=[0,1,2,3....]
        # for >=2D histogram, e.g. binning=[ [0,1,2...], [0,1,2...] ] = [ X-bining, Y-bining]
        # BinType: Type1 -> [ nbins, low-bound, up-bound], Type2 -> [bin1,
        # bin2, ... binN]
        self.binning = []
        self.bintype = "Type2"

        # do equal bins?
        # assign same width for each bin even if they are not in equal range
        # this will also make changes accordingly on the axis label
        self.equalbin = False

        # the names of histograms to be plotted
        # and the legends, colors, plotting options
        self.names = []  # histogram names
        self.legends = []  # texts to draw the legends
        self.opt_legends = []  # options to draw the legends
        self.options = []  # options to draw the histograms
        self.colors = [ROOT.kBlack, ROOT.kOrange, ROOT.kRed, ROOT.kGreen - 9, ROOT.kMagenta, ROOT.kBlue, ROOT.kAzure - 8,
                       ROOT.kCyan, ROOT.kGreen + 2, ROOT.kSpring, ROOT.kYellow -
                       3, ROOT.kViolet - 6, ROOT.kSpring + 10,
                       ROOT.kYellow - 10, ROOT.kYellow - 7, ROOT.kYellow -
                       4, ROOT.kYellow - 1, ROOT.kYellow + 2, ROOT.kYellow + 5,
                       ROOT.kYellow + 8, ROOT.kRed - 10, ROOT.kRed - 7, ROOT.kRed -
                       4, ROOT.kRed - 1, ROOT.kRed + 2, ROOT.kRed + 5,
                       ROOT.kRed + 8, ROOT.kMagenta - 10, ROOT.kMagenta -
                       7, ROOT.kMagenta - 4, ROOT.kMagenta - 1, ROOT.kMagenta + 2,
                       ROOT.kMagenta + 5, ROOT.kMagenta + 8, ROOT.kBlue - 10, ROOT.kBlue -
                       7, ROOT.kBlue - 4, ROOT.kBlue - 1, ROOT.kBlue + 2,
                       ROOT.kBlue + 5, ROOT.kBlue + 8, ROOT.kCyan - 10, ROOT.kCyan -
                       7, ROOT.kCyan - 4, ROOT.kCyan - 1, ROOT.kCyan + 2,
                       ROOT.kCyan + 5, ROOT.kCyan + 8, ROOT.kGreen - 10, ROOT.kGreen -
                       7, ROOT.kGreen - 4, ROOT.kGreen - 1, ROOT.kGreen + 2,
                       ROOT.kGreen + 5, ROOT.kGreen + 8]  # this is the default color setting

        # X, Y axis title and Y axis title for ratio plot if applicable
        self.xtitle, self.ytitle, self.ratiotitle = "", "", ""

        # figure name
        # output plot will be figname+".png/.XXX"
        self.figname = ""

        # if want to add ratio plot, give the size of ratio TPAD / normal TPAD
        self.ratio = -1

        # additional parameters to help regularize ratio plots
        # by default the ratio plot is made by treating the first histogram as denominator and take every other histogram into consideration
        # the changes of action will take place only if the following variables are not empty
        # if ratio_denominater!="", will use specified histogram as denominator for ratio plot calculation
        # if doratio[i] = True/False, means whether or not add i-th histogram
        # into ratio plot
        self.ratio_denominater = ""
        self.doratio = []

        # plotting options for ratio
        # in the case you want to plot the ratios differently from the main
        # plot, need to setup this
        self.options_ratio = []

        # additional setups for plotting, the names should be self explanatory
        # include the types/colors/sizes for markers/fills/lines ...
        self.marker_types, self.marker_colors, self.marker_sizes = [], [], []
        self.line_types, self.line_colors, self.line_sizes = [], [], []
        self.fill_types, self.fill_colors = [], []

        self.ratio_marker_types, self.ratio_marker_colors, self.ratio_marker_sizes = [], [], []
        self.ratio_line_types, self.ratio_line_colors, self.ratio_line_sizes = [], [], []
        self.ratio_fill_types, self.ratio_fill_colors = [], []

        # <<<<<< End of inputs

        # create the logger and set the LEVEL
        self.logger = logging.getLogger("OnePlot")
        if verbose == "INFO":
            self.logger.setLevel(logging.INFO)
        if verbose == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        if verbose == "ERROR":
            self.logger.setLevel(logging.ERROR)
        stream = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s     %(name)-12s:  %(levelname)-8s  %(message)s')
        stream.setFormatter(formatter)
        self.logger.addHandler(stream)

        # first screen printout
        self.logger.info("")
        self.logger.info("")
        self.logger.info("")
        self.logger.info("--------------------")
        self.logger.info("----- One Plot -----")
        self.logger.info("--------------------")
        self.logger.info("")

        # put a end mark
        return

    #################
    # Main Work flow
    #################

    # functions:
    # >>>>>>
    # initialize()
    # readInputs()
    # readOptions(index=0)
    # plot1D()
    # plot2D()
    #
    # ...
    # <<<<<<

    # >>>
    # Initialize
    # >>>

    # initialize the necessary inputs for plotting
    def initialize(self, file="", list_histo=[], names=[], binning=[], legends=[], opt_legends=[],
                   options=[], colors=[], ratio=-1, figname="",
                   xtitle="", ytitle="", ratiotitle="",
                   equalbin=False,
                   ratio_denominater="", doratio=[], options_ratio=[],
                   marker_types=[], marker_colors=[], marker_sizes=[],
                   line_types=[], line_colors=[], line_sizes=[],
                   fill_types=[], fill_colors=[],
                   ratio_marker_types=[], ratio_marker_colors=[], ratio_marker_sizes=[],
                   ratio_line_types=[], ratio_line_colors=[], ratio_line_sizes=[],
                   ratio_fill_types=[], ratio_fill_colors=[],
                   force_min=1.e9, force_max=-9999.):
        # This function is provided to setup all necessary inputs at one place
        # one can also initialize them by directly assigning values to members of this class
        # e.g. self.names=["abc"]
        self.logger.info("Initialize plotting parameters")

        # assign the values if inputs not empty
        if file != "":
            self.file = file
        self.list_histo = list_histo
        if len(names) != 0:
            self.names = names
        if len(binning) != 0:
            self.binning = binning
        if len(legends) != 0:
            self.legends = legends
        if len(options) != 0:
            self.options = options
        if len(colors) != 0:
            self.colors = colors
        if ratio != -1:
            self.ratio = ratio
        if figname != "":
            self.figname = figname
        if xtitle != "":
            self.xtitle = xtitle
        if ytitle != "":
            self.ytitle = ytitle
        if ratiotitle != "":
            self.ratiotitle = ratiotitle
        self.opt_legends = opt_legends
        self.equalbin = equalbin

        # assign additional variables
        self.ratio_denominater = ratio_denominater
        self.doratio = doratio
        self.options_ratio = options_ratio
        self.marker_types = marker_types
        self.marker_colors = marker_colors
        self.fill_types = fill_types
        self.fill_colors = fill_colors
        self.line_types = line_types
        self.line_colors = line_colors
        self.ratio_marker_types = ratio_marker_types
        self.ratio_marker_colors = ratio_marker_colors
        self.ratio_fill_types = ratio_fill_types
        self.ratio_fill_colors = ratio_fill_colors
        self.ratio_line_types = ratio_line_types
        self.ratio_fill_colors = ratio_fill_colors
        self.ratio_marker_sizes = ratio_marker_sizes
        self.ratio_line_sizes = ratio_line_sizes
        self.marker_sizes = marker_sizes
        self.line_sizes = line_sizes

        # if force the maximum or minimum to some value
        if force_max != -9999.:
            self.force_max = force_max
        if force_min != 1.e9:
            self.force_min = force_min

        # put a end mark
        return

    # >>>
    # Assign options based on arrays
    # >>>
    # this is an internal function
    def _assign_option(self, hname="", dict={}, key="", descr="", list=[], index=-1, default_value_int=None, default_value_str=None, default_value_bool=None):
        # check if the list of options contain the current index, if so make
        # assignment, if not use default value
        if len(list) >= index + 1:
            dict[key] = list[index]
            self.logger.debug("Histogram {0}, manually set {1} as {2}".format(
                hname, descr, dict[key]))
        else:
            if not default_value_int is None:
                dict[key] = default_value_int
            if not default_value_str is None:
                dict[key] = default_value_str
            if not default_value_bool is None:
                dict[key] = default_value_bool
            self.logger.debug("Histogram {0}, auto set {1} as {2}".format(
                hname, descr, dict[key]))

    # >>>
    # Read Options for each histogram
    # >>>
    def readOptions(self, index=0):

        # read input options for index-th histograms
        # and add the information to self.dict{}
        # the default plotting styles are hard-coded

        # read general parameters
        hname = self.names[index]
        color = self.colors[index]
        legend = self.legends[index]
        if len(self.options) >= index + 1:
            option = self.options[index]
        else:
            option = "LPE"

        # logging
        self.logger.info("Load histogram, name=\"{0}\", color=\"{1}\", legend=\"{2}\", option=\"{3}\" ".format(
            hname, color, legend, option))

        # write into dict.: first part
        self.dict[hname] = {}
        self.dict[hname]["LEG"] = legend
        self.dict[hname]["COLOR"] = color
        self.dict[hname]["OPT"] = option

        # read additional plotting parameters if they exist
        # do not check the list size, but if their sizes are up to the index of
        # histogram, will assign the value

        # set1: use as denominator of histograms or not
        if self.ratio_denominater != "" and self.ratio_denominater == hname:
            self.dict[hname]["DENOM"] = True
            self.logger.debug(
                "Histogram: {0} manually set as the denominator".format(hname))
        else:
            self.dict[hname]["DENOM"] = False

        # set2-...
        self._assign_option(hname, self.dict[
                            hname], "OPT_Legend", "Legend Draw Option", self.opt_legends, index, default_value_str=option)
        self._assign_option(hname, self.dict[
                            hname], "DoRatio", "Produce Ratio or Not", self.doratio, index, default_value_bool=True)
        self._assign_option(hname, self.dict[
                            hname], "OptRatio", "Plotting Option for Ratio", self.options_ratio, index, default_value_str=option)
        self._assign_option(hname, self.dict[
                            hname], "MarkerType", "Marker Type", self.marker_types, index, default_value_int=1)
        self._assign_option(hname, self.dict[
                            hname], "MarkerColor", "Marker Color", self.marker_colors, index, default_value_int=color)
        self._assign_option(hname, self.dict[
                            hname], "MarkerSize", "Marker Size", self.marker_sizes, index, default_value_int=1)
        self._assign_option(hname, self.dict[
                            hname], "LineType", "Line Type", self.line_types, index, default_value_int=1)
        self._assign_option(hname, self.dict[
                            hname], "LineColor", "Line Color", self.line_colors, index, default_value_int=color)
        self._assign_option(hname, self.dict[
                            hname], "LineSize", "Line Size", self.line_sizes, index, default_value_int=1)
        self._assign_option(hname, self.dict[
                            hname], "FillType", "Fill Type", self.fill_types, index, default_value_int=0)
        self._assign_option(hname, self.dict[
                            hname], "FillColor", "Fill Color", self.fill_colors, index, default_value_int=color)
        self._assign_option(hname, self.dict[hname], "RatioMarkerType", "Ratio Marker Type",
                            self.ratio_marker_types, index, default_value_int=self.dict[hname]["MarkerType"])
        self._assign_option(hname, self.dict[hname], "RatioMarkerColor", "Ratio Marker Color",
                            self.ratio_marker_colors, index, default_value_int=self.dict[hname]["MarkerColor"])
        self._assign_option(hname, self.dict[hname], "RatioMarkerSize", "Ratio Marker Size",
                            self.ratio_marker_sizes, index, default_value_int=self.dict[hname]["MarkerSize"])
        self._assign_option(hname, self.dict[hname], "RatioLineType", "Ratio Line Type",
                            self.ratio_line_types, index, default_value_int=self.dict[hname]["LineType"])
        self._assign_option(hname, self.dict[hname], "RatioLineColor", "Ratio Line Color",
                            self.ratio_line_colors, index, default_value_int=self.dict[hname]["LineColor"])
        self._assign_option(hname, self.dict[hname], "RatioLineSize", "Ratio Line Size",
                            self.ratio_line_sizes, index, default_value_int=self.dict[hname]["LineSize"])
        self._assign_option(hname, self.dict[hname], "RatioFillType", "Ratio Fill Type",
                            self.ratio_fill_types, index, default_value_int=self.dict[hname]["FillType"])
        self._assign_option(hname, self.dict[hname], "RatioFillColor", "Ratio Fill Color",
                            self.ratio_fill_colors, index, default_value_int=self.dict[hname]["FillColor"])

    # >>>
    # Read Input information
    # >>>
    def readInputs(self, dimension="1D"):

        # number of histograms
        histos = []
        # create dictionary and supporting variables
        firstname = ""

        # load histograms
        self.logger.info("Begin to load histograms")

        useoption = False
        if len(self.options) != 0:
            useoption = True

        if len(self.names) > len(self.legends) or len(self.names) > len(self.colors) or (useoption and len(self.names) > len(self.options)):
            self.logger.error(
                "Input array length short: <names> larger than <legends>,<colors>,<options>")
            sys.exit(-1)

        # if read from file
        if self.file != "":

            # Read file
            self.logger.info("Open root file: {0}".format(self.file))

            self.fin = TFile(self.file)
            if self.fin.IsZombie():
                self.logger.error("Failed to load root file")
                sys.exit(-1)

            # looping histogram names
            for index in range(len(self.names)):
                hname = self.names[index]
                temp = gDirectory.Get(hname)
                # if empty, raise error
                if temp.GetEntries() != -9999999.:
                    pass
                else:
                    self.logger.error("Failed to load this histogram")
                    sys.exit(-1)
                # add into list
                histos.append(temp)

        # if input histograms
        if len(self.list_histo) > 0:
            self.logger.info("Begin to load histograms from input list")
            histos = self.list_histo

        # setup
        for index in range(len(self.names)):

            # read options
            hname = self.names[index]
            self.readOptions(index)

            # logging
            self.logger.info(
                "Load histogram index {0}, name=\"{1}\"".format(index, hname))

            # histo
            temp = histos[index]

            # re-binning if requested
            if len(self.binning) != 0:
                # rebin for 1D histogram
                if dimension == "1D":
                    str_binning = ""
                    for bin in self.binning:
                        str_binning += "{0}".format(bin) + ","
                    self.logger.info(
                        "Rebinning 1D histogram to {0}".format(str_binning))
                    #temp = temp.Rebin(len(binning)-1, "{0}_rebin".format(hname), array.array('d',binning))
                    temp = self.rebinHisto1D(
                        hname=hname, histo=temp, binning=self.binning, bintype=self.bintype)
                # rebin for 2D histogram
                elif dimension == "2D":
                    self.logger.info("Rebinning 2D histograms")
                    temp = self.rebinHisto2D(
                        hname=hname, histo=temp, binning=self.binning, bintype=self.bintype)
                # other possibilities could also be initialized
                else:
                    pass

            if dimension == "1D":
                # calculate y axis maximum and minimum for plotting
                for i in range(temp.GetNbinsX()):
                    if temp.GetBinContent(i + 1) == 0:
                        continue
                    if self.min > temp.GetBinContent(i + 1):
                        self.min = temp.GetBinContent(
                            i + 1) - temp.GetBinError(i + 1)
                    if self.max < temp.GetBinContent(i + 1):
                        self.max = temp.GetBinContent(
                            i + 1) + temp.GetBinError(i + 1)
                        self.maxbin = i + 1
                self.logger.debug(
                    "Up to now, y-max={0}, y-min={1}".format(self.max, self.min))

            # if required reset the bin width to equal bin with and remake the
            # bin label
            temp2 = None
            if self.equalbin:
                # if 1D histogram
                if dimension == "1D":
                    nbins1D = temp.GetNbinsX()
                    name1D = temp.GetName()
                    temp2 = TH1F(name1D, name1D, nbins1D, 0, nbins1D)
                    for index1D in range(nbins1D):
                        content = temp.GetBinContent(index1D + 1)
                        error = temp.GetBinError(index1D + 1)
                        lowedge = temp.GetXaxis().GetBinLowEdge(index1D + 1)
                        highedge = temp.GetXaxis().GetBinLowEdge(index1D + 1) + \
                            temp.GetXaxis().GetBinWidth(index1D + 1)
                        temp2.SetBinContent(index1D + 1, content)
                        temp2.SetBinError(index1D + 1, error)
                        temp2.GetXaxis().SetBinLabel(
                            index1D + 1, "{0:.0f}-{1:.0f}".format(lowedge, highedge))
                        temp2.LabelsOption("u", "X")
                # if 2D histogram
                if dimension == "2D":
                    nbins2DX = temp.GetNbinsX()
                    nbins2DY = temp.GetNbinsY()
                    name2D = temp.GetName()
                    temp2 = TH2F(name2D, name2D, nbins2DX, 0,
                                 nbins2DX, nbins2DY, 0, nbins2DY)
                    for index2DX in range(nbins2DX):
                        for index2DY in range(nbins2DY):
                            content = temp.GetBinContent(
                                index2DX + 1, index2DY + 1)
                            error = temp.GetBinError(
                                index2DX + 1, index2DY + 1)
                            lowedgeX = temp.GetXaxis().GetBinLowEdge(index2DX + 1)
                            highedgeX = temp.GetXaxis().GetBinLowEdge(index2DX + 1) + \
                                temp.GetXaxis().GetBinWidth(index2DX + 1)
                            lowedgeY = temp.GetYaxis().GetBinLowEdge(index2DY + 1)
                            highedgeY = temp.GetYaxis().GetBinLowEdge(index2DY + 1) + \
                                temp.GetYaxis().GetBinWidth(index2DY + 1)
                            temp2.SetBinContent(
                                index2DX + 1, index2DY + 1, content)
                            temp2.SetBinError(
                                index2DX + 1, index2DY + 1, error)
                            temp2.GetXaxis.SetBinLabel(
                                index2DX + 1, "{0:.0f}-{1:.0f}".format(lowedgeX, highedgeX))
                            temp2.GetYaxis.SetBinLabel(
                                index2DY + 1, "{0:.0f}-{1:.0f}".format(lowedgeY, highedgeY))
                            temp2.LabelsOption("u", "X")
                            temp2.LabelsOption("u", "X")

            # add into dict.
            if self.equalbin:
                self.dict[hname]["HIST"] = temp2
            else:
                self.dict[hname]["HIST"] = temp

        # save the name of first histogram
        # will be the histogram with index-0
        self.firstname = self.names[0]
        self.firsthisto = self.dict[self.firstname]["HIST"]

        # get the histogram to be used as denominator
        self.denomname = self.names[0]
        for hname in self.names:
            if self.dict[hname]["DENOM"]:
                self.denomname = hname

        # if need to plot ratio, do it here
        for hname in self.names:
            if self.ratio != -1 and dimension == "1D" and hname != self.denomname and self.dict[hname]["DoRatio"]:
                newhist = self.dict[hname]["HIST"].Clone(hname + "_ratio")
                newhist.Divide(self.dict[self.denomname]["HIST"])
                self.dict[hname]["RATIO"] = newhist
                if self.firstratio is None:
                    self.firstratio = newhist
                    self.firstratio_name = hname
                # calculate y-axis maximum and minimum for ratio plot
                for i in range(newhist.GetNbinsX()):
                    if newhist.GetBinContent(i + 1) == 0:
                        continue
                    if self.rmin > (newhist.GetBinContent(i + 1) - newhist.GetBinError(i + 1)):
                        self.rmin = newhist.GetBinContent(
                            i + 1) - newhist.GetBinError(i + 1)
                    if self.rmax < (newhist.GetBinContent(i + 1) + newhist.GetBinError(i + 1)):
                        self.rmax = newhist.GetBinContent(
                            i + 1) + newhist.GetBinError(i + 1)
                self.logger.debug(
                    "Up to now, y-max-ratio={0}, y-min-ratio={1}".format(self.rmax, self.rmin))

        # put an end mark
        return

    # >>>
    # Plot 1D Histogram
    # >>>
    def plot1DHistogram(self):

        # Call various plotting segment functions to plot
        self.logger.info("Plot from file <{0}> and Output figure <{1}>".format(
            self.file, self.figname))

        # Read Histograms
        self.readInputs("1D")

        # Create Canvas
        self.setupCanvas()

        # Plot the histograms
        # loop the array and check one by one
        for index in range(len(self.names)):
            # read parameters and apply on drawing
            hname = self.names[index]
            histo = self.dict[hname]["HIST"]
            option = self.dict[hname]["OPT"]
            histo.SetLineStyle(self.dict[hname]["LineType"])
            histo.SetLineColor(self.dict[hname]["LineColor"])
            histo.SetLineWidth(self.dict[hname]["LineSize"])
            histo.SetMarkerStyle(self.dict[hname]["MarkerType"])
            histo.SetMarkerColor(self.dict[hname]["MarkerColor"])
            histo.SetMarkerSize(self.dict[hname]["MarkerSize"])
            histo.SetFillStyle(self.dict[hname]["FillType"])
            histo.SetFillColor(self.dict[hname]["FillColor"])

            self.logger.debug("Plot histogram: {0}".format(hname))
            # ratio or not
            if self.ratio == -1:
                self.MyC.cd()
            else:
                self.Pad1.cd()
            # draw main histogram
            if index == 0:
                histo.Draw(option)
            else:
                histo.Draw("{0}SAME".format(option))

            # if draw ratio plot
            if self.ratio != -1 and self.dict[hname]["DoRatio"] and hname != self.denomname:
                self.logger.debug("Plot ratio histogram: {0}".format(hname))
                optionII = self.dict[hname]["OptRatio"]
                self.Pad2.cd()
                histoII = self.dict[hname]["RATIO"]
                histoII.SetLineStyle(self.dict[hname]["RatioLineType"])
                histoII.SetLineColor(self.dict[hname]["RatioLineColor"])
                histoII.SetLineWidth(self.dict[hname]["RatioLineSize"])
                histoII.SetMarkerStyle(self.dict[hname]["RatioMarkerType"])
                histoII.SetMarkerColor(self.dict[hname]["RatioMarkerColor"])
                histoII.SetMarkerSize(self.dict[hname]["RatioMarkerSize"])
                histoII.SetFillStyle(self.dict[hname]["RatioFillType"])
                histoII.SetFillColor(self.dict[hname]["RatioFillColor"])
                if hname == self.firstratio_name:
                    histoII.Draw(optionII)
                else:
                    histoII.Draw("{0}SAME".format(optionII))

        # Draw Textual information
        self.drawTXT()

        # Draw Legends
        self.drawLegend()

        # Adjust Axis post drawing
        self.adjustAxis()

        # Output plots
        self.logger.info("Output plots")

        # Print to "png" file in linear scale
        # automatically optimize the histogram position on Canvas
        if self.maxbin * 1.0 > self.firsthisto.GetNbinsX() * 0.66:
            self.firsthisto.SetMaximum(2.2 * self.max)
        else:
            self.firsthisto.SetMaximum(1.5 * self.max)
        self.firsthisto.SetMinimum(0)
        # if force the maximum or minimum
        if self.force_max != -9999.:
            self.firsthisto.SetMaximum(self.force_max)
        if self.force_min != 1.e9:
            self.firsthisto.SetMinimum(self.force_min)

        self.MyC.Update()
        for type in self._figtype:
            self.MyC.Print(self.figname + "_linear.{0}".format(type))

        # Print to "png" file in log scale
        # automatically optimize the histogram position on Canvas
        if self.maxbin * 1.0 > self.firsthisto.GetNbinsX() * 0.66:
            self.firsthisto.SetMaximum(400 * self.max)
        else:
            self.firsthisto.SetMaximum(200 * self.max)
        # self.firsthisto.SetMinimum(1e-1)
        self.firsthisto.SetMinimum(1e-4)
        if self.ratio != -1:
            self.Pad1.SetLogy(1)
        else:
            self.MyC.SetLogy(1)
        # if force the maximum or minimum
        if self.force_max != -9999.:
            self.firsthisto.SetMaximum(self.force_max)
        if self.force_min != 1.e9:
            self.firsthisto.SetMinimum(self.force_min)

        self.MyC.Update()
        for type in self._figtype:
            self.MyC.Print(self.figname + "_log.{0}".format(type))

        # put an end mark
        return

    # >>>
    # Plot 2D Histogram
    # >>>
    def plot2DHistogram(self, normalize="NULL"):
        """
        normalize: normalize the 2D histogram on axis "X" or "Y", or do not normalize at all "NULL"
        For 2D histograms, if option="TEXT,COLZ" or similar combination delimited by comma, both options will be drawn
        """

        # Call various plotting segment functions to plot
        self.logger.info("Plot from file <{0}> and Output figure <{1}>".format(
            self.file, self.figname))

        # Read Histograms
        self.readInputs("2D")

        # Create Canvas
        self.setupCanvas()

        # Set Color Palette for 2D drawing
        gStyle.SetPalette(1)

        # Set Test format for 2D drawing
        gStyle.SetPaintTextFormat("3.2f")

        # Plot the histograms
        # loop the array and check one by one
        for index in range(len(self.names)):
            # read parameters
            hname = self.names[index]
            histo = self.dict[hname]["HIST"]
            # if request to normalize histogram on specific axis, do it here
            if normalize != "NULL":
                self.normalizeAxis(histo=histo, axis=normalize)
            color = self.dict[hname]["COLOR"]
            option = self.dict[hname]["OPT"]
            histo.SetLineColor(color)
            histo.SetMarkerColor(color)
            self.logger.debug("Plot histogram: {0}".format(hname))
            # draw 2D histogram
            # check if option combination is define
            option_list = option.split(",")
            for indexII in range(len(option_list)):
                option = option_list[indexII]
                if index == 0 and indexII == 0:
                    histo.Draw(option)
                else:
                    histo.Draw("{0}SAME".format(option))

        # Draw Textual information
        self.drawTXT()

        # Draw Legends
        self.drawLegend()

        # Adjust Axis post drawing
        self.adjustAxis()

        # Output plots
        self.logger.info("Output plots")

        # Print to "png" file in linear scale
        # Only need linear plot in 2D mode
        self.MyC.Update()
        self.MyC.Print(self.figname + "_linear.png")

        # put an end mark
        return

    # >>>
    # END
    # >>>
    def finish(self):

        # Close the file
        if self.fin:
            self.logger.info("Close the ROOT file")
            self.fin.Close()

        # Delete the logging stream
        self.logger.info("END of plotting")
        stream = self.logger.handlers[0]
        self.logger.removeHandler(stream)
        stream.flush()
        stream.close()

        # END
        return

    #####################
    # Auxiliary Functions
    #####################

    # functions:
    # >>>>>>
    # rebinHisto1D(), rebinHisto2D()
    # setupCanvas()
    # drawTXT()
    # drawLegend()
    # adjustAxis()
    # normalizeAxis()
    # <<<<<<

    # >>>
    # Rebin histograms 1D & 2D
    # >>>
    def rebinHisto1D(self, hname, histo, binning, bintype):
        # A small function to handle 1D histogram re-binning
        self.logger.debug("Start to rebin")

        # if bintype="Type1", binning is given as [nbins, low-bound, up-bound]
        # need to expand that to real binning so that consistent with "Type2"
        # arrays
        newbinning = []
        if bintype == "Type1":
            # check the binning array should have 3 elements
            if len(binning) != 3:
                self.logger.error(
                    "If Type1 bintype, need exact three element in array!")
                sys.exit(-1)
            # calculate bin width
            if binning[0] == 0:
                self.logger.error(
                    "If Type1 bintype, first element should be number of bins, cannot be zero!")
                sys.exit(-1)
            binwidth = (binning[2] - binning[1]) / binning[0]
            logger.debug("New bin width: {0}".format(binwidth))
            # re-fill binning
            newbinning.append(binning[1])
            for index in range(binning[0]):
                newbinning.append(binning[1] + (index + 1) * binwidth)
        else:
            newbinning = binning

        # rebin
        return histo.Rebin(len(newbinning) - 1, "{0}_rebin".format(hname), array.array('d', newbinning))

    def rebinHisto2D(self, hname, histo, binning, bintype):
        # A small function to handle 1D histogram re-binning
        self.logger.debug("Start to rebin")

        # 2D binning should be [ [x-axis binning], [y-axis binning] ]
        if len(binning) != 2:
            self.logger.error(
                "For 2D re-binning, input array should have two dimensions")
            sys.exit(-1)

        # if bintype="Type1", binning is given as [nbins, low-bound, up-bound]
        # need to expand that to real binning so that consistent with "Type2"
        # arrays
        newbinning = []
        if bintype == "Type1":
            # loop x, y components
            for index in len(binning):
                axis_binning = binning[index]
                axis_newbinning = []
                # check the binning array should have 3 elements
                if len(axis_binning) != 3:
                    self.logger.error(
                        "If Type1 bintype, need exact three element in array!")
                    sys.exit(-1)
                # calculate bin width
                if axis_binning[0] == 0:
                    self.logger.error(
                        "If Type1 bintype, first element should be number of bins, cannot be zero!")
                    sys.exit(-1)
                binwidth = (axis_binning[2] -
                            axis_binning[1]) / axis_binning[0]
                logger.debug("New bin width: {0}".format(binwidth))
                # re-fill binning
                axis_newbinning.append(binning[1])
                for indexII in range(binning[0]):
                    axis_newbinning.append(
                        binning[1] + (indexII + 1) * binwidth)
                # add into binning array
                newbinning.append(axis_newbinning)
        else:
            newbinning = binning

        # Rebin 2D histograms
        self.logger.debug("Create a new 2D histogram to adopt the new binning")

        # printouts for debug purposes
        nbinsX = len(newbinning[0]) - 1
        nbinsY = len(newbinning[1]) - 1
        str_binsX, str_binsY = "", ""
        for index in range(nbinsX):
            str_binsX += "{0}".format(newbinning[0][index]) + ","
        for indexII in range(nbinsY):
            str_binsY += "{0}".format(newbinning[1][index]) + ","
        self.logger.debug(
            "number of bins in X: {0}, binning: {1}".format(nbinsX, str_binsX))
        self.logger.debug(
            "number of bins in Y: {0}, binning: {1}".format(nbinsY, str_binsY))

        # create new histograms
        newhisto = TH2F("{0}_rebin".format(hname), "{0}_rebin".format(hname), nbinsX,
                        array.array('d', newbinning[0]), nbinsY, array.array('d', newbinning[1]))
        newhisto.Sumw2()

        # refill the new histograms with input one
        # need to take care of the underflow and the overflow bins
        # also try to treat the statistical uncertainties
        nbinsX_ori = histo.GetNbinsX()
        nbinsY_ori = histo.GetNbinsY()
        for index in range(nbinsX_ori + 2):
            for indexII in range(nbinsY_ori + 2):
                # get ori. bin centers
                bincenterx = histo.GetXaxis().GetBinCenter(index)
                bincentery = histo.GetYaxis().GetBinCenter(indexII)
                # get ori. bin content/error
                bincontent = histo.GetBinContent(index, indexII)
                binerror = histo.GetBinError(index, indexII)
                # find the bin number in new histogram
                newbin = newhisto.FindFixBin(bincenterx, bincentery)
                newcontent = bincontent + newhisto.GetBinContent(newbin)
                newerror = sqrt(pow(binerror, 2) +
                                pow(newhisto.GetBinError(newbin), 2))
                newhisto.SetBinContent(newbin, newcontent)
                newhisto.SetBinError(newbin, newerror)

        # return
        return newhisto

    # >>>
    # Setup the Canvas
    # >>>
    def setupCanvas(self):

        # setup ATLAS plotting style
        self.logger.info("Load ATLAS plotting style")

        atlas_style()

        # create canvas
        self.logger.info("Begin to define canvas")

        # If want ratio plot to be shown at the bottom, define its fraction
        # first
        if self.ratio <= 0:
            canvas_w, canvas_h = 800, 600
        elif self.ratio > 0:
            canvas_w, canvas_h = 800, int(600 * (1 + self.ratio))
        else:
            self.logger.error(
                "The scale of RATIO plot is wrongly defined: %.4f".format(self.ratio))
            sys.exit(-1)

        # Define canvas and create sub pad if needed
        gStyle.SetPadLeftMargin(0.15)
        gStyle.SetPadRightMargin(0.10)
        gStyle.SetPadTopMargin(0.06)
        gStyle.SetPadBottomMargin(0.15)
        self.MyC = TCanvas('MyC', 'MyC', canvas_w, canvas_h)
        self.MyC.SetTicks(1, 1)
        if self.ratio > 0:
            fraction = self.ratio + 0.2
            self.Pad1 = TPad("p1", "p1", 0, fraction * 1.0 /
                             (fraction + 1), 1, 1, 0, 0)  # x1,y1,x2,y2
            # left, right, bottom, top
            self.Pad1.SetMargin(0.15, 0.10, 0.03, 0.05)
            self.Pad2 = TPad("p2", "p2", 0, 0, 1, fraction *
                             1.0 / (fraction + 1), 0, 0)
            self.Pad2.SetMargin(0.15, 0.10, 0.15 / fraction, 0)
            self.Pad1.Draw()
            self.Pad2.Draw()
            self.Pad2.SetGrid()
            self.logger.info(
                "Canvas is defined as (width={0},height={1}): Ratio Plot Pad / Main Pad = {2:0.3f}".format(canvas_w, canvas_h, self.ratio))
        else:
            self.logger.info(
                "Canvas is defined as (width={0},height={1})".format(canvas_w, canvas_h))

        # put a end mark
        return

    # >>>
    # Draw Text and Luminosities, etc.
    # >>>
    def drawTXT(self):

        # This is a basic example, if needed should modify or extend this
        self.logger.info("Draw textual contents on Canvas")

        # Draw Text (lumi)(Part1)
        if self.ratio > 0:
            self.Pad1.cd()
        else:
            self.MyC.cd()
        self.t1 = TPaveText(0.17, 0.71, 0.18, 0.81, "NDC")
        self.t1.SetBorderSize(0)
        self.t1.SetFillColor(10)
        self.t1.SetTextColor(1)
        self.t1.SetTextSize(0.04)
        self.t1.SetTextAlign(22)
        self.t1.AddText('#int')
#        self.t1.Draw()
        # Draw Text (lumi)(Part2)
        self.t2 = TPaveText(0.18, 0.72, 0.41, 0.82, "NDC")
        self.t2.SetBorderSize(0)
        self.t2.SetFillColor(10)
        self.t2.SetTextColor(1)
        self.t2.SetTextSize(0.06)
        self.t2.SetTextAlign(12)
        self.t2.AddText(
            "Ldt = {0:.1f}fb^{{-1}}".format(self._lumi_in_pb / 1000.))
#        self.t2.Draw()
        # Draw Text (ATLAS )
        self.ta = TPaveText(0.17, 0.82, 0.41, 0.92, "NDC")
        self.ta.SetBorderSize(0)
        self.ta.SetFillColor(10)
        self.ta.SetTextColor(1)
        self.ta.SetTextSize(0.06)
        self.ta.SetTextAlign(12)
        self.ta.SetTextFont(72)
        self.ta.AddText(self._draw_text)
        self.ta.Draw()
        # Draw Text (CME)
        self.ta1 = TPaveText(0.17, 0.76, 0.41, 0.82, "NDC")
        self.ta1.SetBorderSize(0)
        self.ta1.SetFillColor(10)
        self.ta1.SetTextColor(1)
        self.ta1.SetTextSize(0.06)
        self.ta1.SetTextAlign(12)
        self.ta1.AddText('#sqrt{{s}}={0}'.format(self._center_mass_energy))
        self.ta1.Draw()

        # put a end mark
        return

    # >>>
    # Draw Legends
    # >>>
    def drawLegend(self):

        # Draw TLegend
        # Use number of entries to determine the y-size of legend automatically
        # currently use automatic

        self.logger.info("Draw legends")

        if self.ratio > 0:
            self.Pad1.cd()
        else:
            self.MyC.cd()

        nentries = len(self.names)
        if nentries < 7:
            self.lg = TLegend(0.6, 0.90 - 0.06 * nentries, 0.88, 0.90)
            self.lg.SetTextSize(0.05)
        else:
            self.lg = TLegend(0.60, 0.44, 0.85, 0.92)
            self.lg.SetTextSize(0.05 * 6 / nentries)
        self.lg.SetBorderSize(0)
        self.lg.SetFillColor(10)

        for index in range(len(self.names)):
            hname = self.names[index]
            histo = self.dict[hname]["HIST"]
            legend = self.dict[hname]["LEG"]
            self.lg.AddEntry(histo, legend, self.dict[hname]["OPT_Legend"])
        self.lg.Draw()

        # put an end mark
        return

    # >>>
    # Adjust Axis attributes post drawing
    # >>>
    def adjustAxis(self):

        # Adjust the axis titles
        self.logger.info("Setup axis titles and labels")

        self.firsthisto.GetYaxis().SetTitleSize(self._yaxis_title_size)
        self.firsthisto.GetYaxis().SetTitle(self.ytitle)
        self.firsthisto.GetYaxis().SetTitleOffset(self._yaxis_title_offset)
        self.firsthisto.GetXaxis().SetLabelSize(self._labelsize)
        self.firsthisto.GetYaxis().SetLabelSize(self._labelsize)
        if self.ratio == -1:
            self.firsthisto.GetXaxis().SetTitleSize(self._xaxis_title_size)
            self.firsthisto.GetXaxis().SetTitle(self.xtitle)
            self.firsthisto.GetXaxis().SetTitleOffset(self._xaxis_title_offset)
        if self.ratio > 0:
            fractionII = self.ratio + 0.2
            self.firstratio.GetXaxis().SetTitle(self.xtitle)
            self.firstratio.GetXaxis().SetTitleSize(
                self._xaxis_title_size * 1.0 / fractionII)
            self.firstratio.GetXaxis().SetTitleOffset(self._xaxis_title_offset)
            self.firstratio.GetYaxis().SetTitle(self.ratiotitle)
            self.firstratio.GetYaxis().SetTitleSize(
                self._yaxis_title_size * 1.0 / fractionII)
            self.firstratio.GetYaxis().SetTitleOffset(
                self._yaxis_title_offset * fractionII)
            self.firstratio.GetXaxis().SetLabelSize(
                self.firsthisto.GetLabelSize() * 1.0 / fractionII)
            self.firstratio.GetYaxis().SetLabelSize(
                self.firsthisto.GetLabelSize() * 1.0 / fractionII)
            if self.rmin < 0:
                self.rmin = 0
            if self.rmax > 2:
                self.rmax = 2
            self.firstratio.SetMinimum(self.rmin)
            self.firstratio.SetMaximum(self.rmax)
            # automatically adjust y axis stick intensity
            self.firstratio.GetYaxis().SetNdivisions(5 + 100 * 5)
            self.firsthisto.GetXaxis().SetLabelSize(0)

        self.MyC.Update()

        # put an end mark
        return

    # >>>
    # normalize Axis for 2D histogram
    # >>>
    def normalizeAxis(self, histo, axis="X"):
        # normalize the entries into axis "axis"
        # may be useful for correlation study
        self.logger.info("Normalize histogram on {0} axis".format(axis))

        # read the histogram and normalize
        nbinsX = histo.GetNbinsX()
        nbinsY = histo.GetNbinsY()
        # If normalize on X
        if axis == "X":
            for index in range(nbinsY):
                # for given y-bin, calculate integral on X:
                integralx = 0.
                for indexII in range(nbinsX):
                    integralx += histo.GetBinContent(indexII + 1, index + 1)
                # scale the bin content
                for indexII in range(nbinsX):
                    bincontent_ori = histo.GetBinContent(
                        indexII + 1, index + 1)
                    if integralx:
                        histo.SetBinContent(
                            indexII + 1, index + 1, bincontent_ori / integralx * 1.0)
        # If normalize on Y
        if axis == "Y":
            for index in range(nbinsX):
                # for given x-bin, calculate integral on Y:
                integraly = 0.
                for indexII in range(nbinsY):
                    integraly += histo.GetBinContent(index + 1, indexII + 1)
                # scale the bin content
                for indexII in range(nbinsY):
                    bincontent_ori = histo.GetBinContent(
                        index + 1, indexII + 1)
                    if integraly:
                        histo.SetBinContent(
                            index + 1, indexII + 1, bincontent_ori / integraly * 1.0)
        # put an end mark
        return
