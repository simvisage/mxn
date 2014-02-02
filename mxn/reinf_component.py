'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.


@author: rch
'''
from etsproxy.traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Trait, Event, on_trait_change, Instance, Button, Callable, \
    DelegatesTo, Constant, WeakRef

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from etsproxy.traits.ui.api import \
    View, Item, Group, HSplit, VGroup, HGroup

from ecb_law import \
    ECBLBase, ECBLLinear, ECBLFBM, ECBLCubic, ECBLBilinear, ECBLSteel

from constitutive_law import \
    ConstitutiveLawModelView

from mxn.matrix_cross_section import \
    MatrixCrossSection

from mxn.cross_section_component import \
    CrossSectionComponent, \
    ECB_COMPONENT_CHANGE, \
    ECB_COMPONENT_AND_EPS_CHANGE

class ReinfComponent(CrossSectionComponent):
    '''Cross section characteristics needed for tensile specimens
    '''

    matrix_cs = WeakRef(MatrixCrossSection)

    height = DelegatesTo('matrix_cs')
    '''height of reinforced cross section
    '''

    #===========================================================================
    # Effective crack bridge law
    #===========================================================================
    ecb_law_type = Trait('fbm', dict(fbm=ECBLFBM,
                                  cubic=ECBLCubic,
                                  linear=ECBLLinear,
                                  bilinear=ECBLBilinear,
                                  steel=ECBLSteel),
                      tt_input=True)
    '''Selector of the effective crack bridge law type
    ['fbm', 'cubic', 'linear', 'bilinear','steel']'''

    ecb_law = Property(Instance(ECBLBase), depends_on='+tt_input')
    '''Effective crack bridge law corresponding to ecb_law_type'''
    @cached_property
    def _get_ecb_law(self):
        return self.ecb_law_type_(sig_tex_u=self.sig_tex_u, cs=self)

    show_ecb_law = Button
    '''Button launching a separate view of the effective crack bridge law.
    '''
    def _show_ecb_law_fired(self):
        ecb_law_mw = ConstitutiveLawModelView(model=self.ecb_law)
        ecb_law_mw.edit_traits(kind='live')
        return

    tt_modified = Event
