'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.


@author: rch
'''

from traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Trait, Event, on_trait_change, Instance, Button, Callable, \
    DelegatesTo, Constant, List, WeakRef

from matplotlib.figure import \
    Figure

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, HSplit, VGroup, HGroup

from cross_section_state import \
    CrossSectionState

from matrix_cross_section import \
    MatrixCrossSection

from reinf_layout import \
    ReinfLayoutComponent

import numpy as np


class CrossSection(CrossSectionState):
    '''Cross section characteristics needed for tensile specimens
    '''
    matrix_cs = Instance(MatrixCrossSection)
    def _matrix_cs_default(self):
        return MatrixCrossSection()

    reinf = List(ReinfLayoutComponent)
    '''Components of the cross section including the matrix and reinforcement.
    '''

    matrix_cs_with_state = Property(depends_on='matrix_cs')
    @cached_property
    def _get_matrix_cs_with_state(self):
        self.matrix_cs.state = self
        return self.matrix_cs

    reinf_components_with_state = Property(depends_on='reinf')
    '''Components linked to the strain state of the cross section
    '''
    @cached_property
    def _get_reinf_components_with_state(self):
        for r in self.reinf:
            r.state = self
            r.matrix_cs = self.matrix_cs
        return self.reinf

    unit_conversion_factor = Constant(1000.0)

    '''Convert the MN to kN
    '''

    #===========================================================================
    # State management
    #===========================================================================
    changed = Event
    '''Notifier of a changed in some component of a cross section
    '''

    @on_trait_change('+eps_input')
    def _notify_eps_change(self):
        self.matrix_cs.eps_changed = True
        for c in self.reinf:
            c.eps_changed = True

    #===========================================================================
    # Cross-sectional stress resultants
    #===========================================================================

    N = Property(depends_on='changed,+eps_input')
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        N_matrix = self.matrix_cs_with_state.N
        return N_matrix + np.sum([c.N for c in self.reinf_components_with_state])

    M = Property(depends_on='changed,+eps_input')
    '''Get the resulting moment.
    '''
    @cached_property
    def _get_M(self):
        M_matrix = self.matrix_cs_with_state.M
        M = M_matrix + np.sum([c.M for c in self.reinf_components_with_state])
        return M - self.N * self.matrix_cs.geo.gravity_centre

    def plot_geometry(self, ax):
        self.matrix_cs_with_state.geo.plot_geometry(ax)
        for r in self.reinf_components_with_state:
            r.plot_geometry(ax)

    def plot_eps(self, ax):
        self.matrix_cs_with_state.plot_eps(ax)
        for r in self.reinf_components_with_state:
            r.plot_eps(ax)
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

    def plot_sig(self, ax):
        self.matrix_cs_with_state.plot_sig(ax)
        for r in self.reinf_components_with_state:
            r.plot_sig(ax)
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

    #===========================================================================
    # Auxiliary access methods
    #===========================================================================

    tree_node_list = Property(depends_on='matrix_cs')
    @cached_property
    def _get_tree_node_list(self):
        return [self.matrix_cs_with_state, ReinfLayout(cs_state=self)]

    matrix_cs_tree_node = Property(depends_on='matrix_cs')
    '''Auxiliary property for tree node visualization.
    (must be a list)
    '''
    @cached_property
    def _get_matrix_cs_tree_node(self):
        return [self.matrix_cs_with_state]

    view = View(VGroup(Item('eps_up'),
                       Item('eps_lo'),
                       Item('matrix_cs'),
                       label='Cross section'
                      ),
                resizable=True,
                buttons=['OK', 'Cancel']
                )

class ReinfLayout(HasStrictTraits):
    '''Method accommodating the list of all reinforcement components.
    '''
    cs_state = WeakRef(CrossSection)

    tree_node_list = Property(depends_on='cs_state.reinf_components_with_state')
    @cached_property
    def _get_tree_node_list(self):
        return self.cs_state.reinf_components_with_state

if __name__ == '__main__':
    pass
