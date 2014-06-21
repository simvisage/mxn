'''
Created on 15. 2. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoCirc

from mxn.reinf_layout import \
    RLCSteelBar, RLCTexLayer

import numpy as np

def test_cross_section_mn():
    '''Test the moment and normal force calculated for a cross section.
    Circular cross section with mixed reinforcement.
    '''

    radius = 0.3
    ge = MCSGeoCirc(radius=0.3)
    '''Cross section geometry
    '''

    n_bars = 10
    radius_bars = 0.26
    bar_area = 0.0002
    '''Specifications of bar reinforcement
    '''

    fi_bar_arr = np.arange(0, 2 * np.pi, 2 * np.pi / n_bars, dtype=float)
    x_bar_arr = np.cos(fi_bar_arr) * radius_bars + radius
    z_bar_arr = radius - np.sin(fi_bar_arr) * radius_bars
    '''Positions of bars divided equally across the circumference
    '''

    bar_lst = []
    '''List of bars
    '''
    for i in range(n_bars):
        bar_lst.append(RLCSteelBar(x=x_bar_arr[i], z=z_bar_arr[i], area=bar_area))

    tl1 = RLCTexLayer(z_coord=0.45, ecb_law_type='fbm')
    tl2 = RLCTexLayer(z_coord=0.44, ecb_law_type='fbm')
    '''Two layers of textile reinforcement
    '''

    cs = CrossSection(reinf=[tl1, tl2] + bar_lst,
                             matrix_cs=MatrixCrossSection(geo=ge,
                                         n_cj=20, mm_key='default_mixture',
                                         cc_law_type='constant'),
                             eps_lo=0.002,
                             eps_up=-0.0033,
                             )

    tl1.ecb_law.set(sig_tex_u=1216., eps_u=0.014, m=0.5)
    tl1.fabric_.set(s_0=0.0247, A_roving=0.5)

    assert np.allclose([cs.M, cs.N], [1236.3684520623658, -9300.9390846971837])
    bar_lst[3].area = 0.0004
    assert np.allclose([cs.M, cs.N], [1261.0959216705535, -9400.9390846971837])
    ge.radius = 0.33
    assert np.allclose([cs.M, cs.N], [1633.4192537491854, -11401.438217633615])
    cs.eps_lo = 0.004
    assert np.allclose([cs.M, cs.N], [1518.3366590381993, -7292.1434236508921])

if __name__ == '__main__':
    test_cross_section_mn()
