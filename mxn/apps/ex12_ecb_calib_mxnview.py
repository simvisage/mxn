'''
Created on 1. 4. 2014

@author: Vancikv
'''

from mxn import \
    ECBCalib, \
    MxNTreeNode, MxNTreeView

from mxn.material_types import \
    MTMatrixMixture, MTReinfFabric, MTReinfBar

ec = ECBCalib(Mu=3.49)

database_root_node = MxNTreeNode(tree_node_list=[MTMatrixMixture.db, MTReinfFabric.db,
                                                 MTReinfBar.db], node_name='Material database')

root_node = MxNTreeNode(tree_node_list=[database_root_node, ec],
                                 node_name='Calibration / Database')

ecw = MxNTreeView(root=root_node)
ecw.configure_traits()
