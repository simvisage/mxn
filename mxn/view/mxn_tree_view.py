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
    Str, List, WeakRef

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, \
    HSplit, HGroup, Handler

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from traitsui.menu import \
    Menu, Action

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction

from pyface.file_dialog import \
    FileDialog

from traitsui.file_dialog import \
    open_file, save_file

import pickle

class MxNTreeNode(HasStrictTraits):
    '''Base class of all model classes that can appear in a tree node.
    '''
    node_name = Str('<unnamed>')

    tree_node_list = List([])

    view = View()

    plot_state = WeakRef(transient=True)
    '''Allows for passing a reference to cross section
    to reinforcement layout node for purposes of plotting
    '''
    def __getstate__ (self):
        '''Overriding __getstate__ because of WeakRef usage
        '''
        state = super(HasStrictTraits, self).__getstate__()

        for key in [ 'plot_state', 'plot_state_' ]:
            if state.has_key(key):
                del state[ key ]

        return state

    def plot(self, fig):
        if self.plot_state:
            ax = fig.add_subplot(1, 1, 1)
            self.plot_state.plot_geometry(ax)
        return

class MxNLeafNode(HasStrictTraits):
    '''Base class of all model classes that can appear in a tree node.
    '''
    node_name = Str('<unnamed>')

    def plot(self, fig):
        return

plot_self = Action(name='Plot', action='plot_node')
'''Menu action for plotting tree nodes
'''
menu_save = Action(name='Save', action='menu_save')
'''Menubar action for saving the root node to file
'''
menu_open = Action(name='Open', action='menu_open')
'''Menubar action for loading root node from file
'''


tree_node = TreeNode(node_for=[MxNTreeNode],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(NewAction, DeleteAction, plot_self)
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

class MxNTreeViewHandler(Handler):
    '''Handler for MxNTreeView class
    '''
    def plot_node(self, info, node):
        '''Handles context menu action Plot for tree nodes
        '''
        info.object.figure.clear()
        node.plot(info.object.figure)
        info.object.data_changed = True

    def menu_save(self, info):
        file_name = save_file()
        pickle.dump(info.object.root, open(file_name, 'wb'), 1)

    def menu_open(self, info):
        file_name = open_file()
        info.object.root = pickle.load(open(file_name, 'rb'))

class MxNTreeView(HasStrictTraits):
    '''View object for a cross section state.
    '''
    root = Instance(MxNTreeNode)

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
                    width=0.7,
                    height=0.4,
                    buttons=['OK', 'Cancel'],
                    resizable=True,
                    handler=MxNTreeViewHandler())

if __name__ == '__main__':

    tr = MxNTreeNode(node_name='root',
                     tree_node_list=[MxNTreeNode(node_name='subnode 1'),
                                     MxNTreeNode(node_name='subnode 2'),
                                     ])

    tv = MxNTreeView(root=tr)
    tv.configure_traits()
