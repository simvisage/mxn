'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.

@author: rch
'''
from etsproxy.traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Event, on_trait_change, Callable, Instance, WeakRef, Trait, Button

from etsproxy.traits.ui.api import \
    View, Item, Group, HGroup

from mxn.cross_section_component import \
    CrossSectionComponent, \
    ECB_COMPONENT_CHANGE, \
    ECB_COMPONENT_AND_EPS_CHANGE

from mxn.cross_section_state import \
    CrossSectionState
    
from mxn.cross_section_geo import \
    CrossSectionGeo, GeoRect, GeoI, GeoCirc

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from etsproxy.traits.ui.api import \
    View, Item, Group, HSplit, VGroup, HGroup

from ecb_law import \
    ECBLBase, ECBLLinear, ECBLFBM, ECBLCubic, ECBLBilinear

from constitutive_law import \
    ConstitutiveLawModelView

from cc_law import \
    CCLawBase, CCLawBlock, CCLawLinear, CCLawQuadratic, CCLawQuad

import numpy as np

class MatrixCrossSection(CrossSectionComponent):
    '''Cross section characteristics needed for tensile specimens.
    '''

    n_cj = Float(30, auto_set=False, enter_set=True, geo_input=True)
    '''Number of integration points.
    '''

    f_ck = Float(55.7, auto_set=False, enter_set=True,
                 cc_input=True)
    '''Ultimate compression stress  [MPa]
    '''

    eps_c_u = Float(0.0033, auto_set=False, enter_set=True,
                    cc_input=True)
    '''Strain at failure of the matrix in compression [-]
    '''

    x = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Height of the compressive zone
    '''
    @cached_property
    def _get_x(self):
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        if eps_up == eps_lo:
            # @todo: explain
            return (abs(eps_up) / (abs(eps_up - eps_lo * 1e-9)) *
                     self.height)
        else:
            return (abs(eps_up) / (abs(eps_up - eps_lo)) *
                     self.height)

    z_ti_arr = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Discretizaton of the  compressive zone
    '''
    @cached_property
    def _get_z_ti_arr(self):
        if self.state.eps_up <= 0: # bending
            zx = min(self.height, self.x)
            return np.linspace(0, zx, self.n_cj)
        elif self.state.eps_lo <= 0: # bending
            return np.linspace(self.x, self.height, self.n_cj)
        else: # no compression
            return np.array([0], dtype='f')

    eps_ti_arr = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Compressive strain at each integration layer of the compressive zone [-]:
    '''
    @cached_property
    def _get_eps_ti_arr(self):
        # for calibration us measured compressive strain
        # @todo: use mapped traits instead
        #
        height = self.height
        eps_up = self.state.eps_up
        eps_lo = self.state.eps_lo
        eps_j_arr = (eps_up + (eps_lo - eps_up) * self.z_ti_arr /
                     height)
        return (-np.fabs(eps_j_arr) + eps_j_arr) / 2.0

    zz_ti_arr = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Distance of discrete slices of compressive zone from the bottom
    '''
    @cached_property
    def _get_zz_ti_arr(self):
        return self.height - self.z_ti_arr

    #===========================================================================
    # Cross section geometry and related parameters
    #===========================================================================

    geo = Instance(CrossSectionGeo)
    '''Geometry of the cross section
    '''
    
    height = Property(depends_on='geo.+geo_input')
    '''height of the cross section [m]
    '''
    def _get_height(self):
        return self.geo.height

    w_ti_arr = Property(depends_on='geo.+geo_input,+geo_input')
    '''Discretization of the  compressive zone - weight factors for general cross section
    '''
    @cached_property
    def _get_w_ti_arr(self):
        return self.geo.get_width(self.z_ti_arr)
    
    #===========================================================================
    # Compressive concrete constitutive law
    #===========================================================================

    cc_law_type = Trait('constant', dict(constant=CCLawBlock,
                                         linear=CCLawLinear,
                                         quadratic=CCLawQuadratic,
                                         quad=CCLawQuad),
                        cc_input=True)
    '''Selector of the concrete compression law type
    ['constant', 'linear', 'quadratic', 'quad']'''

    cc_law = Property(Instance(CCLawBase), depends_on='+cc_input')
    '''Compressive concrete law corresponding to cc_law_type'''
    @cached_property
    def _get_cc_law(self):
        return self.cc_law_type_(f_ck=self.f_ck, eps_c_u=self.eps_c_u, cs=self)

    show_cc_law = Button
    '''Button launching a separate view of the compression law.
    '''
    def _show_cc_law_fired(self):
        cc_law_mw = ConstitutiveLawModelView(model=self.cc_law)
        cc_law_mw.edit_traits(kind='live')
        return

    cc_modified = Event

    #===========================================================================
    # Calculation of compressive stresses and forces
    #===========================================================================

    sig_ti_arr = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Stresses at the j-th integration point.
    '''
    @cached_property
    def _get_sig_ti_arr(self):
        return -self.cc_law.mfn_vct(-self.eps_ti_arr)

    f_ti_arr = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Layer force corresponding to the j-th integration point.
    '''
    @cached_property
    def _get_f_ti_arr(self):
        return self.w_ti_arr * self.sig_ti_arr * self.unit_conversion_factor

    N = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        return np.trapz(self.f_ti_arr, self.z_ti_arr)

    M = Property(depends_on=ECB_COMPONENT_AND_EPS_CHANGE + ',geo.+geo_input')
    '''Get the resulting moment evaluated with respect to the center line
    '''
    @cached_property
    def _get_M(self):
        return np.trapz(self.f_ti_arr * self.z_ti_arr, self.z_ti_arr)

    modified = Event
    @on_trait_change('+geo_input')
    def set_modified(self):
        self.modified = True

    view = View(HGroup(
                Group(Item('height', springy=True),
                      Item('width'),
                      Item('n_layers'),
                      Item('n_rovings'),
                      Item('A_roving'),
                      label='Geometry',
                      springy=True
                      ),
                springy=True,
                ),
                resizable=True,
                buttons=['OK', 'Cancel'])

if __name__ == '__main__':
    state = CrossSectionState(eps_lo=0.02)
    ecs = MatrixCrossSection(state=state, height=0.4)

    print 'zz_ti_arr', ecs.zz_ti_arr
    print 'ecb_lo', ecs.state.eps_lo
    #ecs.configure_traits()
