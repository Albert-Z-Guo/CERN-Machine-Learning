// THis is the Top discriminator built based on BDT
// The TMVA classes are used
// 2013 Yusheng Wu

#include <iostream>
#include <vector>
#include <limits>
#include <map>

#include "TChain.h"
#include "TTree.h"
#include "TCut.h"
#include "TDirectory.h"
#include "TH1F.h"
#include "TH1.h"
#include "TMath.h"
#include "TFile.h"
#include "TROOT.h"

#include "TMVA/GeneticAlgorithm.h"
#include "TMVA/Factory.h"
#include "TMVA/Reader.h"

using namespace std;

class dtop {
    public:
            int init(vector<string> &files, vector<double> &weights, string sigorbkg);
            void train(string option);

    private:
            // the root files and weights for each samples; separated for signal and bkg
            map<string, double> _sigwt;
            map<string, double> _bkgwt;
            map<string, TTree *> _sigtree;
            map<string, TTree *> _bkgtree;
};
