'''
Created on 1. 2. 2014

@author: Vancikv
'''

'''rectangular concrete cross section with textile reinforcement input as single layers
'''

from mxn import \
    CrossSection
    
from matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from reinf_layout import \
    RLCTexLayer

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg
    
tl1 = RLCTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.4)
tl2 = RLCTexLayer(n_rovings=30, A_roving=0.5, z_coord=0.45)
'''Two layers of textile reinforcement
'''

ge = MCSGeoRect(height=0.5, width=0.3)
'''Cross section geometry
'''

cs = CrossSection(reinf=[tl1, tl2],
                         matrix_cs=MatrixCrossSection(geo=ge,
                                                         n_cj=20),
                         eps_lo=0.008,
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
canvas.print_figure('ex02.png')
