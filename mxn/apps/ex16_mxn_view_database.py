'''
Created on 14. 4. 2014

@author: Vancikv
'''

from mxn.view import \
    MxNTreeView, MxNTreeNode

from mxn.material_types import \
    MTMatrixMixture, MTReinfFabric, MTReinfBar

database_root_node = MxNTreeNode(tree_node_list=[MTMatrixMixture.db, MTReinfFabric.db,
                                                 MTReinfBar.db], node_name='Material database')
database_view = MxNTreeView(root=database_root_node)
database_view.configure_traits()
