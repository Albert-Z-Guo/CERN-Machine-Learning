//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Nov  1 09:22:50 2016 by ROOT version 6.04/14
// from TTree vbfnlo/vbfnlo
// found on file: 210_eeee_fid.root
//////////////////////////////////////////////////////////

#ifndef vbfnlo_h
#define vbfnlo_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
class vbfnlo {
public:
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         l1_pt;
   Float_t         l1_eta;
   Float_t         l1_phi;
   Float_t         l1_e;
   Float_t         l2_pt;
   Float_t         l2_eta;
   Float_t         l2_phi;
   Float_t         l2_e;
   Float_t         l3_pt;
   Float_t         l3_eta;
   Float_t         l3_phi;
   Float_t         l3_e;
   Float_t         l4_pt;
   Float_t         l4_eta;
   Float_t         l4_phi;
   Float_t         l4_e;
   Float_t         leadingj_pt;
   Float_t         leadingj_eta;
   Float_t         leadingj_phi;
   Float_t         leadingj_e;
   Float_t         subleadingj_pt;
   Float_t         subleadingj_eta;
   Float_t         subleadingj_phi;
   Float_t         subleadingj_e;
   Float_t         z1_pt;
   Float_t         z1_eta;
   Float_t         z1_phi;
   Float_t         z1_e;
   Float_t         z1_m;
   Float_t         z2_pt;
   Float_t         z2_eta;
   Float_t         z2_phi;
   Float_t         z2_e;
   Float_t         z2_m;
   Float_t         zz_pt;
   Float_t         zz_eta;
   Float_t         zz_phi;
   Float_t         zz_e;
   Float_t         zz_m;
   Float_t         jj_pt;
   Float_t         jj_eta;
   Float_t         jj_phi;
   Float_t         jj_e;
   Float_t         jj_m;
   Float_t         delta_R_ll_1;
   Float_t         delta_R_ll_2;
   Float_t         delta_R_zz;
   Float_t         delta_R_jj;
   Float_t         delta_R_zz_jj;
   Double_t        mcweight;
   Float_t         delta_eta_jj;
   Float_t         centrality;

   // List of branches
   TBranch        *b_l1_pt;   //!
   TBranch        *b_l1_eta;   //!
   TBranch        *b_l1_phi;   //!
   TBranch        *b_l1_e;   //!
   TBranch        *b_l2_pt;   //!
   TBranch        *b_l2_eta;   //!
   TBranch        *b_l2_phi;   //!
   TBranch        *b_l2_e;   //!
   TBranch        *b_l3_pt;   //!
   TBranch        *b_l3_eta;   //!
   TBranch        *b_l3_phi;   //!
   TBranch        *b_l3_e;   //!
   TBranch        *b_l4_pt;   //!
   TBranch        *b_l4_eta;   //!
   TBranch        *b_l4_phi;   //!
   TBranch        *b_l4_e;   //!
   TBranch        *b_leadingj_pt;   //!
   TBranch        *b_leadingj_eta;   //!
   TBranch        *b_leadingj_phi;   //!
   TBranch        *b_leadingj_e;   //!
   TBranch        *b_subleadingj_pt;   //!
   TBranch        *b_subleadingj_eta;   //!
   TBranch        *b_subleadingj_phi;   //!
   TBranch        *b_subleadingj_e;   //!
   TBranch        *b_z1_pt;   //!
   TBranch        *b_z1_eta;   //!
   TBranch        *b_z1_phi;   //!
   TBranch        *b_z1_e;   //!
   TBranch        *b_z1_m;   //!
   TBranch        *b_z2_pt;   //!
   TBranch        *b_z2_eta;   //!
   TBranch        *b_z2_phi;   //!
   TBranch        *b_z2_e;   //!
   TBranch        *b_z2_m;   //!
   TBranch        *b_zz_pt;   //!
   TBranch        *b_zz_eta;   //!
   TBranch        *b_zz_phi;   //!
   TBranch        *b_zz_e;   //!
   TBranch        *b_zz_m;   //!
   TBranch        *b_jj_pt;   //!
   TBranch        *b_jj_eta;   //!
   TBranch        *b_jj_phi;   //!
   TBranch        *b_jj_e;   //!
   TBranch        *b_jj_m;   //!
   TBranch        *b_delta_R_ll_1;   //!
   TBranch        *b_delta_R_ll_2;   //!
   TBranch        *b_delta_R_zz;   //!
   TBranch        *b_delta_R_jj;   //!
   TBranch        *b_delta_R_zz_jj;   //!
   TBranch        *b_mcweight;   //!
   TBranch        *b_delta_eta_jj;   //!
   TBranch        *b_centrality;   //!

   vbfnlo(TTree *tree=0);
   virtual ~vbfnlo();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(string option);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};
#endif

#ifdef vbfnlo_cxx

const char* FILE_PATH = "/atlas/data19/zuguo/data/210_eeee_fid_preselected.root";
// const char* FILE_PATH = "/atlas/data19/zuguo/data/3210_eeee_fid_preselected.root";

vbfnlo::vbfnlo(TTree *tree) : fChain(0)
{
  // if parameter tree is not specified (or zero), connect the file
  // used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject(FILE_PATH);
      if (!f || !f->IsOpen()) {
         f = new TFile(FILE_PATH);
      }
      f->GetObject("vbfnlo",tree);

   }
   Init(tree);
}

vbfnlo::~vbfnlo()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t vbfnlo::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t vbfnlo::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void vbfnlo::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("l1_pt", &l1_pt, &b_l1_pt);
   fChain->SetBranchAddress("l1_eta", &l1_eta, &b_l1_eta);
   fChain->SetBranchAddress("l1_phi", &l1_phi, &b_l1_phi);
   fChain->SetBranchAddress("l1_e", &l1_e, &b_l1_e);
   fChain->SetBranchAddress("l2_pt", &l2_pt, &b_l2_pt);
   fChain->SetBranchAddress("l2_eta", &l2_eta, &b_l2_eta);
   fChain->SetBranchAddress("l2_phi", &l2_phi, &b_l2_phi);
   fChain->SetBranchAddress("l2_e", &l2_e, &b_l2_e);
   fChain->SetBranchAddress("l3_pt", &l3_pt, &b_l3_pt);
   fChain->SetBranchAddress("l3_eta", &l3_eta, &b_l3_eta);
   fChain->SetBranchAddress("l3_phi", &l3_phi, &b_l3_phi);
   fChain->SetBranchAddress("l3_e", &l3_e, &b_l3_e);
   fChain->SetBranchAddress("l4_pt", &l4_pt, &b_l4_pt);
   fChain->SetBranchAddress("l4_eta", &l4_eta, &b_l4_eta);
   fChain->SetBranchAddress("l4_phi", &l4_phi, &b_l4_phi);
   fChain->SetBranchAddress("l4_e", &l4_e, &b_l4_e);
   fChain->SetBranchAddress("leadingj_pt", &leadingj_pt, &b_leadingj_pt);
   fChain->SetBranchAddress("leadingj_eta", &leadingj_eta, &b_leadingj_eta);
   fChain->SetBranchAddress("leadingj_phi", &leadingj_phi, &b_leadingj_phi);
   fChain->SetBranchAddress("leadingj_e", &leadingj_e, &b_leadingj_e);
   fChain->SetBranchAddress("subleadingj_pt", &subleadingj_pt, &b_subleadingj_pt);
   fChain->SetBranchAddress("subleadingj_eta", &subleadingj_eta, &b_subleadingj_eta);
   fChain->SetBranchAddress("subleadingj_phi", &subleadingj_phi, &b_subleadingj_phi);
   fChain->SetBranchAddress("subleadingj_e", &subleadingj_e, &b_subleadingj_e);
   fChain->SetBranchAddress("z1_pt", &z1_pt, &b_z1_pt);
   fChain->SetBranchAddress("z1_eta", &z1_eta, &b_z1_eta);
   fChain->SetBranchAddress("z1_phi", &z1_phi, &b_z1_phi);
   fChain->SetBranchAddress("z1_e", &z1_e, &b_z1_e);
   fChain->SetBranchAddress("z1_m", &z1_m, &b_z1_m);
   fChain->SetBranchAddress("z2_pt", &z2_pt, &b_z2_pt);
   fChain->SetBranchAddress("z2_eta", &z2_eta, &b_z2_eta);
   fChain->SetBranchAddress("z2_phi", &z2_phi, &b_z2_phi);
   fChain->SetBranchAddress("z2_e", &z2_e, &b_z2_e);
   fChain->SetBranchAddress("z2_m", &z2_m, &b_z2_m);
   fChain->SetBranchAddress("zz_pt", &zz_pt, &b_zz_pt);
   fChain->SetBranchAddress("zz_eta", &zz_eta, &b_zz_eta);
   fChain->SetBranchAddress("zz_phi", &zz_phi, &b_zz_phi);
   fChain->SetBranchAddress("zz_e", &zz_e, &b_zz_e);
   fChain->SetBranchAddress("zz_m", &zz_m, &b_zz_m);
   fChain->SetBranchAddress("jj_pt", &jj_pt, &b_jj_pt);
   fChain->SetBranchAddress("jj_eta", &jj_eta, &b_jj_eta);
   fChain->SetBranchAddress("jj_phi", &jj_phi, &b_jj_phi);
   fChain->SetBranchAddress("jj_e", &jj_e, &b_jj_e);
   fChain->SetBranchAddress("jj_m", &jj_m, &b_jj_m);
   fChain->SetBranchAddress("delta_R_ll_1", &delta_R_ll_1, &b_delta_R_ll_1);
   fChain->SetBranchAddress("delta_R_ll_2", &delta_R_ll_2, &b_delta_R_ll_2);
   fChain->SetBranchAddress("delta_R_zz", &delta_R_zz, &b_delta_R_zz);
   fChain->SetBranchAddress("delta_R_jj", &delta_R_jj, &b_delta_R_jj);
   fChain->SetBranchAddress("delta_R_zz_jj", &delta_R_zz_jj, &b_delta_R_zz_jj);
   fChain->SetBranchAddress("mcweight", &mcweight, &b_mcweight);
   fChain->SetBranchAddress("delta_eta_jj", &delta_eta_jj, &b_delta_eta_jj);
   fChain->SetBranchAddress("centrality", &centrality, &b_centrality);
   Notify();
}

Bool_t vbfnlo::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void vbfnlo::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t vbfnlo::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef vbfnlo_cxx
