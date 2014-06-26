'''
Created on 26. 2. 2014

@author: Vancikv
'''

from mxn import \
    ECBCalib, CrossSection, MxNDiagram

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

import numpy as np

def test_mxn_diagram():
    '''Test the calibrated crack bridge law.
    '''
    rf = RLCTexUniform(n_layers=12, material='default_fabric', material_law='fbm')
    rf.material_.set(s_0=0.0083, A_roving=0.461)

    mx = MatrixCrossSection(geo=MCSGeoRect(width=0.2, \
            height=0.06), n_cj=20, material='default_mixture', material_law='quadratic')
    cs1 = CrossSection(reinf=[rf], matrix_cs=mx)

    c = ECBCalib(Mu=3.49, cs=cs1)
    c.calibrated_ecb_law

    mn = MxNDiagram(cs=cs1, n_eps=5)
    assert np.allclose(mn.MN_arr, [[  8.46833921e-01, -8.36958790e-02, 4.99124621e-01,
         1.83590489e+00, 3.59406948e+00, 3.59406948e+00,
         5.43778492e+00, 4.74839849e+00, 4.06147239e+00,
         3.49000000e+00, 3.49000000e+00, 2.72230615e+00,
         1.71066701e+00, 8.52760158e-01, 4.10791170e-01,
         4.10791170e-01, 1.41195780e-01, 3.92268565e-02,
         3.98354193e-03, -8.88178420e-16],
        [ -7.01628255e+02, -7.59593651e+02, -7.26750551e+02,
        - 6.42677940e+02, -5.26283708e+02, -5.26283708e+02,
        - 2.26595623e+02, -1.06001638e+02, -4.07893660e+01,
         6.04373440e-10, 6.04373440e-10, 3.65172415e+01,
         7.90698984e+01, 1.13070827e+02, 1.30866035e+02,
         1.30866035e+02, 1.46191707e+02, 1.52386516e+02,
         1.54523035e+02, 1.54755994e+02]])

if __name__ == '__main__':
    test_mxn_diagram()
