'''
Created on 31. 1. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    Float, Property, cached_property, List

from etsproxy.traits.ui.api import \
    View, Item, VGroup

from constitutive_law import \
    ConstitutiveLawModelView

from reinf_layout_component import \
    ReinfLayoutComponent, \
    STATE_LAW_AND_GEOMETRY_CHANGE, \
    STATE_AND_GEOMETRY_CHANGE
    
import numpy as np

class RLCBar(ReinfLayoutComponent):
    '''base class for bar reinforcement
    '''

    position = List(Float, [0.1, 0.05], auto_set=False, enter_set=True, geo_input=True)
    '''position of the bar with respect to upper left 
    corner of reinforced cross section
    '''
    
    area = Float(0.0002, auto_set=False, enter_set=True, geo_input=True)
    '''area of the bar
    '''
    
    bar_coord_arr = Property(depends_on='position')
    def _get_bar_coord_arr(self):
        return np.array(self.position, dtype='f')
    
    z_up = Property(depends_on='position')
    '''vertical distance from upper rim of cross section
    '''
    @cached_property
    def _get_z_up(self):
        return self.bar_coord_arr[1]
    
    eps = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Strain of the bar
    '''
    @cached_property
    def _get_eps(self):
        # ------------------------------------------------------------------------                
        # geometric params independent from the value for 'eps_t'
        # ------------------------------------------------------------------------                
        height = self.matrix_cs.geo.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        # strain at the height of reinforcement bar [-]:
        #
        return eps_up + (eps_lo - eps_up) * self.z_up / height

    sig = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Stress of the bar
    '''
    @cached_property
    def _get_sig(self):
        return self.ecb_law.mfn.get_value(self.eps)

    f = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''force in the bar [kN]:
    '''
    @cached_property
    def _get_f(self):
        sig = self.sig
        A_bar = self.area
        return sig * A_bar * self.unit_conversion_factor

    N = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        return self.f

    M = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting moment.
    '''
    @cached_property
    def _get_M(self):
        return self.f * self.z_up

    def plot_geometry(self, ax):
        '''Plot geometry'''
        ax.plot(self.bar_coord_arr[0], self.matrix_cs.geo.height - self.bar_coord_arr[1], 'go')

    def plot_eps(self, ax):
        h = self.matrix_cs.geo.height
        ax.hlines([h-self.z_up], [0], [-self.eps], lw=4, color='green')

    def plot_sig(self, ax):
        h = self.matrix_cs.geo.height
        ax.hlines([h-self.z_up], [0], [-self.f], lw=4, color='green')

    view = View(VGroup(
                       Item('position', style = 'readonly'),
                       Item('area'),
                       label='Reinforcement Bar',
                       springy=True
                       ),
                       resizable=True,
                       buttons=['OK', 'Cancel']
                       )
    
if __name__ == '__main__':
    pass