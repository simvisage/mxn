'''
Created on 31. 1. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Trait, Event, on_trait_change, Instance, Button, Callable, \
    DelegatesTo, Constant

from constitutive_law import \
    ConstitutiveLawModelView

from mxn.reinf_component import \
    ReinfComponent, \
    ECB_COMPONENT_CHANGE, \
    ECB_COMPONENT_AND_EPS_CHANGE

import numpy as np

class ReinfTexLayer(ReinfComponent):
    '''single layer of textile reinforcement
    '''

    n_rovings = Int(23, auto_set=False, enter_set=True, geo_input=True)
    '''number of rovings in 0-direction of one composite layer of the
    bending test [-]:
    '''

    A_roving = Float(0.461, auto_set=False, enter_set=True, geo_input=True)
    '''cross section of one roving [mm**2]'''
    
    z_coord = Float(0.2, auto_set=False, enter_set=True, geo_input=True)
    '''distance of the layer from the top'''

    sig_tex_u = Float(1216., auto_set=False, enter_set=True,
                      tt_input=True)
    '''Ultimate textile stress measured in the tensile test [MPa]
    '''

    #===========================================================================
    # Discretization conform to the tex layers
    #===========================================================================

    eps = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''Strain at the level of the reinforcement layer
    '''
    @cached_property
    def _get_eps(self):
        # ------------------------------------------------------------------------                
        # geometric params independent from the value for 'eps_t'
        # ------------------------------------------------------------------------                
        height = self.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        # strain at the height of each reinforcement layer [-]:
        #
        return eps_up + (eps_lo - eps_up) * self.z_coord / height

    eps_t = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''Tension strain at the level of the layer of the fabrics
    '''
    @cached_property
    def _get_eps_t(self):
        return (np.fabs(self.eps) + self.eps) / 2.0

    eps_c = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''Compression strain at the level of the layer.
    '''
    @cached_property
    def _get_eps_c(self):
        return (-np.fabs(self.eps) + self.eps) / 2.0

    sig_t = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''Stresses at the i-th fabric layer.
    '''
    @cached_property
    def _get_sig_t(self):
        return self.ecb_law.mfn_vct(self.eps_t)

    f_t = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''force at the height of reinforcement layer [kN]:
    '''
    @cached_property
    def _get_f_t(self):
        sig_t = self.sig_t
        n_rovings = self.n_rovings
        A_roving = self.A_roving
        return sig_t * n_rovings * A_roving / self.unit_conversion_factor

    def _get_N(self):
        return self.f_t

    def _get_M(self):
        return self.f_t * self.z_coord

    
    