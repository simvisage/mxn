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
    
    #===============================================================================
    # Plotting functions
    #===============================================================================
    
    def plot_geometry(self, ax, clr):
        '''Plot geometry'''
        return

    def plot_eps(self, ax):
        return
    
    def plot_sig(self, ax):
        return
    
    def plot(self, fig):
        '''Plots the cross section - particular reinforcement component 
        plotted with distinctive color to others 
        '''
        ax1 = fig.add_subplot(1,2,1)
        self.state.plot_geometry(ax1)
        self.plot_geometry(ax1, clr='red')
        ax2 = fig.add_subplot(1,2,2)
        self.ecb_law.plot_ax(ax2)


    #===========================================================================
    # Auxiliary methods for tree editor
    #===========================================================================
    tree_node_list = Property(depends_on='ecb_law_type')
    @cached_property
    def _get_tree_node_list(self):
        return [ self.ecb_law ]

