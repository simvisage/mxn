'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.


@author: rch
'''
from etsproxy.traits.api import \
    Property, cached_property, \
    Trait, Instance, Button, WeakRef, Str

from mxn.reinf_laws import \
    ReinfLawBase, ReinfLawLinear, ReinfLawFBM, ReinfLawCubic, ReinfLawBilinear, ReinfLawSteel

from constitutive_law import \
    ConstitutiveLawModelView
 
from mxn.matrix_cross_section import \
    MatrixCrossSection

from mxn import \
    CrossSectionComponent

STATE_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed'
STATE_LAW_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed,+law_input'

class ReinfLayoutComponent(CrossSectionComponent):
    '''Cross section characteristics needed for tensile specimens
    '''
    
    name = Str()

    matrix_cs = WeakRef(MatrixCrossSection)

    #===========================================================================
    # Effective crack bridge law
    #===========================================================================
    ecb_law_type = Trait('fbm', dict(fbm=ReinfLawFBM,
                                  cubic=ReinfLawCubic,
                                  linear=ReinfLawLinear,
                                  bilinear=ReinfLawBilinear,
                                  steel=ReinfLawSteel),
                      law_input=True)
    '''Selector of the effective crack bridge law type
    ['fbm', 'cubic', 'linear', 'bilinear','steel']'''

    ecb_law = Property(Instance(ReinfLawBase), depends_on='+law_input')
    '''Effective crack bridge law corresponding to ecb_law_type'''
    @cached_property
    def _get_ecb_law(self):
        return self.ecb_law_type_(cs=self.state)

    show_ecb_law = Button
    '''Button launching a separate view of the effective crack bridge law.
    '''
    def _show_ecb_law_fired(self):
        ecb_law_mw = ConstitutiveLawModelView(model=self.ecb_law)
        ecb_law_mw.edit_traits(kind='live')
        return

