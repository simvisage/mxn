'''
Created on 15. 2. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, SteelBar, MatrixCrossSection, GeoRect, ReinfTexLayer, GeoCirc

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg

import numpy as np
    
def test05_cross_section_mn():
    '''Test the moment and normal force calculated for a cross section.
    Circular cross section with mixed reinforcement.
    '''
    
    radius = 0.3
    ge = GeoCirc(radius=0.3)
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
        bar_lst.append(SteelBar(position=[x_bar_arr[i], z_bar_arr[i]], area=bar_area))
                       
    tl1 = ReinfTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.45)
    tl2 = ReinfTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.44)
    '''Two layers of textile reinforcement
    '''
    
    cs = CrossSection(reinf=[tl1, tl2] + bar_lst,
                             matrix_cs=MatrixCrossSection(geo=ge,
                                                             n_cj=20),
                             eps_lo=0.002,
                             eps_up= -0.0033,
                             )
    
    assert np.allclose([cs.M, cs.N], [1236.3684520623658, -9300.9390846971837])
    bar_lst[3].area = 0.0004
    assert np.allclose([cs.M, cs.N], [1261.0959216705535, -9400.9390846971837])
    ge.radius = 0.33
    assert np.allclose([cs.M, cs.N], [1642.5772498095203, -11306.262165932989])
    cs.eps_lo = 0.004
    assert np.allclose([cs.M, cs.N], [1677.4116782656272, -8055.6401549652082])
    
if __name__ == '__main__':
    test05_cross_section_mn()
