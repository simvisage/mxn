'''
Created on 6. 4. 2014

@author: Vancikv

Defines a tree view for a parameter study.
'''

from traits.api import \
    HasStrictTraits, Instance, Button, Event

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, \
    HSplit, HGroup, VGroup

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure
    
from mxn_diagram import \
    MxNDiagram

from mxn_parametric_study import \
    MxNParametricStudy, MxNDescription
    
from mxn.view import \
    tree_node, MxNTreeNode, plot_self, \
    MxNTreeViewHandler, leaf_node, \
    menu_save, menu_open

from traitsui.menu import \
    Menu, Action, Separator, MenuBar

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction, RenameAction, \
    CopyAction, PasteAction
 
mxn_ps_node = TreeNode(node_for=[MxNParametricStudy],
                                     auto_open=False,
                                     children='description_lst',
                                     label='node_name',
                                     menu=Menu(NewAction, DeleteAction, plot_self, PasteAction),
                                     add=[MxNDescription]
                                     )

mxn_description_node = TreeNode(node_for=[MxNDescription],
                                     auto_open=False,
                                     children='tree_node_list',
                                     label='node_name',
                                     menu=Menu(RenameAction, DeleteAction, plot_self, CopyAction),
                                     )

tree_editor = TreeEditor(
                    nodes=[tree_node, 
                           leaf_node,
                           mxn_ps_node,
                           mxn_description_node],
                    selected='selected_node',
                    orientation='vertical'
                             )

class MxNPSView(HasStrictTraits):
    '''View object for a cross section state.
    '''
    root = Instance(MxNParametricStudy)
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
                    handler=MxNTreeViewHandler(),
                    menubar=MenuBar(Menu(menu_save, menu_open,
                                    name = 'File'))
                )
