'''
Created on 31. 1. 2014

@author: Vancikv
'''

from traits.api import \
    Float, Property, cached_property, \
    Int, Instance, Trait
    
from mxn.reinf_laws import \
    ReinfLawBase, ReinfLawLinear, ReinfLawFBM, \
    ReinfLawCubic, ReinfLawBilinear

from traitsui.api import \
    View, Item, VGroup, Group

from reinf_layout_component import \
    ReinfLayoutComponent, \
    STATE_LAW_AND_GEOMETRY_CHANGE, \
    STATE_AND_GEOMETRY_CHANGE

import numpy as np


class RLCTexLayer(ReinfLayoutComponent):
    '''single layer of textile reinforcement
    '''

    node_name = 'Textile layer'
    
    n_rovings = Int(23, auto_set=False, enter_set=True, geo_input=True)
    '''number of rovings in 0-direction of one composite layer of the
    bending test [-]:
    '''

    A_roving = Float(0.461, auto_set=False, enter_set=True, geo_input=True)
    '''cross section of one roving [mm**2]'''
    
    z_coord = Float(0.2, auto_set=False, enter_set=True, geo_input=True)
    '''distance of the layer from the top'''

    sig_tex_u = Float(1216., auto_set=False, enter_set=True,
                      law_input=True)
    '''Ultimate textile stress measured in the tensile test [MPa]
    '''
    #===========================================================================
    # Effective crack bridge law
    #===========================================================================
    ecb_law_type = Trait('fbm', dict(fbm=ReinfLawFBM,
                                  cubic=ReinfLawCubic,
                                  linear=ReinfLawLinear,
                                  bilinear=ReinfLawBilinear),
                      law_input=True)
    '''Selector of the effective crack bridge law type
    ['fbm', 'cubic', 'linear', 'bilinear']'''
    
    adapted_ecb_law = Instance(ReinfLawBase)

    ecb_law = Property(Instance(ReinfLawBase), depends_on='+law_input')
    '''Effective crack bridge law corresponding to ecb_law_type'''
    @cached_property
    def _get_ecb_law(self):
        if self.adapted_ecb_law:
            return self.adapted_ecb_law
        if self.ecb_law_type == 'linear':
            return self.ecb_law_type_(cs=self)
        else:
            return self.ecb_law_type_(sig_tex_u=self.sig_tex_u, cs=self)

    #===========================================================================
    # Discretization conform to the tex layers
    #===========================================================================

    eps = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Strain at the level of the reinforcement layer
    '''
    @cached_property
    def _get_eps(self):
        # ------------------------------------------------------------------------                
        # geometric params independent from the value for 'eps_t'
        # ------------------------------------------------------------------------                
        height = self.matrix_cs.geo.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        # strain at the height of each reinforcement layer [-]:
        #
        return eps_up + (eps_lo - eps_up) * self.z_coord / height

    eps_t = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Tension strain at the level of the layer of the fabrics
    '''
    @cached_property
    def _get_eps_t(self):
        return (np.fabs(self.eps) + self.eps) / 2.0

    eps_c = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Compression strain at the level of the layer.
    '''
    @cached_property
    def _get_eps_c(self):
        return (-np.fabs(self.eps) + self.eps) / 2.0

    sig_t = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Stresses at the i-th fabric layer.
    '''
    @cached_property
    def _get_sig_t(self):
        return self.ecb_law.mfn.get_value(self.eps_t)

    f_t = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''force at the height of reinforcement layer [kN]:
    '''
    @cached_property
    def _get_f_t(self):
        sig_t = self.sig_t
        n_rovings = self.n_rovings
        A_roving = self.A_roving
        return sig_t * n_rovings * A_roving / self.unit_conversion_factor
    
    N = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        return self.f_t
    
    M = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting moment.
    '''
    @cached_property
    def _get_M(self):
        return self.f_t * self.z_coord

    def plot_geometry(self, ax, clr='DarkOrange'):
        '''Plot geometry'''
        width = self.matrix_cs.geo.get_width(self.z_coord)
        w_max = self.matrix_cs.geo.width
        ax.hlines(self.matrix_cs.geo.height - self.z_coord, (w_max - width) / 2, 
                  (w_max + width) / 2, lw=2, color=clr, linestyle='dashed')

    def plot_eps(self, ax):
        h = self.matrix_cs.geo.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        
        # eps t
        ax.hlines([h-self.z_coord], [0], [-self.eps_t], lw=4, color='DarkOrange')

        # reinforcement layer
        ax.hlines([h-self.z_coord], [min(0.0, -eps_lo, -eps_up)], 
                  [max(0.0, -eps_lo, -eps_up)], lw=1, color='black', linestyle='--')

    def plot_sig(self, ax):
        h = self.matrix_cs.geo.height
        
        # sig t
        ax.hlines([h-self.z_coord], [0], [-self.f_t], lw=4, color='DarkOrange')
        
    tree_view = View(VGroup(
                      Group(
                      Item('n_rovings'),
                      Item('A_roving'),
                      Item('z_coord'),
                      label='Geometry'
                      ),
                      Group(
                      Item('sig_tex_u'),
                      Item('ecb_law_type'),
                      label='Reinforcement law',
                      ),
                      springy=True,
                      ),
                resizable=True,
                buttons=['OK', 'Cancel']
                )
    
if __name__ == '__main__':
    Layer = RLCTexLayer()
    Layer.configure_traits()
