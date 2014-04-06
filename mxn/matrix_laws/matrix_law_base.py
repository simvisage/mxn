'''
Created on Aug 23, 2012

@author: rch
'''

from etsproxy.traits.api import \
    Float, Property, cached_property

import numpy as np

from constitutive_law import CLBase

from mxn.view import \
    MxNLeafNode

class MatrixLawBase(CLBase, MxNLeafNode):
    '''Base class for concrete constitutive laws.'''
    # characteristic compressive stress [MPa]
    #
    f_ck = Float(60.0, enter_set = True, auto_set = False, input=True)
    eps_c_u = Float(0.0033, enter_set = True, auto_set = False, input=True)
    E_c = Float(28e+3, enter_set=True, auto_set=False, input=True)
    node_name = 'Constitutive law'

    high_strength_level = Float(50.0, enter_set=True, auto_set=False, input=True)

    eps_arr = Property(depends_on='+input')
    @cached_property
    def _get_eps_arr(self):
        return self.mfn.xdata

    sig_arr = Property(depends_on='+input')
    @cached_property
    def _get_sig_arr(self):
        return self.mfn.ydata

if __name__ == '__main__':

    import pylab as p
    from constitutive_law import ConstitutiveLawModelView
    #cc_law = CCLawQuadratic(f_ck = 40.0, eps_c_u = 0.004)
    cc_law = CCLawQuad()
    print cc_law.mfn

    print cc_law.mfn_vct([0, 0.004, 0.01])

    colors = ['red', 'green', 'blue', 'orange', 'black', 'magenta', 'yellow']
    f_ck_arr = np.linspace(55, 85, 6)
    for f_ck, color in zip(f_ck_arr, colors):
        cc_law.f_ck = f_ck
        cc_law.mfn.plot(p, color=color, label='f_ck = %g' % f_ck)

    p.legend(loc=4)
    p.show()
