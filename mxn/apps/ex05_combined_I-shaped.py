'''
Created on 6. 2. 2014

@author: Vancikv
'''

'''I-shaped concrete cross section with combined reinforcement
of textile layers and steel bars
'''

from mxn import \
    CrossSection, ReinfTexLayer, MatrixCrossSection, SteelBar, MCSGeoI
    
import numpy as np

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg
    
ge = MCSGeoI(height=0.4, height_up=0.05, width_up=0.25, height_lo=0.05, width_lo=0.35, width_st=0.05)
mcs = MatrixCrossSection(geo=ge, n_cj=20)    
'''Cross section geometry + matrix
'''

bar1 = SteelBar(position=[0.025, 0.375], area=0.00005)
bar2 = SteelBar(position=[0.125, 0.375], area=0.00005)
bar3 = SteelBar(position=[0.225, 0.375], area=0.00005)
bar4 = SteelBar(position=[0.325, 0.375], area=0.00005)
'''Four steel reinforcement bars in lower flange
'''

tl1 = ReinfTexLayer(n_rovings=25, A_roving=0.5, z_coord=0.39)
tl2 = ReinfTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.01)
'''Two layers of textile reinforcement
'''

cs = CrossSection(reinf=[tl1, tl2, bar1, bar2, bar3, bar4],
                         matrix_cs=mcs,
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
canvas.print_figure('ex05.png')
