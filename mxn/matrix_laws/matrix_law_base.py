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
    
from matresdev.db.simdb import \
    SimDBClass, SimDBClassExt

class MatrixLawBase(CLBase, MxNLeafNode, SimDBClass):
    '''Base class for concrete constitutive laws.'''
    # characteristic compressive stress [MPa]
    #
    f_ck = Float(60.0, simdb = True, enter_set = True, auto_set = False, input=True)
    eps_c_u = Float(0.0033, simdb = True, enter_set = True, auto_set = False, input=True)
    E_c = Float(28e+3, simdb = True, enter_set=True, auto_set=False, input=True)
    node_name = 'Constitutive law'

    high_strength_level = Float(50.0, simdb = True, enter_set=True, auto_set=False, input=True)

    eps_arr = Property(depends_on='+input')
    @cached_property
    def _get_eps_arr(self):
        return self.mfn.xdata

    sig_arr = Property(depends_on='+input')
    @cached_property
    def _get_sig_arr(self):
        return self.mfn.ydata

MatrixLawBase.db = SimDBClassExt(
            klass = MatrixLawBase,
            verbose = 'io',
            )

if __name__ == '__main__':
    MatrixLawBase.db.configure_traits()