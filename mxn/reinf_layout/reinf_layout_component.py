'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.


@author: rch
'''
from traits.api import \
    Property, cached_property, HasStrictTraits, \
    Trait, Instance, WeakRef, Str, on_trait_change

from mxn.reinf_laws import \
    ReinfLawBase

from mxn.matrix_cross_section import \
    MatrixCrossSection

from mxn import \
    CrossSectionComponent

from matresdev.db.simdb import \
    SimDBClass

STATE_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed'
STATE_LAW_AND_GEOMETRY_CHANGE = 'eps_changed,+geo_input,matrix_cs.geo.changed,law_changed,+law_input,ecb_law.+input'

class ReinfLayoutComponent(CrossSectionComponent):
    '''Cross section characteristics needed for tensile specimens
    '''

    matrix_cs = WeakRef(MatrixCrossSection, transient=True)

    def __getstate__ (self):
        '''Overriding __getstate__ because of WeakRef usage
        '''
        state = super(HasStrictTraits, self).__getstate__()

        for key in [ 'state', 'state_', 'plot_state',
                    'plot_state_', 'matrix_cs', 'matrix_cs_' ]:
            if state.has_key(key):
                del state[ key ]

        return state

    @on_trait_change('ecb_law.+input')
    def notify_law_change(self):
        # print 'law internal change - object:', self
        self.law_changed = True

    #===========================================================================
    # Effective crack bridge law
    #===========================================================================

    ecb_law_key = Trait('fbm-default', ReinfLawBase.db.keys(), law_input=True)

    ecb_law = Property(Instance(SimDBClass), depends_on='+law_input')
    '''Effective crack bridge law corresponding to ecb_law_key'''
    @cached_property
    def _get_ecb_law(self):
        law = ReinfLawBase.db[ self.ecb_law_key ]
        return law

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
        ax1 = fig.add_subplot(1, 2, 1)
        self.state.plot_geometry(ax1)
        self.plot_geometry(ax1, clr='red')
        ax2 = fig.add_subplot(1, 2, 2)
        self.ecb_law.plot_ax(ax2)


    #===========================================================================
    # Auxiliary methods for tree editor
    #===========================================================================
    tree_node_list = Property(depends_on='ecb_law_key')
    @cached_property
    def _get_tree_node_list(self):
        return [ self.ecb_law ]

if __name__ == '__main__':
    ReinfLawBase.db.configure_traits()
    print ReinfLawBase.db.keys()
