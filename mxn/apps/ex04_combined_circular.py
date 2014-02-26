'''
Created on 2. 2. 2014

@author: Vancikv
'''

'''Circular concrete cross section with combined reinforcement
of textile layers and steel bars
'''

from mxn import \
    CrossSection, ReinfTexLayer, MatrixCrossSection, SteelBar, MCSGeoCirc
    
import numpy as np

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg
    
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

fig = Figure(figsize=(10,7),dpi=80,facecolor='white')
canvas = FigureCanvasAgg(fig)
ax = fig.add_subplot(1,1,1)
ge.plot_geometry(ax)
for i in range(len(cs.reinf)):
    cs.reinf[i].plot_geometry(ax)
canvas.print_figure('ex04.png')
