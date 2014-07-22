'''
Created on 1. 7. 2014

@author: Vancikv
'''

from mxn.mxn_tree_node import \
    MxNTreeNode

from mxn.material_types import \
    MTMatrixMixture, MTReinfFabric, MTReinfBar

class UCDatabase(MxNTreeNode):
    node_name = 'Material database'

    tree_node_list = [MTMatrixMixture.db,
                      MTReinfFabric.db,
                      MTReinfBar.db]
