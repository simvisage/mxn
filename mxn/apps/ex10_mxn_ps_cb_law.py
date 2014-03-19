'''
Created on 19. 3. 2014

@author: Vancik
'''

'''Parameter study of mxn diagram for textile 
reinforced concrete with different crack bridge laws
i.e. fbm and bilinear
'''

from mxn import \
    CrossSection, MxNDiagram, ECBCalib

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

from matplotlib.figure import \
    Figure

from matplotlib.backends.backend_agg import \
    FigureCanvasAgg
    
from mxn.utils import \
    get_outfile

ge = MCSGeoRect(height=0.06,width=0.14)
mcs = MatrixCrossSection(geo=ge,n_cj=20,f_ck=55.0,cc_law_type='constant')
uni_layers = RLCTexUniform(n_layers=12, n_rovings=16, A_roving=0.447,
                           sig_tex_u = 1200.13, ecb_law_type='fbm')
'''
N = 103 kN
sig_tex_u = N / A_tex_tot = 103000 / (12 * 16 * 0.447) = 1200.13 N/mm2
'''

cs = CrossSection(matrix_cs=mcs,reinf=[uni_layers])

calib = ECBCalib(cs=cs, Mu=2.45)
mxn = MxNDiagram(calib=calib,n_eps=20)

fig = Figure(figsize=(10, 7), dpi=80, facecolor='white')
canvas = FigureCanvasAgg(fig)
ax = fig.add_subplot(1, 1, 1)
mxn.plot_MN(ax)
uni_layers.ecb_law_type = 'bilinear'
mxn.plot_MN(ax)

canvas.print_figure(get_outfile(folder_name='.mxn',
                                file_name='ex10.png'))