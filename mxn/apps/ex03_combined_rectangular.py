'''
Created on 2. 2. 2014

@author: Vancikv
'''

'''rectangular concrete cross section with combined reinforcement
of textile layers and steel bars
'''

from mxn.cross_section import \
    CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexLayer, RLCBar

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg

from mxn.utils import \
    get_outfile

tl1 = RLCTexLayer(z_coord=0.39, material='default_fabric', material_law='fbm')
tl2 = RLCTexLayer(z_coord=0.38, material='default_fabric')
'''Two layers of textile reinforcement
'''

bar1 = RLCBar(x=0.1, z=0.36, material='bar_d10')
bar2 = RLCBar(x=0.2, z=0.36, material='bar_d10')
bar3 = RLCBar(x=0.1, z=0.04, material='bar_d10')
bar4 = RLCBar(x=0.2, z=0.04, material='bar_d10')
'''Four steel reinforcement bars
'''

ge = MCSGeoRect(height=0.4, width=0.3)
'''Cross section geometry
'''

cs = CrossSection(reinf=[tl1, tl2, bar1, bar2, bar3, bar4],
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
                                file_name='ex03.png'))
