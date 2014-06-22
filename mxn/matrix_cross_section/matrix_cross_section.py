'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.

@author: rch
'''
from traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Event, on_trait_change, Callable, Instance, Trait, \
    Button, List, Str, Event

from matrix_cross_section_geo import \
    MCSGeo

from matrix_cross_section_geo_I import \
    MCSGeoI

from matrix_cross_section_geo_circ import \
    MCSGeoCirc

from matrix_cross_section_geo_rect import \
    MCSGeoRect

from matplotlib.figure import \
    Figure

from traitsui.api import \
    View, Item, Group, HSplit, VGroup, HGroup, InstanceEditor

from mxn.matrix_laws import \
    MatrixMixture

from matresdev.db.simdb import \
    SimDBClass

from mxn import \
    CrossSectionComponent

import numpy as np

from mxn.utils import \
    KeyRef

STATE_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,geo.changed'
STATE_LAW_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,geo.changed,+law_input,law_changed,cc_law.+input,mixture_changed'

class MatrixCrossSection(CrossSectionComponent):
    '''Cross section characteristics needed for tensile specimens.
    '''
    def __init__(self, *args, **metadata):
        '''Default value of mixture must be set here to ensure
        it has been set before an editor for it is requested
        '''
        setattr(self, 'mixture', 'default_mixture')
        super(MatrixCrossSection, self).__init__(**metadata)

    n_cj = Float(30, auto_set=False, enter_set=True, geo_input=True)
    '''Number of integration points.
    '''

    x = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Height of the compressive zone
    '''
    @cached_property
    def _get_x(self):
        height = self.geo.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        if eps_up <= 0 and eps_lo <= 0:
            return height
        elif eps_up == eps_lo:
            return 0.
        else:
            return (abs(eps_up) / (abs(eps_up - eps_lo)) * height)

    z_ti_arr = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Discretizaton of the  compressive zone
    '''
    @cached_property
    def _get_z_ti_arr(self):
        if self.state.eps_up <= 0:  # bending
            zx = min(self.geo.height, self.x)
            return np.linspace(0, zx, self.n_cj)
        elif self.state.eps_lo <= 0:  # bending
            return np.linspace(self.x, self.geo.height, self.n_cj)
        else:  # no compression
            return np.array([0], dtype='f')

    eps_ti_arr = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Compressive strain at each integration layer of the compressive zone [-]:
    '''
    @cached_property
    def _get_eps_ti_arr(self):
        # for calibration us measured compressive strain
        # @todo: use mapped traits instead
        #
        height = self.geo.height
        eps_up = self.state.eps_up
        eps_lo = self.state.eps_lo
        eps_j_arr = (eps_up + (eps_lo - eps_up) * self.z_ti_arr /
                     height)
        return (-np.fabs(eps_j_arr) + eps_j_arr) / 2.0

    zz_ti_arr = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Distance of discrete slices of compressive zone from the bottom
    '''
    @cached_property
    def _get_zz_ti_arr(self):
        return self.geo.height - self.z_ti_arr

    #===========================================================================
    # Cross section geometry and related parameters
    #===========================================================================

    geo = Instance(MCSGeo)
    '''Geometry of the cross section
    '''
    def _geo_default(self):
        return MCSGeoRect(height=0.06, width=0.2)

    geo_lst = Property()
    @cached_property
    def _get_geo_lst(self):
        lst = [MCSGeoRect(), MCSGeoCirc(), MCSGeoI()]
        for i in range(len(lst)):
            if lst[i].__class__ == self.geo.__class__:
                lst[i] = self.geo
        return lst

    w_ti_arr = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Discretization of the  compressive zone - weight factors for general cross section
    '''
    @cached_property
    def _get_w_ti_arr(self):
        return self.geo.width_vct(self.z_ti_arr)

    #===========================================================================
    # Compressive concrete constitutive law
    #===========================================================================

    mixture = KeyRef(db=MatrixMixture.db, law_input=True)

    mixture_changed = Event

    cc_law_types = Property(depends_on='mixture')
    @cached_property
    def _get_cc_law_types(self):
        return self.mixture_.mtrl_laws.keys()

    cc_law_type = Trait('quadratic', ['constant', 'quadratic', 'quad',
                                      'linear', 'bilinear'], law_input=True)

    cc_law = Property(depends_on='+law_input,mixture_changed')
    @cached_property
    def _get_cc_law(self):
        return self.mixture_.get_mtrl_law(self.cc_law_type)

    @on_trait_change('cc_law.+input,mixture_changed')
    def notify_law_change(self):
        self.law_changed = True

    #===========================================================================
    # Calculation of compressive stresses and forces
    #===========================================================================

    sig_ti_arr = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Stresses at the j-th integration point.
    '''
    @cached_property
    def _get_sig_ti_arr(self):
        return -self.cc_law.mfn_vct(-self.eps_ti_arr)

    f_ti_arr = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Layer force corresponding to the j-th integration point.
    '''
    @cached_property
    def _get_f_ti_arr(self):
        return self.w_ti_arr * self.sig_ti_arr * self.unit_conversion_factor

    N = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        return np.trapz(self.f_ti_arr, self.z_ti_arr)

    M = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting moment evaluated with respect to the center line
    '''
    @cached_property
    def _get_M(self):
        return np.trapz(self.f_ti_arr * self.z_ti_arr, self.z_ti_arr)

    #===============================================================================
    # Plotting functions
    #===============================================================================

    def plot_eps(self, ax):
        h = self.geo.height

        # eps ti
        ec = np.hstack([self.eps_ti_arr] + [0, 0])
        zz = np.hstack([self.zz_ti_arr] + [0, h ])
        ax.fill(-ec, zz, color='DodgerBlue')

    def plot_sig(self, ax):
        h = self.geo.height

        # sig ti
        ec = np.hstack([self.f_ti_arr * self.x / self.n_cj] + [0, 0])
        zz = np.hstack([self.zz_ti_arr] + [0, h ])
        ax.fill(-ec, zz, color='DodgerBlue')

    def plot(self, fig):
        '''Plots the geometry + concrete law
        '''
        ax1 = fig.add_subplot(1, 2, 1)
        self.geo.plot_geometry(ax1)
        ax2 = fig.add_subplot(1, 2, 2)
        self.cc_law.plot_ax(ax2)

    #===========================================================================
    # Auxiliary methods for tree editor
    #===========================================================================
    node_name = 'Matrix cross section'

    tree_node_list = Property(depends_on='mixture_changed,+law_input')
    @cached_property
    def _get_tree_node_list(self):
        return [ self.cc_law ]

    tree_view = View(HGroup(
                Group(
                      Item('n_cj'),
                      Item('mixture'),
                      Item('cc_law_type'),
                      Group(
                      Item('geo', show_label=False,
                           editor=InstanceEditor(name='geo_lst',
                           editable=True), style='custom'),
                      label='Geometry'
                      ),
                      label='Matrix',
                      springy=True
                      ),
                springy=True,
                ),
                width=0.4,
                height=0.4,
                resizable=True,
                buttons=['OK', 'Cancel'])

if __name__ == '__main__':
    mcs = MatrixCrossSection()
    mcs.configure_traits()
