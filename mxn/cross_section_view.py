'''
Created on 26. 2. 2014

@author: Vancikv
'''

from traits.api import \
    HasStrictTraits, Instance, Button, Event, \
    Property, cached_property, WeakRef, Str

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, \
    HSplit, HGroup, Menu

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction

from mxn.cross_section import \
    CrossSection

from mxn.reinf_layout import \
    RLCTexUniform, RLCTexLayer, RLCBar

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from mxn.mxn_tree_node import \
    MxNTreeNode

from mxn.view import \
    tree_node, plot_self, \
    MxNTreeViewHandler, leaf_node

class CrossSectionTreeNode(MxNTreeNode):
    '''Proxy class for the cross section node returning the two subnotes.
    '''
    cs = WeakRef(CrossSection)
    node_name = 'Cross section'
    view = View(Item('cs@', show_label=False))

    def plot(self, fig):
        self.cs.plot(fig)

    tree_node_list = Property
    def _get_tree_node_list(self):
        return [self.cs.matrix_cs_with_state, ReinfLayoutTreeNode(cs_state=self.cs)]

class ReinfLayoutTreeNode(HasStrictTraits):
    '''Method accommodating the list of all reinforcement components.
    '''
    cs_state = WeakRef(CrossSection)
    node_name = Str('Reinforcement layout')
    view = View()

    def plot(self, fig):
        ax = fig.add_subplot(1, 1, 1)
        self.cs_state.plot_geometry(ax)

    tree_node_list = Property(depends_on='cs_state.reinf_components_with_state')
    @cached_property
    def _get_tree_node_list(self):
        return self.cs_state.reinf_components_with_state

reinf_layout_node = TreeNode(node_for=[ReinfLayoutTreeNode],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view=View(),
                                     menu=Menu(NewAction, plot_self),
                                     add=[RLCTexUniform, RLCTexLayer, RLCBar]
                                     )

reinf_layout_node_steel = TreeNode(node_for=[RLCBar],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     menu=Menu(DeleteAction, plot_self),
                                     )

reinf_layout_node_tex_layer = TreeNode(node_for=[RLCTexLayer],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     menu=Menu(DeleteAction, plot_self),
                                     )

reinf_layout_node_tex_uniform = TreeNode(node_for=[RLCTexUniform],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     menu=Menu(DeleteAction, plot_self),
                                     )

tree_editor = TreeEditor(
                    nodes=[tree_node,
                           leaf_node,
                           reinf_layout_node,
                           reinf_layout_node_steel,
                           reinf_layout_node_tex_layer,
                           reinf_layout_node_tex_uniform],
                    selected='selected_node',
                    orientation='vertical'
                             )

class CrossSectionView(HasStrictTraits):
    '''View object for a cross section state.
    '''
    cs = Instance(CrossSection)
    selected_node = Instance(HasStrictTraits)

    root = Property(depends_on='cs')
    @cached_property
    def _get_root(self):
        return CrossSectionTreeNode(cs=self.cs)

    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        figure.add_axes([0.08, 0.13, 0.85, 0.74])
        return figure

    data_changed = Event

    replot = Button
    def _replot_fired(self):
        self.figure.clear()
        self.selected_node.plot(self.figure)
        self.data_changed = True

    clear = Button()
    def _clear_fired(self):
        self.figure.clear()
        self.data_changed = True

    view = View(HSplit(Group(Item('root',
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
                    resizable=True,
                    handler=MxNTreeViewHandler())
