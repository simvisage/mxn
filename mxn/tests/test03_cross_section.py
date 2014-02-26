'''
Created on 15. 2. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection
    
from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect
    
from mxn.reinf_layout import \
    RLCSteelBar

import numpy as np

def test03_cross_section_mn():
    '''Test the moment and normal force calculated for a cross section. 
    Rectangular cross section with steel reinforcement.
    '''
    
    bar = RLCSteelBar(position=[0.1, 0.45], area=0.0002)
    ge = MCSGeoRect(height=0.5, width=0.3)
    cs = CrossSection(reinf=[bar],
                         matrix_cs=MatrixCrossSection(geo=ge,
                                                         n_cj=20),
                         eps_lo=0.002,
                         eps_up= -0.0033,
                         )
    
    assert np.allclose([cs.M, cs.N], [605.63085424909093, -4763.6924315440474])
    bar.position = [0.15, 0.35]
    assert np.allclose([cs.M, cs.N], [595.51085561046102, -4806.0924290168105])
    cs.eps_lo = 0.010
    assert np.allclose([cs.M, cs.N], [393.29047407596528, -1821.7451022853184])

if __name__ == '__main__':
    test03_cross_section_mn()
