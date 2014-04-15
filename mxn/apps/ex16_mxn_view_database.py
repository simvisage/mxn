'''
Created on 14. 4. 2014

@author: Vancikv
'''

from mxn.view import \
    MxNTreeView, MxNTreeNode

from mxn import \
    MatrixMixture

database_root_node = MxNTreeNode(tree_node_list=[MatrixMixture.db,
                                                 ], node_name='database')
database_view = MxNTreeView(root=database_root_node)
database_view.configure_traits()
