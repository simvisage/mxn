'''
Created on 15. 2. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection
    
from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect, MCSGeoI
    
from mxn.reinf_layout import \
    RLCSteelBar, RLCTexLayer

import numpy as np
    
def test06_cross_section_mn():
    '''Test the moment and normal force calculated for a cross section.
    I - shaped cross section with mixed reinforcement. Change of geometry
    to rectangular also tested.
    '''
    ge = MCSGeoI(height=0.4, height_up=0.05, width_up=0.25, height_lo=0.05, width_lo=0.35, width_st=0.05)
    mcs = MatrixCrossSection(geo=ge, n_cj=20)    
    '''Cross section geometry + matrix
    '''
    
    bar1 = RLCSteelBar(x=0.025,z=0.375, area=0.00005)
    bar2 = RLCSteelBar(x=0.125,z=0.375, area=0.00005)
    bar3 = RLCSteelBar(x=0.225,z=0.375, area=0.00005)
    bar4 = RLCSteelBar(x=0.325,z=0.375, area=0.00005)
    '''Four steel reinforcement bars in lower flange
    '''
    
    tl1 = RLCTexLayer(n_rovings=25, A_roving=0.5, z_coord=0.39)
    tl2 = RLCTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.01)
    '''Two layers of textile reinforcement
    '''
    
    cs = CrossSection(reinf=[tl1, tl2, bar1, bar2, bar3, bar4],
                             matrix_cs=mcs,
                             eps_lo=0.002,
                             eps_up= -0.0033,
                             )
    
    assert np.allclose([cs.M, cs.N], [201.85966110328661, -1149.8070885108996])
    bar1.area = 0.0004
    assert np.allclose([cs.M, cs.N], [220.03049443661996, -1032.9945885108996])
    ge.height_lo = 0.06
    assert np.allclose([cs.M, cs.N], [228.13663252701798, -1032.9945885108996])
    cs.eps_lo = 0.004
    assert np.allclose([cs.M, cs.N], [247.49122203, -843.661746225])
    mcs.geo = MCSGeoRect(height=0.4, width=0.4)
    assert np.allclose([cs.M, cs.N], [521.93902914533874, -3448.901578806112])
        
if __name__ == '__main__':
    test06_cross_section_mn()
