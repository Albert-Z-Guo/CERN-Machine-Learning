#include <iostream>
#include "dtop.h"

int main() {
    dtop *test  = new dtop();
    test->train("jj_m_zz_m_z1_pt_z2_pt_delta_eta_jj");
    test->train("jj_m_zz_m_z_pt_delta_eta_jj_l_pt");
    test->train("jj_m_zz_m_z_pt_delta_eta_jj_l_pt_optimal");
    return 0;
}
