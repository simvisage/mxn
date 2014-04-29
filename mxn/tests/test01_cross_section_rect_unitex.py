'''
Created on Nov 21, 2013

@author: rch
'''

from mxn import \
    CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

import numpy as np

def test_cross_section_mn():
    '''Test the moment and normal force calculated for a cross section.
    '''
    cp = CrossSection(reinf=[RLCTexUniform(n_layers=3, ecb_law_key='fbm')],
                         matrix_cs=MatrixCrossSection(geo=MCSGeoRect(width=0.1, height=0.05),
                                                      n_cj=20, cc_law_type='constant', mm_key='default_mixture'),
                         eps_lo=0.014,
                         eps_up=-0.0033,
                         )

    cp.reinf_components_with_state[0].fabric.s_0 = 0.0043
    assert np.allclose([cp.M, cp.N], [1.14513592334, -22.1303533699])
    cp.reinf[0].n_layers = 5

    assert np.allclose([cp.M, cp.N], [1.29225385264, -6.60917224146])
    cp.eps_lo = 0.010

    assert np.allclose([cp.M, cp.N], [1.52939155655, -28.4691640432])

if __name__ == '__main__':
    test_cross_section_mn()
