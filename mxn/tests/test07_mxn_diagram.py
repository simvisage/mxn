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
    rf = RLCTexUniform(n_layers=12,ecb_law_type='fbm')
    mx = MatrixCrossSection(geo=MCSGeoRect(width=0.2, \
            height=0.06), n_cj=20, cc_law_type='quadratic')    
    cs1 = CrossSection(reinf = [rf], matrix_cs = mx)
    
    c = ECBCalib(Mu=3.49, cs = cs1)

    mn = MxNDiagram(calib=c, n_eps=5)
    assert np.allclose(mn.MN_arr, [[  8.46833921e-01,  -8.36958790e-02,   4.99124621e-01,
         1.83590489e+00,   3.59406948e+00,   3.59406948e+00,
         5.43778524e+00,   4.74839855e+00,   4.06147227e+00,
         3.48999976e+00,   3.48999976e+00,   2.72230593e+00,
         1.71066673e+00,   8.52759845e-01,   4.10790856e-01,
         4.10790856e-01,   1.41195617e-01,   3.92268048e-02,
         3.98353636e-03,   1.77635684e-15], 
        [ -7.01628255e+02,  -7.59593651e+02,  -7.26750551e+02,
        -6.42677940e+02,  -5.26283708e+02,  -5.26283708e+02,
        -2.26595590e+02,  -1.06001604e+02,  -4.07893377e+01,
         2.43245098e-05,   2.43245098e-05,   3.65172631e+01,
         7.90699210e+01,   1.13070849e+02,   1.30866056e+02,
         1.30866056e+02,   1.46191717e+02,   1.52386519e+02,
         1.54523036e+02,   1.54755994e+02]])

if __name__ == '__main__':
    test_mxn_diagram()
