#define vbfnlo_cxx
#include "vbfnlo.h"

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
#include <TStyle.h>
#include <TCanvas.h>

#include "TMVA/Factory.h"
#include "TMVA/Reader.h"

using namespace std;

// In this script, the BDT training results are read from the "weights" directory,
// and all the events are counted by looping through the ROOT trees based on the
// classification result of the BDT

//   In a ROOT session, you can do:
//      root> .L vbfnlo.cxx
//      root> vbfnlo t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries

void vbfnlo::Loop(string option)
{
        // if there is no file loaded, end the program
        if (fChain == 0) return;

        // the total number of entries of trees in all files in fChain
        // since there is only 1 file and therefore 1 tree,
        // nentries is the total number of entries of the tree
        Long64_t nentries = fChain->GetEntriesFast();

        // define the histogram with 100 bins ranging from -1 to 1
        TH1F* h1 = new TH1F("h1", "h1", 100, -1, 1);
        TH1F* h1 = new TH1F("h1", "h1", 100, -1, 1);

        // define the histograms for the following variables
        // zz_m, jj_m, z1_pt, z2_pt, delta_eta_jj
        // binning setting of histograms map referred from tree2hist.cxx
        TH1F* zz_m_hist = new TH1F("zz_m", "zz_m", 50, 0, 500);
        TH1F* jj_m_hist = new TH1F("jj_m", "jj_m", 50, 0, 3000);
        TH1F* z1_pt_hist = new TH1F("z1_pt", "z1_pt", 50, 0, 500);
        TH1F* z2_pt_hist = new TH1F("z2_pt", "z2_pt", 50, 0, 500);
        TH1F* delta_eta_jj_hist = new TH1F("delta_eta_jj", "delta_eta_jj", 40, 0, 10);

        // create a TMVA reader and suppress all output
        TMVA::Reader *reader = new TMVA::Reader("Silent");

        if (option=="dtop_dtop_jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj") {
                reader->AddVariable("jj_m",&jj_m);
                reader->AddVariable("zz_m",&zz_m);
                reader->AddVariable("z1_pt",&z1_pt);
                reader->AddVariable("z2_pt",&z2_pt);
                reader->AddVariable("delta_eta_jj",&delta_eta_jj);
                reader->BookMVA("BDT","weights/dtop_dtop_jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj.weights.xml");
        }

        if (option=="dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt") {
                reader->AddVariable("jj_m",&jj_m);
                reader->AddVariable("zz_m",&zz_m);
                reader->AddVariable("z1_pt",&z1_pt);
                reader->AddVariable("z2_pt",&z2_pt);
                reader->AddVariable("delta_eta_jj",&delta_eta_jj);
                reader->AddVariable("l1_pt",&l1_pt);
                reader->AddVariable("l2_pt",&l2_pt);
                reader->AddVariable("l3_pt",&l3_pt);
                reader->AddVariable("l4_pt",&l4_pt);
                reader->BookMVA("BDT","weights/dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt.weights.xml");
        }

        if (option=="dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal") {
                reader->AddVariable("jj_m",&jj_m);
                reader->AddVariable("zz_m",&zz_m);
                reader->AddVariable("z1_pt",&z1_pt);
                reader->AddVariable("z2_pt",&z2_pt);
                reader->AddVariable("delta_eta_jj",&delta_eta_jj);
                reader->AddVariable("l1_pt",&l1_pt);
                reader->AddVariable("l2_pt",&l2_pt);
                reader->AddVariable("l3_pt",&l3_pt);
                reader->AddVariable("l4_pt",&l4_pt);
                reader->BookMVA("BDT","weights/dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal.weights.xml");
        }

        // loop through all events
        for (Long64_t jentry=0; jentry<nentries; jentry++) {

                Long64_t ientry = LoadTree(jentry);
                Long64_t nb = fChain->GetEntry(jentry);

                if (ientry < 0) break;

                // if (jentry%1000 == 0) {
                //         cout << "for every 1000 entries" << endl;
                // }
                // cout << jj_m << endl;
                // cout << zz_m << endl;
                // cout << z1_pt << endl;
                // cout << z2_pt << endl;

                Double_t BDT_score = reader->EvaluateMVA("BDT");
                // cout << BDT_score << endl;

                // fill the histogram for each event
                h1->Fill(BDT_score);

                if (BDT_score > 0) {
                        zz_m_hist->Fill(zz_m);
                        jj_m_hist->Fill(jj_m);
                        z1_pt_hist->Fill(z1_pt);
                        z2_pt_hist->Fill(z2_pt);
                        delta_eta_jj_hist->Fill(delta_eta_jj);
                }
        }
        // save the histogram
        if (option=="dtop_dtop_jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj") {
                if (FILE_PATH=="/atlas/data19/zuguo/data/210_eeee_fid_preselected.root") {
                        TFile f("BDT_Signal_histogram_1.root","recreate");
                        h1 ->Write();
                        zz_m_hist->Write();
                        jj_m_hist->Write();
                        z1_pt_hist->Write();
                        z2_pt_hist->Write();
                        delta_eta_jj_hist->Write();
                        f.Close();
                }
                else if (FILE_PATH=="/atlas/data19/zuguo/data/3210_eeee_fid_preselected.root") {
                        TFile f("BDT_Background_histogram_1.root","recreate");
                        h1->Write();
                        zz_m_hist->Write();
                        jj_m_hist->Write();
                        z1_pt_hist->Write();
                        z2_pt_hist->Write();
                        delta_eta_jj_hist->Write();
                        f.Close();
                }

        }
        if (option=="dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt") {
                if (FILE_PATH=="/atlas/data19/zuguo/data/210_eeee_fid_preselected.root") {
                        TFile f("BDT_Signal_histogram_2.root","recreate");
                        h1->Write();
                        zz_m_hist->Write();
                        jj_m_hist->Write();
                        z1_pt_hist->Write();
                        z2_pt_hist->Write();
                        delta_eta_jj_hist->Write();
                        f.Close();
                }
                else if (FILE_PATH=="/atlas/data19/zuguo/data/3210_eeee_fid_preselected.root") {
                        TFile f("BDT_Background_histogram_2.root","recreate");
                        h1->Write();
                        zz_m_hist->Write();
                        jj_m_hist->Write();
                        z1_pt_hist->Write();
                        z2_pt_hist->Write();
                        delta_eta_jj_hist->Write();
                        f.Close();
                }
        }
        if (option=="dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal") {
                if (FILE_PATH=="/atlas/data19/zuguo/data/210_eeee_fid_preselected.root") {
                        TFile f("BDT_Signal_histogram_3.root","recreate");
                        h1->Write();
                        zz_m_hist->Write();
                        jj_m_hist->Write();
                        z1_pt_hist->Write();
                        z2_pt_hist->Write();
                        delta_eta_jj_hist->Write();
                        f.Close();
                }
                else if (FILE_PATH=="/atlas/data19/zuguo/data/3210_eeee_fid_preselected.root") {
                        TFile f("BDT_Background_histogram_3.root","recreate");
                        h1->Write();
                        zz_m_hist->Write();
                        jj_m_hist->Write();
                        z1_pt_hist->Write();
                        z2_pt_hist->Write();
                        delta_eta_jj_hist->Write();
                        f.Close();
                }
        }
}
