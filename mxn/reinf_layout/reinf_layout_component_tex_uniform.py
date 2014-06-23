'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.


@author: rch
'''
from traits.api import \
    Float, Property, cached_property, Int, \
    Instance, Trait, on_trait_change, Button, \
    Str, Event

from traitsui.api import \
    View, Item, VGroup, Group

from mxn.reinf_laws import \
    ReinfLawBase, ReinfFabric

from reinf_layout_component import \
    ReinfLayoutComponent

from reinf_layout_component_tex_layer import \
    RLCTexLayer

from reinf_fabric_handler import \
    FabricHandler

from mxn.utils import \
    KeyRef

import numpy as np

STATE_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed'
STATE_LAW_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed,fabric_changed,law_changed,+law_input'

class RLCTexUniform(ReinfLayoutComponent):

    def __init__(self, *args, **metadata):
        '''Default value of fabric must be set here to ensure
        it has been set before an editor for it is requested
        '''
        setattr(self, 'fabric', 'default_fabric')
        self.add_trait('ecb_law', KeyRef(db=self.fabric_.named_mtrl_laws))
        self.on_trait_change(self._refresh_ecb_law, 'fabric')
        setattr(self, 'ecb_law', 'fbm')
        super(RLCTexUniform, self).__init__(**metadata)

    def _refresh_ecb_law(self):
        self.remove_trait('ecb_law')
        self.add_trait('ecb_law', KeyRef(db=self.fabric_.named_mtrl_laws))

    n_layers = Int(12, auto_set=False, enter_set=True, geo_input=True)
    '''total number of reinforcement layers [-]
    '''

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
    # Effective crack bridge law
    #===========================================================================


    fabric = KeyRef(db=ReinfFabric.db, law_input=True)

    fabric_changed = Event

#     ecb_law_type = Trait('fbm', ['fbm', 'cubic', 'linear', 'bilinear'], law_input=True)
#
#     ecb_law = Property(Instance(ReinfLawBase), depends_on='+law_input')
#     '''Effective crack bridge law corresponding to ecb_law_key'''
#     @cached_property
#     def _get_ecb_law(self):
#         law = self.fabric_.get_mtrl_law(self.ecb_law_type)
#         return law

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
            lst.append(RLCTexLayer(state=self.state, matrix_cs=self.matrix_cs,
                                     z_coord=self.z_ti_arr[i],
                                     ecb_law=self.ecb_law,
                                     fabric=self.fabric
                                     ))
        return lst

    @on_trait_change('eps_changed')
    def notify_eps_change(self):
        for i in range(self.n_layers):
            self.layer_lst[i].eps_changed = True

    @on_trait_change('fabric_changed')
    def notify_mat_change(self):
        self.law_changed = True

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

    #===========================================================================
    # UI-related functionality
    #===========================================================================

    node_name = 'Uniform textile layers'

    save_fabric = Button(label='Save current fabric')
    def _save_fabric_fired(self):
        self.fabric_.save()

    new_fabric = Button(label='Make new fabric')
    def _new_fabric_fired(self):
        pass

    del_fabric = Button(label='Delete current fabric')
    def _del_fabric_fired(self):
        pass

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
                      Item('n_layers'),
                      label='Geometry'
                      ),
                      Group(
                      Item('fabric'),
                      Item('ecb_law'),
                      Item('save_fabric', show_label=False),
                      Item('new_fabric', show_label=False),
                      Item('del_fabric', show_label=False),
                      label='Fabric material',
                      ),
                      springy=True,
                      ),
                resizable=True,
                handler=FabricHandler(),
                buttons=['OK', 'Cancel']
                )


if __name__ == '__main__':
    Layers = RLCTexUniform()
    Layers.configure_traits()
