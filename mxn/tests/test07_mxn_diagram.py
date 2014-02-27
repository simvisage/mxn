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

    mn = MxNDiagram(calib=c, n_eps=5,)
    assert np.allclose(mn.MN_arr, [[ 0.84683392, -0.08369588,  0.49912462,  
                                   1.83590489,  3.59406948,
        3.59406948,  5.3586855 ,  4.68736596,  4.03655655,  3.49983508,
        3.49983508,  2.73737941,  1.74260919,  0.90059919,  0.47082758,
        0.47082758,  0.19336894,  0.07043817,  0.01662683,  0.        ], 
        [-701.62825504, -759.59365112, -726.75055052, -642.6779403 ,
       -526.2837081 , -526.2837081 , -231.70594128, -112.83119169,
        -47.3257649 ,   -5.72510225,   -5.72510225,   30.75068698,
         72.75903022,  106.38325184,  123.9998091 ,  123.9998091 ,
        140.97566794,  149.2686308 ,  153.22360342,  154.6231108 ]])

if __name__ == '__main__':
    test_mxn_diagram()
