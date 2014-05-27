'''
Created on 2. 4. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, MxNDiagram, ECBCalib

from mxn.view import \
    MxNTreeView

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

ge = MCSGeoRect(height=0.06, width=0.2)
mcs = MatrixCrossSection(geo=ge, n_cj=20, cc_law_key='linear')
mcs.eps_c_u = 0.003
uni_layers = RLCTexUniform(n_layers=12, n_rovings=23, A_roving=0.446, ecb_law_key='fbm')
uni_layers.ecb_law.sig_tex_u = 1569.0

cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])

calib = ECBCalib(cs=cs, Mu=3.5)
mxn = MxNDiagram(calib=calib, n_eps=35)

import pylab as p
m, n = mxn.MN_arr
p.plot(m, -n, lw=2, color='black')

p.show()

mxn_view = MxNTreeView(root=mxn)
mxn_view.configure_traits()
