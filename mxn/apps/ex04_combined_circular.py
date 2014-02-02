'''
Created on 2. 2. 2014

@author: Vancikv
'''

'''Circular concrete cross section with combined reinforcement
of textile layers and steel bars
'''

from mxn import \
    CrossSection, ReinfTexLayer, MatrixCrossSection, SteelBar, GeoCirc
    
import numpy as np
    
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
x_bar_arr = np.cos(fi_bar_arr) * (radius - radius_bars) + radius
z_bar_arr = radius - np.sin(fi_bar_arr) * (radius - radius_bars)
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

cs = CrossSection(reinf=[tl1, tl2]+bar_lst,
                         matrix_cs=MatrixCrossSection(geo=ge,
                                                         n_cj=20),
                         eps_lo=0.002,
                         eps_up= -0.0033,
                         )

print 'normal force', cs.N
print 'moment', cs.M
print 'sigma_layer1', tl1.sig_t
print 'sigma_bar1', bar_lst[0].sig
print 'sigma_bar3', bar_lst[2].sig