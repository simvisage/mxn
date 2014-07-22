'''
Created on 9. 7. 2014

@author: Vancikv
'''

from traitsui.api import \
    TreeNode

from traitsui.menu import \
    Menu

from mxn_tree_view_handler import \
    plot_self, new_material, del_material

from traitsui.wx.tree_editor import \
    NewAction, DeleteAction, CopyAction, PasteAction

from mxn.mxn_diagram import \
    MxNDiagram

from mxn.cross_section import \
    CrossSection

from mxn.use_cases import \
    UCDatabase, UCPStudyElementMxN, UCParametricStudy, \
    UseCaseContainer

from mxn.utils import \
    get_outfile

from mxn.material_types import \
    MaterialTypeBase

from mxn.mxn_tree_node import \
    ReinfLayoutTreeNode

from mxn.reinf_layout import \
    RLCTexLayer, RLCTexUniform, RLCBar

from mxn.mxn_class_extension import \
    MxNClassExt

from mxn.ecb_calib import \
    ECBCalib

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

use_case_container_node = TreeNode(
                                     node_for=[UseCaseContainer],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(NewAction),
                                     add=[MxNDiagram, UCParametricStudy,
                                          ECBCalib],
                                     )

parametric_study_node = TreeNode(
                                     node_for=[UCParametricStudy],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(NewAction),
                                     add=[],
                                     )

mxn_diagram_container_node = SingleChildTreeNode(
                                     node_for=[UCPStudyElementMxN],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(plot_self,
                                               PasteAction,
                                               DeleteAction),
                                     add=[MxNDiagram],
                                     )

mxn_diagram_node = SingleChildTreeNode(node_for=[MxNDiagram],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     add=[CrossSection],
                                     menu=Menu(plot_self,
                                               CopyAction,
                                               PasteAction,
                                               DeleteAction),
                                     )

ecb_calib_node = SingleChildTreeNode(node_for=[ECBCalib],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     add=[CrossSection],
                                     menu=Menu(plot_self,
                                               CopyAction,
                                               PasteAction,
                                               DeleteAction),
                                     )
#===============================================================================
# Database and subordinates
#===============================================================================

''' Generic nodes are used for constitutive laws
'''

database_node = TreeNode(node_for=[UCDatabase],
                                     auto_open=False,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(),
                                     )

database_subnode = TreeNode(node_for=[MxNClassExt],
                                     auto_open=True,
                                     children='tree_node_list',
                                     label='node_name',
                                     view='tree_view',
                                     menu=Menu(new_material),
                                     )

material_type_node = TreeNode(node_for=[MaterialTypeBase],
                              auto_open=False,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(del_material),
                              )

#===============================================================================
# Cross section and subordinates
#===============================================================================

''' Generic nodes are used for MatrixCrossSection and for constitutive laws
'''

cross_section_node = TreeNode(node_for=[CrossSection],
                              auto_open=True,
                              children='tree_node_list',
                              label='node_name',
                              view='tree_view',
                              menu=Menu(CopyAction, plot_self),
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

#===============================================================================
# List of all custom nodes
#===============================================================================

custom_node_list = [mxn_diagram_container_node, mxn_diagram_node,
                    cross_section_node, material_type_node,
                    reinf_layout_node, reinf_tex_uniform_node,
                    reinf_tex_layer_node, reinf_bar_node,
                    database_node, database_subnode, ecb_calib_node,
                    use_case_container_node, parametric_study_node]
