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

ge = MCSGeoRect(height=0.02, width=0.1)
mcs = MatrixCrossSection(geo=ge, n_cj=20, f_ck=69, cc_law_type='linear')
mcs.eps_c_u = 0.0022
uni_layers = RLCTexUniform(n_layers=6, n_rovings=11, A_roving=0.446, ecb_law_type='fbm')
uni_layers.ecb_law.sig_tex_u = 2185.0

cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])

calib = ECBCalib(cs=cs, Mu=0.32)
mxn = MxNDiagram(calib=calib, n_eps=35)

import pylab as p
m, n = mxn.MN_arr
ax = p.subplot(1, 1, 1)
mxn.plot_MN_custom(ax, color='black', linewidth=2)
mxn.plot_eps(ax)
p.show()

ax = p.subplot(1, 1, 1)
ecb_law = mxn.calib.calibrated_ecb_law
ax.plot(ecb_law.eps_arr, ecb_law.sig_arr, lw=2, color='black')
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(b=None, which='major')
p.show()

mxn_view = MxNTreeView(root=mxn)
mxn_view.configure_traits()
