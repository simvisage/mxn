'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.


@author: rch
'''

from traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Trait, Event, on_trait_change, Instance, Button, Callable, \
    DelegatesTo, Constant, List

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, HSplit, VGroup, HGroup

from cross_section_state import \
    CrossSectionState

from matrix_cross_section import \
    MatrixCrossSection

from reinf_layout_component import \
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
        self.changed = True
        self.matrix_cs.eps_changed = True
        for c in self.reinf:
            c.eps_changed = True

    #===========================================================================
    # Cross-sectional stress resultants
    #===========================================================================

    N = Property(depends_on='changed')
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        N_matrix = self.matrix_cs_with_state.N
        return N_matrix + np.sum([c.N for c in self.reinf_components_with_state])

    M = Property(depends_on='changed')
    '''Get the resulting moment.
    '''
    @cached_property
    def _get_M(self):
        M_matrix = self.matrix_cs_with_state.M
        M = M_matrix + np.sum([c.M for c in self.reinf_components_with_state])
        return M - self.N * self.matrix_cs.geo.gravity_centre

    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        figure.add_axes([0.08, 0.13, 0.85, 0.74])
        return figure

    replot = Button
    def _replot_fired(self):
        self.figure.clear()
        fig = self.figure
        ax1 = fig.add_subplot(131)
        ax2 = fig.add_subplot(132)
        ax3 = fig.add_subplot(133)

        self.plot_geometry(ax1)
        self.plot_eps(ax2)
        self.plot_sig(ax3)

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
    
    view = View(HSplit(
                    VGroup(Item('eps_up'),
                           Item('eps_lo'),
                           Item('matrix_cs')
                            ),
                      Group(
                      Item('replot', show_label=False),
                      Item('figure', editor=MPLFigureEditor(),
                           resizable=True, show_label=False),
                      id='simexdb.plot_sheet',
                      label='plot sheet',
                      dock='tab',
                      )))
        
class CrossSectionTree(HasStrictTraits):
    cs = Instance(CrossSection)
    
# tree_editor = TreeEditor(
#             nodes=[
#                    TreeNode( node_for = [CrossSection],
#                              auto_open = True,
#                              children = '',
#                              label = '=Cross section',
#                             ),
#                    TreeNode( node_for = [CrossSection],
#                              auto_open = True,
#                              children = 'reinf',
#                              label = '=Reinforcement',
#                              view = View(),
#                              add = [ReinfTexUniform, ReinfTexLayer, SteelBar]
#                             ),
#                    TreeNode( node_for = [ReinfTexUniform, ReinfTexLayer, SteelBar],
#                              auto_open = True,
#                             ),
#                    TreeNode( node_for = [MatrixCrossSection],
#                               auto_open = True,
#                             ),
#                    ],
#                          orientation='vertical'
#                          )
# 
# view = View(
#                Group(
#                    Item(
#                         name = 'cs',
#                         editor = tree_editor,
#                         resizable = True ),
#                     orientation = 'vertical',
#                     show_labels = True,
#                     show_left = True, ),
#                 title = 'Cross section structure',
#                 dock = 'horizontal',
#                 drop_class = HasStrictTraits,
#                 buttons = [ 'Undo', 'OK', 'Cancel' ],
#                 resizable = True,
#                 width = .5,
#                 height = .5 )
    

if __name__ == '__main__':
#     from mxn.matrix_cross_section.matrix_cross_section_geo import GeoRect
#     ecs = CrossSection(reinf=[ReinfTexUniform(n_layers=3)],
#                          matrix_cs=MatrixCrossSection(geo=GeoRect(width=0.1, height=0.05),
#                                                          n_cj=20),
#                          eps_lo=0.014,
#                          eps_up= -0.0033,
#                          )
#     print ecs.M
#     cst = CrossSectionTree(cs=ecs)
#     cst.configure_traits(view=view)
    pass
