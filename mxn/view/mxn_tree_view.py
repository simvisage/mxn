'''
Created on 28. 3. 2014

The module defines the framework for tree visualization of the model
in a ModelView window. The components of the model classes should
inherit from the MxNTreeNode and supply the attributes

 - node_name - a label to appear in the tree editor
 - tree_node_list  - subnodes of the current nodes

 Further, the plot method can be defined to plot the current node
 in the plot window of the model view.

@author: rch
'''

from traits.api import \
    HasStrictTraits, Instance, Button, Event, \
    Str, List, WeakRef, Property, cached_property

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, \
    HSplit, HGroup, Handler

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from traitsui.menu import \
    Menu, MenuBar, Separator

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction

from mxn_tree_node import \
    MxNTreeNode, MxNLeafNode

from mxn_tree_view_handler import \
    MxNTreeViewHandler, plot_self, menu_save, \
    menu_open, menu_exit

tree_node = TreeNode(node_for=[MxNTreeNode],
                                     auto_open=False,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(DeleteAction, plot_self),
#                                      move=[MxNTreeNode, MxNLeafNode],
#                                      add=[MxNTreeNode, MxNLeafNode]
                                     )

leaf_node = TreeNode(node_for=[MxNLeafNode],
                                     auto_open=True,
                                     children='',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(plot_self)
                                     )

tree_editor = TreeEditor(
                    nodes=[ tree_node, leaf_node ],
                    selected='selected_node',
                    orientation='vertical'
                             )

class MxNTreeView(HasStrictTraits):
    '''View object for a cross section state.
    '''
    root = Instance(HasStrictTraits)

    selected_node = Instance(HasStrictTraits)

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
                    id='mxntreeview_id',
                    width=0.7,
                    height=0.4,
                    title='MxN',
                    resizable=True,
                    handler=MxNTreeViewHandler(),
                    menubar=MenuBar(Menu(menu_exit, Separator(),
                                         menu_save, menu_open,
                                    name='File'))
                    )

if __name__ == '__main__':

    tr = MxNTreeNode(node_name='root',
                     tree_node_list=[MxNTreeNode(node_name='subnode 1'),
                                     MxNTreeNode(node_name='subnode 2'),
                                     ])

    tv = MxNTreeView(root=tr)
    tv.configure_traits()
