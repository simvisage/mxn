'''
Created on 2. 4. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, MxNDiagram, ECBCalib

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

import numpy as np

import pylab as p

from matplotlib import rc
rc('font', **{'family':'sans-serif', 'sans-serif':['Helvetica']})
# # for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

eps_c_u = np.array([0.0022, 0.0033], dtype='f')
sig_tex_u = np.array([1216, 1565], dtype='f')
colors = np.array(['black', 'green', 'blue', 'red'])

def get_mxn(eps_c_u=0.0022, sig_tex_u=1216.0):
    ge = MCSGeoRect(height=0.06, width=0.2 * 5)
    mcs = MatrixCrossSection(geo=ge, n_cj=20, cc_law_type='linear')
    mcs.eps_c_u = float(eps_c_u)
    uni_layers = RLCTexUniform(n_layers=12, n_rovings=23 * 5, A_roving=0.446, ecb_law_type='fbm')
    uni_layers.ecb_law.sig_tex_u = float(sig_tex_u)
    cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])
    calib = ECBCalib(cs=cs, Mu=3.45 * 5)
    return MxNDiagram(calib=calib, n_eps=35)

get_vmxn = np.vectorize(get_mxn)
mxn_arr = get_vmxn(eps_c_u[:, np.newaxis], sig_tex_u[np.newaxis, :])

ax = p.subplot(1, 2, 1)
def plot_mxn(ax, mxn, color):
    label = r'$\varepsilon_{\mathrm{c,u}} = %g, \sigma_{\mathrm{tex,u}}$ = %g ' % (mxn.calib.cs.matrix_cs.eps_c_u,
                                                 mxn.calib.cs.reinf[0].ecb_law.sig_tex_u)
    mxn.plot_MN_custom(ax, color=color, linewidth=2, label=label)
    mxn.plot_eps(ax)

plot_vmxn = np.vectorize(plot_mxn)
# plot_vmxn = np.frompyfunc(plot_mxn, 3, 0)
plot_vmxn(ax, mxn_arr.flatten(), colors)
p.legend(loc=10)

ax = p.subplot(1, 2, 2)
def plot_ecb(ax, mxn, color):
    label = r'$\varepsilon_{\mathrm{c,u}} = %g, \sigma_{\mathrm{tex,u}}$ = %g ' % (mxn.calib.cs.matrix_cs.eps_c_u,
                                                 mxn.calib.cs.reinf[0].ecb_law.sig_tex_u)
    ecb_law = mxn.calib.calibrated_ecb_law
    ax.plot(ecb_law.eps_arr, ecb_law.sig_arr, lw=2, color=color, label=label)

# plot_vecb = np.frompyfunc(plot_ecb, 3, 0)
plot_vecb = np.vectorize(plot_ecb)
plot_vecb(ax, mxn_arr.flatten(), colors)

ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(b=None, which='major')
p.legend(loc=4)
p.show()