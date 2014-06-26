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

def test_cross_section_mn():
    '''Test the moment and normal force calculated for a cross section.
    I - shaped cross section with mixed reinforcement. Change of geometry
    to rectangular also tested.
    '''
    ge = MCSGeoI(height=0.4, height_up=0.05, width_up=0.25, height_lo=0.05, width_lo=0.35, width_st=0.05)
    mcs = MatrixCrossSection(geo=ge, n_cj=20, mixture='default_mixture',
                             cc_law='constant')
    '''Cross section geometry + matrix
    '''

    bar1 = RLCSteelBar(x=0.025, z=0.375, area=0.00005)
    bar2 = RLCSteelBar(x=0.125, z=0.375, area=0.00005)
    bar3 = RLCSteelBar(x=0.225, z=0.375, area=0.00005)
    bar4 = RLCSteelBar(x=0.325, z=0.375, area=0.00005)
    '''Four steel reinforcement bars in lower flange
    '''

    tl1 = RLCTexLayer(z_coord=0.39, ecb_law='fbm')
    tl2 = RLCTexLayer(z_coord=0.01, ecb_law='fbm')
    '''Two layers of textile reinforcement
    '''

    cs = CrossSection(reinf=[tl1, tl2, bar1, bar2, bar3, bar4],
                             matrix_cs=mcs,
                             eps_lo=0.002,
                             eps_up=-0.0033,
                             )

    tl1.ecb_law_.set(sig_tex_u=1216., eps_u=0.014, m=0.5)
    tl1.fabric_.set(s_0=0.02, A_roving=0.461)

    assert np.allclose([cs.M, cs.N], [201.35521782599423, -1152.7647363907902])
    bar1.area = 0.0004
    assert np.allclose([cs.M, cs.N], [219.52605115932755, -1035.9522363907902])
    ge.height_lo = 0.06
    assert np.allclose([cs.M, cs.N], [227.65539856989415, -1035.9522363907902])
    cs.eps_lo = 0.004
    assert np.allclose([cs.M, cs.N], [246.77239163193633, -848.07965392270125])
    mcs.geo = MCSGeoRect(height=0.4, width=0.4)
    assert np.allclose([cs.M, cs.N], [521.32618671511852, -3452.1270652809549])

if __name__ == '__main__':
    test_cross_section_mn()
