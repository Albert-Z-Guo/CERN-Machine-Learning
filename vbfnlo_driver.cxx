#include "vbfnlo.cxx"

int vbfnlo_driver() {
        vbfnlo *t  = new vbfnlo();
        // t->Loop("dtop_dtop_jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj");
        // t->Loop("dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt");
        t->Loop("dtop_dtop_jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal");
        return 0;
}
