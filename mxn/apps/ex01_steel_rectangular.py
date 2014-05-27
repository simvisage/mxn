'''
Created on Jan 30, 2014

@author: rch
'''

'''Rectangular concrete cross section with steel reinforcement
'''

from mxn import \
    CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCSteelBar

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg
    
from mxn.utils import \
    get_outfile

bar = RLCSteelBar(x=0.1,z=0.45, area=0.0002)
'''Single steel reinforcement bar
'''

ge = MCSGeoRect(height=0.5, width=0.3)
'''Cross section geometry
'''

cs = CrossSection(reinf=[bar],
                         matrix_cs=MatrixCrossSection(geo=ge,
                                                      n_cj=20),
                         eps_lo=0.002,
                         eps_up=-0.0033
                         )

print 'normal force', cs.N
print 'moment', cs.M

fig = Figure(figsize=(10, 7), dpi=80, facecolor='white')
canvas = FigureCanvasAgg(fig)
ax = fig.add_subplot(1, 1, 1)
cs.plot_geometry(ax)

canvas.print_figure(get_outfile(folder_name='.mxn',
                                file_name='ex01.png'))
'''Saves a picture of cross section to a directory .mxn 
located in user's home directory
'''