#include "dtop.h"

int dtop::init(vector<string> &files, vector<double> &weights, string sigorbkg) {

        // check first the size of two inputs
        int size_files, size_wts, size_n;
        size_files = files.size();
        size_wts = files.size();
        if(size_files != size_wts) {
                cout<<"Input files and weights have different size: now quit!"<<endl;
                return -1;
        }
        size_n = size_files;

        // read files and put into maps
        for(int i=0; i<size_n; i++) {
                //open the file
                string nametag;
                TFile *tmpfile = new TFile(files.at(i).c_str());
                TTree *tmptree = (TTree*) gDirectory->Get("vbfnlo");
                if(sigorbkg=="sig") {
                        string name= Form("sig_%d",i);
                        _sigtree[name]=tmptree;
                        _sigwt[name]=weights.at(i);
                }
                if(sigorbkg=="bkg") {
                        string name= Form("bkg_%d",i);
                        _bkgtree[name]=tmptree;
                        _bkgwt[name]=weights.at(i);
                }
        }

        //done for the initialization
        return 0;
}

void dtop::train(string option) {

        // define vectors to be used
        vector<string> sigfiles, bkgfiles;
        vector<double> sigweights, bkgweights;

        // pile the paths of the root files and weights
        string file_path="/atlas/data19/zuguo/data";
        sigfiles.push_back(file_path + "/210_eeee_fid_preselected.root");
        sigweights.push_back(1);
        // sigfiles.push_back( file_path + "/" + "mc12_8TeV.126929.PowhegPythia8_AU2CT10_WpWm_me.merge.NTUP_SMWZ.e1280_s1469_s1470_r3542_r3549_p1328.listskim.root");
        // sigweights.push_back(20344.293376*1.0*1.0*0.62/178401.2000);

        bkgfiles.push_back(file_path + "/3210_eeee_fid_preselected.root");
        bkgweights.push_back(1);
        // bkgfiles.push_back(file_path + "/" + "mc12_8TeV.108343.McAtNloJimmy_AUET2CT10_SingleTopSChanWenu.merge.NTUP_SMWZ.e1242_s1469_s1470_r3542_r3549_p1328.listskim.root");
        // bkgweights.push_back(20344.293376*1.0*1.0*0.606/167513.6000);

        // initialize the root files, weights, signals and backgrounds...
        init(sigfiles, sigweights, "sig");
        init(bkgfiles, bkgweights, "bkg");

        //---------------------------------
        // start and initialize TMVA factory
        //---------------------------------
        // set the factory option
        // verbose flag: false
        // batch mode: false
        // transformations: decorrelation, Uniform and Gaussianisation, decorrelation transformations
        // analysis type: classification
        string factory_option = "!V:!Silent:Transformations=D;G,D:AnalysisType=Classification";

        // create the output file
        string ofname = option + "_dtop.root";
        TFile *ofile = new TFile(ofname.c_str(), "recreate");

        // set the constructor
        TMVA::Factory *factory = new TMVA::Factory("dtop", ofile, factory_option);

        // training options configuration
        // add variables
        if(option=="jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj") {
                factory->AddVariable("jj_m","jj_m","", 'F');
                factory->AddVariable("zz_m","zz_m", "", 'F');
                factory->AddVariable("z1_pt","z1_pt", "", 'F');
                factory->AddVariable("z2_pt","z2_pt", "", 'F');
                factory->AddVariable("delta_eta_jj","delta_eta_jj", "", 'F');
        }

        if(option=="jj_m_zz_m_z_pt_delta_eta_jj_l_pt") {
                factory->AddVariable("jj_m","jj_m","", 'F');
                factory->AddVariable("zz_m","zz_m", "", 'F');
                factory->AddVariable("z1_pt","z1_pt", "", 'F');
                factory->AddVariable("z2_pt","z2_pt", "", 'F');
                factory->AddVariable("delta_eta_jj","delta_eta_jj", "", 'F');
                factory->AddVariable("l1_pt","l1_pt", "", 'F');
                factory->AddVariable("l2_pt","l2_pt", "", 'F');
                factory->AddVariable("l3_pt","l3_pt", "", 'F');
                factory->AddVariable("l4_pt","l4_pt", "", 'F');
        }

        if(option=="jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal") {
                factory->AddVariable("jj_m","jj_m","", 'F');
                factory->AddVariable("zz_m","zz_m", "", 'F');
                factory->AddVariable("z1_pt","z1_pt", "", 'F');
                factory->AddVariable("z2_pt","z2_pt", "", 'F');
                factory->AddVariable("delta_eta_jj","delta_eta_jj", "", 'F');
                factory->AddVariable("l1_pt","l1_pt", "", 'F');
                factory->AddVariable("l2_pt","l2_pt", "", 'F');
                factory->AddVariable("l3_pt","l3_pt", "", 'F');
                factory->AddVariable("l4_pt","l4_pt", "", 'F');
        }

        // add signal trees and backgroud trees from the previously loaded map
        map<string, double>::iterator itr;
        for(itr=_sigwt.begin(); itr!=_sigwt.end(); itr++) {
                factory->AddSignalTree(_sigtree[(*itr).first], (*itr).second);
        }
        for(itr=_bkgwt.begin(); itr!=_bkgwt.end(); itr++) {
                factory->AddBackgroundTree(_bkgtree[(*itr).first], (*itr).second);
        }

        // specify the individual event weight
        // factory->SetWeightExpression("weight");

        // total events of output_tree_10000_210_eeee.root: 890100
        // total events of output_tree_10000_3210_eeee.root: 1014200

        // total events of 210_eeee_fid_preselected.root: 209752
        // total events of 3210_eeee_fid_preselected.root: 115629

        // use 60% of signals and backgrounds for training
        // training signals: 69377 = 0.6 * 115629
        // training backgrounds: 69377

        // use the remaining signals and backgrounds for testing
        // testing signals: 140375 = 209752 - 69377
        // testing backgrounds: 46252 = 115629 - 69377

        // no normalization and no pre-selection cut at the moment
        TCut preselcut="";
        factory->PrepareTrainingAndTestTree(preselcut,
                                            "nTrain_Signal=69377:nTrain_Background=69377:nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=None:!V");

        //---------
        // setup BDT
        //---------
        if(option=="jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj") {
                factory->BookMethod( TMVA::Types::kBDT, "dtop_"+option,"!H:!V:NTrees=500:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:MaxDepth=5" );
        }
        if(option=="jj_m_zz_m_z_pt_delta_eta_jj_l_pt") {
                factory->BookMethod( TMVA::Types::kBDT, "dtop_"+option,
                                     "!H:!V:NTrees=500:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:MaxDepth=5" );
        }
        if(option=="jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal") {
                factory->BookMethod( TMVA::Types::kBDT, "dtop_"+option,
                                     "!H:!V:NTrees=500:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=-1:MaxDepth=5" );
        }
        factory->TrainAllMethods();
        factory->TestAllMethods();
        factory->EvaluateAllMethods();

        // end the program
        return;
}
