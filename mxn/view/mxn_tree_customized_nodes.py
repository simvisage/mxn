'''
Created on 9. 7. 2014

@author: Vancikv
'''

from traitsui.api import \
    TreeNode

from traitsui.menu import \
    Menu, MenuBar, Separator

from mxn_tree_view import \
    plot_self, menu_save, \
    menu_open, menu_exit

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction, CopyAction, PasteAction

from use_cases import \
    UCPStudyElementMxN

from mxn_diagram import \
    MxNDiagram

mxn_diagram_container_node = TreeNode(node_for=[UCPStudyElementMxN],
                                     auto_open=False,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(DeleteAction, PasteAction),
                                     )

mxn_diagram_node = TreeNode(node_for=[MxNDiagram],
                                     auto_open=False,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(DeleteAction, CopyAction),
                                     )
