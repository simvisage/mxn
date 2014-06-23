'''
Created on 31. 1. 2014

@author: Vancikv
'''

from traits.api import \
    Float, Property, cached_property, \
    Int, Instance, Trait, on_trait_change, \
    Button, Event

from mxn.reinf_laws import \
    ReinfLawBase, ReinfLawLinear, ReinfLawFBM, \
    ReinfLawCubic, ReinfLawBilinear, ReinfFabric

from traitsui.api import \
    View, Item, VGroup, Group

from reinf_layout_component import \
    ReinfLayoutComponent

import numpy as np

from mxn.utils import \
    KeyRef

from reinf_fabric_handler import \
    FabricHandler

STATE_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed'
STATE_LAW_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed,fabric_changed,+law_input'

class RLCTexLayer(ReinfLayoutComponent):
    '''single layer of textile reinforcement
    '''

    def __init__(self, *args, **metadata):
        '''Default value of fabric must be set here to ensure
        it has been set before an editor for it is requested
        '''
        setattr(self, 'fabric', 'default_fabric')
        self.add_trait('ecb_law', KeyRef(db=self.fabric_.named_mtrl_laws))
        self.on_trait_change(self._refresh_ecb_law, 'fabric')
        setattr(self, 'ecb_law', 'fbm')
        super(RLCTexLayer, self).__init__(**metadata)

    def _refresh_ecb_law(self):
        self.remove_trait('ecb_law')
        self.add_trait('ecb_law', KeyRef(db=self.fabric_.named_mtrl_laws))

    z_coord = Float(0.2, auto_set=False, enter_set=True, geo_input=True)
    '''distance of the layer from the top'''

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

    @on_trait_change('fabric_changed')
    def notify_mat_change(self):
        self.law_changed = True

    #===========================================================================
    # Discretization conform to the tex layers
    #===========================================================================

    n_rovings = Property(depends_on='fabric_changed,matrix_cs.geo.changed')
    '''Number of rovings in the textile layer
    '''
    @cached_property
    def _get_n_rovings(self):
        return int(self.matrix_cs.geo.get_width(self.z_coord) / self.fabric_.s_0) - 1

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
        return self.ecb_law_.mfn.get_value(self.eps_t)

    f_t = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''force at the height of reinforcement layer [kN]:
    '''
    @cached_property
    def _get_f_t(self):
        sig_t = self.sig_t
        n_rovings = self.n_rovings
        A_roving = self.fabric_.A_roving
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

    #===========================================================================
    # UI-related functionality
    #===========================================================================

    node_name = 'Textile layer'

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
        width = self.matrix_cs.geo.get_width(self.z_coord)
        w_max = self.matrix_cs.geo.width
        ax.hlines(self.matrix_cs.geo.height - self.z_coord, (w_max - width) / 2,
                  (w_max + width) / 2, lw=2, color=clr, linestyle='dashed')

    def plot_eps(self, ax):
        h = self.matrix_cs.geo.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up

        # eps t
        ax.hlines([h - self.z_coord], [0], [-self.eps_t], lw=4, color='DarkOrange')

        # reinforcement layer
        ax.hlines([h - self.z_coord], [min(0.0, -eps_lo, -eps_up)],
                  [max(0.0, -eps_lo, -eps_up)], lw=1, color='black', linestyle='--')

    def plot_sig(self, ax):
        h = self.matrix_cs.geo.height

        # sig t
        ax.hlines([h - self.z_coord], [0], [-self.f_t], lw=4, color='DarkOrange')

    tree_view = View(VGroup(
                      Group(
                      Item('z_coord'),
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
    layer = RLCTexLayer()
    layer.fabric = 'default_fabric'
    layer.fabric_.A_roving = 0.5
    print layer.fabric_.state_link_lst
    layer.configure_traits()
