'''
Created on 28. 3. 2014

The module defines the framework for tree visualizatoin of the model
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
    Property, cached_property, Str, List

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, \
    HSplit, HGroup, VGroup, Handler

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from traitsui.menu import \
    Menu, Action, Separator

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction

class MxNTreeNode(HasStrictTraits):
    '''Base class of all model classes that can appear in a tree node.
    '''
    node_name = Str('<unnamed>')

    tree_node_list = List([])
    
    view = View()

    def plot(self, fig):
        return
        #print 'Node "', self.node_name, '" received', fig

plot_self = Action(name='Plot', action='plot_node')
'''Menu action for plotting tree nodes
'''

tree_node = TreeNode(node_for=[MxNTreeNode ],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     #view=View(),
                                     menu=Menu(NewAction, DeleteAction, plot_self)
                                     )

tree_editor = TreeEditor(
                    nodes=[ tree_node ],
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

class MxNTreeView(HasStrictTraits):
    '''View object for a cross section state.
    '''
    root = Instance(MxNTreeNode)

    selected_node = Instance(MxNTreeNode)

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
