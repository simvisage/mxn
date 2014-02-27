'''
Created on 26. 2. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    Float, Property, cached_property

import numpy as np

from reinf_law_base import \
    ReinfLawBase
    
class ReinfLawSteel(ReinfLawBase):
    f_yk = Float(500, enter_set = True, auto_set = False, input = True)
    E_s = Float(200000, enter_set = True, auto_set = False, input = True)
    eps_s_u = Float(0.025, enter_set = True, auto_set = False, input = True)

    eps_s_y = Property(depends_on = '+input')
    @cached_property
    def _get_eps_s_y(self):
        return self.f_yk / self.E_s

    eps_arr = Property(depends_on = '+input')
    @cached_property
    def _get_eps_arr(self):
        return np.array([-self.eps_s_u, -self.eps_s_y, 0., self.eps_s_y, self.eps_s_u])

    sig_arr = Property(depends_on = '+input')
    @cached_property
    def _get_sig_arr(self):
        # with limit for eps_tex
        #
        return np.array([-self.f_yk, -self.f_yk, 0., self.f_yk, self.f_yk])
