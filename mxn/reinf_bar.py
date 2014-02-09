'''
Created on 31. 1. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Trait, Event, on_trait_change, Instance, Button, Callable, \
    DelegatesTo, Constant, WeakRef, List

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from etsproxy.traits.ui.api import \
    View, Item, Group, HSplit, VGroup, HGroup

from constitutive_law import \
    ConstitutiveLawModelView

from mxn.reinf_component import \
    ReinfComponent, \
    ECB_COMPONENT_CHANGE, \
    ECB_COMPONENT_AND_EPS_CHANGE
    
import numpy as np


class ReinfBar(ReinfComponent):
    '''base class for bar reinforcement
    '''

    position = List(Float, [0.1, 0.05], auto_set=False, enter_set=True, geo_input=True)
    '''position of the bar with respect to upper left 
    corner of reinforced cross section
    '''
    
    area = Float(0.0002, auto_set=False, enter_set=True, geo_input=True)
    '''area of the bar
    '''
    
    bar_coord_arr = Property(depends_on='+geo_input')
    def _get_bar_coord_arr(self):
        return np.array(self.position, dtype='f')
    
    z_up = Property(depends_on='+geo_input')
    '''vertical distance from upper rim of cross section
    '''
    @cached_property
    def _get_z_up(self):
        return self.bar_coord_arr[1]
    
    eps = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''Strain of the bar
    '''
    @cached_property
    def _get_eps(self):
        # ------------------------------------------------------------------------                
        # geometric params independent from the value for 'eps_t'
        # ------------------------------------------------------------------------                
        height = self.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        # strain at the height of reinforcement bar [-]:
        #
        return eps_up + (eps_lo - eps_up) * self.z_up / height

    sig = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''Stress of the bar
    '''
    @cached_property
    def _get_sig(self):
        return self.ecb_law.mfn.get_value(self.eps)

    f = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE)
    '''force in the bar [kN]:
    '''
    @cached_property
    def _get_f(self):
        sig = self.sig
        A_bar = self.area
        return sig * A_bar * self.unit_conversion_factor

    def _get_N(self):
        return self.f

    def _get_M(self):
        return self.f * self.z_up

    def plot_geometry(self, ax):
        '''Plot geometry'''
        ax.plot(self.bar_coord_arr[0], self.matrix_cs.geo.height - self.bar_coord_arr[1], 'ro')
       
class SteelBar(ReinfBar):
    '''Steel reinforcement bar
    '''
    ecb_law_type = 'steel'
    def _get_ecb_law(self):
        return self.ecb_law_type_(f_yk=500., E_s=200000., eps_s_u=0.025)
    
    