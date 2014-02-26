'''
Created on 2. 2. 2014

@author: Vancikv
'''

'''rectangular concrete cross section with combined reinforcement
of textile layers and steel bars
'''

from mxn import \
    CrossSection, ReinfTexLayer, MatrixCrossSection, SteelBar, MCSGeoRect

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg
    
tl1 = ReinfTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.39)
tl2 = ReinfTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.38)
'''Two layers of textile reinforcement
'''

bar1 = SteelBar(position=[0.1, 0.36], area=0.0002)
bar2 = SteelBar(position=[0.2, 0.36], area=0.0002)
bar3 = SteelBar(position=[0.1, 0.04], area=0.0002)
bar4 = SteelBar(position=[0.2, 0.04], area=0.0002)
'''Four steel reinforcement bars
'''

ge = MCSGeoRect(height=0.4, width=0.3)
'''Cross section geometry
'''

cs = CrossSection(reinf=[tl1, tl2, bar1, bar2, bar3, bar4],
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
canvas.print_figure('ex03.png')
