'''
Created on 26. 2. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    Float, Property, cached_property, Array, Int, List

from constitutive_law import CLBase

import numpy as np

from math import exp, log

from reinf_law_base import \
    ReinfLawBase
    
class ReinfLawBilinear(ReinfLawBase):
    '''Effective crack bridge Law using a cubic polynomial.'''

    sig_tex_u = Float(1250, input = True)
    eps_tex_u = Float(0.014, input = True)
    var_a = Float(50000, input = True)
    eps_el_fraction = Float(0.0001, input = True)

    cnames = ['eps_tex_u', 'var_a']

    u0 = List([ 0.014, 50000. ])

    eps_arr = Property(depends_on = '+input')
    @cached_property
    def _get_tex_arr(self):
        return np.hstack([0., self.eps_el_fraction * self.eps_tex_u, self.eps_tex_u ])

    sig_arr = Property(depends_on = '+input')
    @cached_property
    def _get_sig_arr(self):
        return np.hstack([0., self.var_a * self.sig_tex_u, self.sig_tex_u])
