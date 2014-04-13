'''
Created on 15. 2. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection
    
from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect
    
from mxn.reinf_layout import \
    RLCSteelBar, RLCTexLayer

import numpy as np
    
def test04_cross_section_mn():
    '''Test the moment and normal force calculated for a cross section.
    Rectangular cross section with spread textile reinforcement.
    '''
    tl1 = RLCTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.4)
    tl2 = RLCTexLayer(n_rovings=30, A_roving=0.5, z_coord=0.45)
    ge = MCSGeoRect(height=0.5, width=0.3)
    cs = CrossSection(reinf=[tl1, tl2],
                         matrix_cs=MatrixCrossSection(geo=ge,
                                        n_cj=20, cc_law_key = 'constant'),
                         eps_lo=0.008,
                         eps_up= -0.0033,
                         )
    
    assert np.allclose([cs.M, cs.N], [435.68614056664501, -2235.3491995963072])
    tl1.z_coord = 0.1
    assert np.allclose([cs.M, cs.N], [434.15077513204272, -2245.584969160323])
    ge.width = 0.15
    assert np.allclose([cs.M, cs.N], [218.70458852958842, -1114.6464797623262])
    cs.eps_lo = 0.014
    assert np.allclose([cs.M, cs.N], [159.47707057379949, -719.71876106187221])

if __name__ == '__main__':
    test04_cross_section_mn()
