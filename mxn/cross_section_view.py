'''
Created on 26. 2. 2014

@author: Vancikv
'''

from traits.api import \
    HasStrictTraits, Instance, Button, Event, \
    Property, cached_property, WeakRef

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, \
    HSplit, HGroup, VGroup
    
from cross_section import \
    CrossSection

from matrix_laws import \
    MatrixLawBase

from reinf_laws import \
    ReinfLawBase

from matrix_cross_section import \
    MatrixCrossSection

from reinf_layout import \
    ReinfLayoutComponent, RLCTexUniform, RLCTexLayer, RLCSteelBar

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

class CrossSectionTreeNode(CrossSection):

    #===========================================================================
    # Auxiliary access methods
    #===========================================================================

    tree_node_list = Property(depends_on='matrix_cs')
    @cached_property
    def _get_tree_node_list(self):
        return [self.matrix_cs_with_state, ReinfLayoutTreeNode(cs_state=self)]

#     matrix_cs_tree_node = Property(depends_on='matrix_cs')
#     '''Auxiliary property for tree node visualization.
#     (must be a list)
#     '''
#     @cached_property
#     def _get_matrix_cs_tree_node(self):
#         return [self.matrix_cs_with_state]


class ReinfLayoutTreeNode(HasStrictTraits):
    '''Method accommodating the list of all reinforcement components.
    '''
    cs_state = WeakRef(CrossSectionTreeNode)

    tree_node_list = Property(depends_on='cs_state.reinf_components_with_state')
    @cached_property
    def _get_tree_node_list(self):
        return self.cs_state.reinf_components_with_state


tree_editor = TreeEditor(
            nodes=[
                   TreeNode(node_for=[CrossSectionTreeNode],
                             auto_open=True,
                             children='tree_node_list',
                             label='=Cross section',
                             view=View(VGroup(Item('eps_up'),
                                              Item('eps_lo'),
                                              label='Cross section'
                                              ),
                                       resizable=True,
                                       buttons=['OK', 'Cancel']
                                       )
                            ),
                   TreeNode(node_for=[ReinfLayoutTreeNode],
                             auto_open=True,
                             children='tree_node_list',
                             label='=Reinforcement Layout',
                             view=View(),
                             add=[RLCTexUniform, RLCTexLayer, RLCSteelBar]
                            ),
                   TreeNode(node_for=[RLCTexUniform, RLCTexLayer, RLCSteelBar],
                             auto_open=True,
                             children='tree_node_list',
                             label='name'
                            ),
                   TreeNode(node_for=[MatrixCrossSection],
                              auto_open=True,
                              children='tree_node_list',
                              label='=Matrix',
                            ),
                   TreeNode(node_for=[ReinfLawBase],
                              auto_open=True,
                             children='',
                              label='=Constitutive law',
                            ),
                   TreeNode(node_for=[MatrixLawBase],
                              auto_open=True,
                             children='',
                              label='=Constitutive law',
                            ),
                   ],
                         orientation='vertical'
                         )


class CrossSectionView(HasStrictTraits):
    '''View object for a cross section state.
    '''
    cs = Instance(CrossSection)

    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        figure.add_axes([0.08, 0.13, 0.85, 0.74])
        return figure

    data_changed = Event

    replot = Button
    def _replot_fired(self):
        self.figure.clear()
        fig = self.figure
        ax1 = fig.add_subplot(111)
        self.cs.plot_geometry(ax1)
        self.data_changed = True

    clear = Button()
    def _clear_fired(self):
        self.figure.clear()

    view = View(HSplit(Group(Item('cs',
                            editor=tree_editor,
                            resizable=True,
                            show_label=False),
                           ),
                       Group(HGroup(Item('replot', show_label=False),
                                    Item('clear', show_label=False),
                                   ),
                             Item('figure', editor=MPLFigureEditor(),
                             resizable=True, show_label=False),
                             label='plot sheet',
                             dock='tab',
                             )
                    ),
                    width=0.7,
                    height=0.4,
                    buttons=['OK', 'Cancel'],
                    resizable=True)
