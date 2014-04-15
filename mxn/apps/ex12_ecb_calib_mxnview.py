'''
Created on 1. 4. 2014

@author: Vancikv
'''

from mxn import \
    ECBCalib, \
    MatrixLawBase, ReinfLawBase, \
    MxNTreeNode, MxNTreeView

ec = ECBCalib(Mu=3.49)

root_node = MxNTreeNode(tree_node_list=[MatrixLawBase.db,
                                                 ReinfLawBase.db,
                                                 ec],
                                 node_name='database')

ecw = MxNTreeView(root=root_node)
ecw.configure_traits()
