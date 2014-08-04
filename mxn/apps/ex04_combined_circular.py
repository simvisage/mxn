'''
Created on 2. 2. 2014

@author: Vancikv
'''

'''Circular concrete cross section with combined
reinforcement of textile layers and steel bars
'''

from mxn.cross_section import \
    CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoCirc

from mxn.reinf_layout import \
    RLCTexLayer, RLCBar

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg

from mxn.utils import \
    get_outfile

import numpy as np

radius = 0.3
ge = MCSGeoCirc(radius=0.3)
'''Cross section geometry
'''

n_bars = 10
radius_bars = 0.26
'''Specifications of bar reinforcement
'''

fi_bar_arr = np.arange(0, 2 * np.pi, 2 * np.pi / n_bars,
                       dtype=float)
x_bar_arr = np.cos(fi_bar_arr) * radius_bars + radius
z_bar_arr = radius - np.sin(fi_bar_arr) * radius_bars
'''Positions of bars divided equally across the
circumference
'''

bar_lst = []
'''List of bars
'''
for i in range(n_bars):
    bar_lst.append(RLCBar(x=x_bar_arr[i],
                          z=z_bar_arr[i], material='bar_d10'))

tl1 = RLCTexLayer(z_coord=0.45)
tl2 = RLCTexLayer(z_coord=0.44)
'''Two layers of textile reinforcement
'''

cs = CrossSection(reinf=[tl1, tl2] + bar_lst,
                  matrix_cs=MatrixCrossSection(geo=ge,
                                               n_cj=20),
                  eps_lo=0.002,
                  eps_up=-0.0033,
                  )

print 'normal force', cs.N
print 'moment', cs.M

fig = Figure(figsize=(10, 7), dpi=80, facecolor='white')
canvas = FigureCanvasAgg(fig)
ax = fig.add_subplot(1, 1, 1)
cs.plot_geometry(ax)

canvas.print_figure(get_outfile(folder_name='.mxn',
                                file_name='ex04.png'))
