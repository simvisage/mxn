'''
Created on 9. 7. 2014

@author: Vancikv
'''

from traitsui.api import \
    TreeNode

from traitsui.menu import \
    Menu, MenuBar, Separator, Action

from mxn_tree_view_handler import \
    plot_self

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction, CopyAction, PasteAction

from use_cases import \
    UCPStudyElementMxN

from mxn_diagram import \
    MxNDiagram

from cross_section import \
    CrossSection

from utils import \
    get_outfile

from material_types import \
    MaterialTypeBase

from mxn_tree_node import \
    ReinfLayoutTreeNode

from reinf_layout import \
    RLCTexLayer, RLCTexUniform, RLCBar

import pickle, os

class SingleChildTreeNode(TreeNode):
    def append_child (self, object, child):
        """ Overriding this method ensures that there is
        always only one child and that upon dropping an object
        merely its copy is assigned.
        """
        copy_file = get_outfile(folder_name='.mxn',
                          file_name='temp.pkl')
        file = open(copy_file, 'wb')
        pickle.dump(child, file, 1)
        file.close()
        file = open(copy_file, 'rb')
        new_child = pickle.load(file)
        file.close()
        os.remove(copy_file)

        setattr(object, self.children , [new_child])

    def delete_child (self, object, index):
        """ Overriding the delete method in order to ensure
        that a dragged object does not remove itself from its
        original location, i.e. the method does nothing because
        there should always be one child.
        """
        pass

mxn_diagram_container_node = SingleChildTreeNode(
                                     node_for=[UCPStudyElementMxN],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(DeleteAction,
                                               PasteAction,
                                                plot_self),
                                     add=[MxNDiagram],
                                     )

mxn_diagram_node = SingleChildTreeNode(node_for=[MxNDiagram],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     add=[CrossSection],
                                     menu=Menu(CopyAction,
                                               PasteAction,
                                               plot_self),
                                     )

cross_section_node = TreeNode(node_for=[CrossSection],
                              auto_open=True,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(CopyAction, plot_self),
                              )

material_type_node = TreeNode(node_for=[MaterialTypeBase],
                              auto_open=False,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(),
                              )

reinf_layout_node = TreeNode(node_for=[ReinfLayoutTreeNode],
                              auto_open=True,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(plot_self, NewAction),
                              add=[RLCTexUniform,
                                   RLCTexLayer,
                                   RLCBar]
                              )

reinf_tex_uniform_node = TreeNode(node_for=[RLCTexUniform],
                              auto_open=False,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(plot_self, DeleteAction),
                              )

reinf_tex_layer_node = TreeNode(node_for=[RLCTexLayer],
                              auto_open=False,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(plot_self, DeleteAction),
                              )

reinf_bar_node = TreeNode(node_for=[RLCBar],
                              auto_open=False,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(plot_self, DeleteAction),
                              )

custom_node_list = [mxn_diagram_container_node, mxn_diagram_node,
                    cross_section_node, material_type_node,
                    reinf_layout_node, reinf_tex_uniform_node,
                    reinf_tex_layer_node, reinf_bar_node]
