'''
Created on 26. 2. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    Float, Property, cached_property, List

import numpy as np

from math import exp, log

from reinf_law_base import \
    ReinfLawBase
    
class ReinfLawFBM(ReinfLawBase):
    '''Effective crack bridge Law based on fiber-bundle-model.'''

    sig_tex_u = Float(1216., input = True)
    eps_u = Float(0.014, input = True)
    m = Float(0.5, input = True)

    cnames = ['eps_u', 'm']

    u0 = List([0.01266923, 0.5 ])

    eps_arr = Property(depends_on = '+input')
    @cached_property
    def _get_eps_arr(self):
        return np.linspace(0, self.eps_u, num = 100)

    sig_arr = Property(depends_on = '+input')
    @cached_property
    def _get_sig_arr(self):
        sig_tex_u = self.sig_tex_u
        eps_u = self.eps_u
        eps_arr = self.eps_arr
        m = self.m
        return (sig_tex_u / eps_u /
                exp(-pow(exp(-log(m) / m), 1.0 * m)) *
                eps_arr * np.exp(-np.power(eps_arr / eps_u * exp(-log(m) / m), 1.0 * m)))
