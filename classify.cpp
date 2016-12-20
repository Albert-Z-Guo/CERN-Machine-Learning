// reference: http://oproject.org/RMVA#C50

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVA/Factory.h"
#include "TMVA/Tools.h"

void classify(){

        // This loads the library
        TMVA::Tools::Instance();

        // Create a ROOT output file where TMVA will store ntuples, histograms, etc.
        TString outfileName( "TMVA.root" );
        TFile* outputFile = TFile::Open( outfileName, "RECREATE" );

        // Create the factory object. Later you can choose the methods
        // whose performance you'd like to investigate. The factory is
        // the only TMVA object you have to interact with

        // The first argument is the base of the name of all the
        // weightfiles in the directory weight/

        // The second argument is the output file for the training results
        // All TMVA output can be suppressed by removing the "!" (not) in
        // front of the "Silent" argument in the option string
        TMVA::Factory *factory = new TMVA::Factory( "RMVAClassification", outputFile,
                                                    "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );

        // Define the input variables that shall be used for the MVA training
        // note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
        // [all types of expressions that can also be parsed by TTree::Draw( "expression" )]
        factory->AddVariable("jj_m","mass of jj","", 'F');
        factory->AddVariable("zz_m","mass of zz", "", 'F');
        factory->AddVariable("z1_pt","transverse momentum of z1", "", 'F');
        factory->AddVariable("z2_pt","transverse momentum of z2", "", 'F');
        factory->AddVariable("delta_eta_jj","delta eta of jj", "", 'F');
        factory->AddVariable("l1_pt","transverse momentum of lepton 1", "", 'F');
        factory->AddVariable("l2_pt","transverse momentum of lepton 2", "", 'F');
        factory->AddVariable("l3_pt","transverse momentum of lepton 3", "", 'F');
        factory->AddVariable("l4_pt","transverse momentum of lepton 4", "", 'F');

        // You can add so-called "Spectator variables", which are not used in the MVA training,
        // but will appear in the final "TestTree" produced by TMVA. This TestTree will contain the
        // input variables, the response values of all trained MVAs, and the spectator variables
        // factory->AddSpectator( "spec1 := var1*2",  "Spectator 1", "units", 'F' );
        // factory->AddSpectator( "spec2 := var1*3",  "Spectator 2", "units", 'F' );

        // Read training and test data
        // (it is also possible to use ASCII format as input -> see TMVA Users Guide)
        TString file_1 = "/atlas/data19/zuguo/data/210_eeee_fid_preselected.root";
        TString file_2 = "/atlas/data19/zuguo/data/3210_eeee_fid_preselected.root";
        TFile *input_1 = TFile::Open( file_1 );
        TFile *input_2 = TFile::Open( file_2 );

        std::cout << "--- TMVAClassification       : Using input file: " << input_1->GetName() << std::endl;
        std::cout << "--- TMVAClassification       : Using input file: " << input_2->GetName() << std::endl;

        // Register the training and test trees
        TTree *tsignal     = (TTree*)input_1->Get("vbfnlo");
        TTree *tbackground = (TTree*)input_2->Get("vbfnlo");

        // global event weights per tree (see below for setting event-wise weights)
        Double_t signalWeight     = 1.0;
        Double_t backgroundWeight = 1.0;

        // You can add an arbitrary number of signal or background trees
        factory->AddSignalTree    ( tsignal,     signalWeight     );
        factory->AddBackgroundTree( tbackground, backgroundWeight );


        // Set individual event weights (the variables must exist in the original TTree)
        // factory->SetSignalWeightExpression    ("weight1*weight2");
        // factory->SetBackgroundWeightExpression("weight1*weight2");
        // factory->SetBackgroundWeightExpression( "weight" );

        // Tell the factory how to use the training and testing events
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

        // Apply additional cuts on the signal and background samples (can be different)
        TCut mycuta = ""; // for example: TCut mycuts = "abs(var1)<0.5 && abs(var2-0.5)<1";
        TCut mycutb = ""; // for example: TCut mycutb = "abs(var1)<0.5";

        factory->PrepareTrainingAndTestTree( mycuta, mycutb,
                                            "nTrain_Signal=69377:nTrain_Background=69377:nTest_Signal=140375:nTest_Background=46252:SplitMode=Random:NormMode=NumEvents:!V" );

        // Boosted Decision Trees
        // Gradient Boost
        factory->BookMethod(TMVA::Types::kBDT, "BDT_Gradient",
                            "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=5" );

        // Adaptive Boost
        factory->BookMethod(TMVA::Types::kBDT, "BDT_Adaptive",
                            "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=5:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );

        // Adaptive Boost + Decorrelation
        factory->BookMethod(TMVA::Types::kBDT, "BDT_Adaptive_Decorrelation",
                            "!H:!V:NTrees=500:MinNodeSize=5%:MaxDepth=5:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate" );

        // Adaptive Boost + Fisher discriminant in node splitting for (strong) linearly correlated variables
        factory->BookMethod(TMVA::Types::kBDT, "BDT_Adaptive_Fisher_discriminant",
                            "!H:!V:NTrees=50:MinNodeSize=2.5%:UseFisherCuts=True:MaxDepth=5:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" );

        // Bagging
        factory->BookMethod(TMVA::Types::kBDT, "BDT_Bagging",
                                                "!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20" );

        // Train MVAs using the set of training events
        factory->TrainAllMethods();

        // Evaluate all MVAs using the set of test events
        factory->TestAllMethods();

        // Evaluate and compare performance of all configured MVAs
        factory->EvaluateAllMethods();

        // Save the output
        outputFile->Close();

        std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
        std::cout << "==> TMVAClassification is done!" << std::endl;

        delete factory;
}
