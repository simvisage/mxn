'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.


@author: rch
'''
from etsproxy.traits.api import \
    Float, Property, cached_property, Int, Instance, Trait, on_trait_change

from etsproxy.traits.ui.api import \
    View, Item, VGroup, Group
    
from mxn.reinf_laws import \
    ReinfLawBase, ReinfLawLinear, ReinfLawFBM, ReinfLawCubic, ReinfLawBilinear

from reinf_layout_component import \
    ReinfLayoutComponent, \
    STATE_LAW_AND_GEOMETRY_CHANGE

from reinf_layout_component_tex_layer import \
    RLCTexLayer

from matresdev.db.simdb import \
    SimDBClassExt, SimDBClass

import numpy as np

class RLCTexUniform(ReinfLayoutComponent):

    node_name = 'Uniform textile layers'

    n_layers = Int(12, auto_set=False, enter_set=True, geo_input=True)
    '''total number of reinforcement layers [-]
    '''

    n_rovings = Int(23, auto_set=False, enter_set=True, geo_input=True)
    '''number of rovings in 0-direction of one composite layer of the
    bending test [-]:
    '''

    A_roving = Float(0.461, auto_set=False, enter_set=True, geo_input=True)
    '''cross section of one roving [mm**2]'''
    
    def convert_eps_tex_u_2_lo(self, eps_tex_u):
        '''Convert the strain in the lowest reinforcement layer at failure
        to the strain at the bottom of the cross section'''
        eps_up = self.state.eps_up
        height = self.matrix_cs.geo.height
        return eps_up + (eps_tex_u - eps_up) / self.z_ti_arr[0] * height

    def convert_eps_lo_2_tex_u(self, eps_lo):
        '''Convert the strain at the bottom of the cross section to the strain
        in the lowest reinforcement layer at failure'''
        eps_up = self.state.eps_up
        height = self.matrix_cs.geo.height
        return (eps_up + (eps_lo - eps_up) / height * self.z_ti_arr[0])
    
    #===========================================================================
    # Distribution of reinforcement
    #===========================================================================

    s_tex_z = Property(depends_on='+geo_input,matrix_cs.geo.changed')
    '''spacing between the layers [m]'''
    @cached_property
    def _get_s_tex_z(self):
        return self.matrix_cs.geo.height / (self.n_layers + 1)
        
    z_ti_arr = Property(depends_on='+geo_input,matrix_cs.geo.changed')
    '''property: distance of each reinforcement layer from the top [m]:
    '''
    @cached_property
    def _get_z_ti_arr(self):
        return np.array([ self.matrix_cs.geo.height - (i + 1) * self.s_tex_z
                         for i in range(self.n_layers) ],
                      dtype=float)

    zz_ti_arr = Property(depends_on='+geo_input,matrix_cs.geo.changed')
    '''property: distance of reinforcement layers from the bottom
    '''
    def _get_zz_ti_arr(self):
        return self.matrix_cs.geo.height - self.z_ti_arr
        
    #===========================================================================
    # Discretization conform to the tex layers
    #===========================================================================

    layer_lst = Property(depends_on='+geo_input,matrix_cs.geo.changed,+law_input')
    '''List of reinforcement layers
    '''
    @cached_property
    def _get_layer_lst(self):
        lst = []
        for i in range(self.n_layers):
            lst.append(RLCTexLayer(n_rovings=self.n_rovings, A_roving=self.A_roving, 
                                     state=self.state, matrix_cs=self.matrix_cs,
                                     z_coord=self.z_ti_arr[i],
                                     ecb_law_key = self.ecb_law_key
                                     ))
        return lst
    
    @on_trait_change('eps_changed')
    def notify_eps_change(self):
        for i in range(self.n_layers):
            self.layer_lst[i].eps_changed = True

    N = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        N = 0.
        for i in range(self.n_layers):
            N += self.layer_lst[i].N
        return N

    M = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting moment.
    '''
    @cached_property
    def _get_M(self):
        M = 0.
        for i in range(self.n_layers):
            M += self.layer_lst[i].M
        return M

    def plot_geometry(self, ax, clr='DarkOrange'):
        '''Plot geometry'''
        for i in range(self.n_layers):
            self.layer_lst[i].plot_geometry(ax, clr=clr)
            
    def plot_eps(self, ax):
        '''Plot strains'''
        for i in range(self.n_layers):
            self.layer_lst[i].plot_eps(ax)
    
    def plot_sig(self, ax):
        '''Plot stresses'''
        for i in range(self.n_layers):
            self.layer_lst[i].plot_sig(ax)
        
    tree_view = View(VGroup(
                      Group(
                      Item('n_rovings'),
                      Item('A_roving'),
                      Item('n_layers'),
                      label='Geometry'
                      ),
                      Group(
                      Item('ecb_law_key'),
                      label='Reinforcement law',
                      ),
                      springy=True,
                      ),
                resizable=True,
                buttons=['OK', 'Cancel']
                )

if __name__ == '__main__':
    Layers = RLCTexUniform()
    Layers.configure_traits()