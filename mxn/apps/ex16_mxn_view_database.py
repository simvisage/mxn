'''
Created on 14. 4. 2014

@author: Vancikv
'''

from mxn.view import \
    MxNTreeView, MxNTreeNode

from mxn.matrix_laws import \
    MatrixLawBase
    
from mxn.reinf_laws import \
    ReinfLawBase
    
database_root_node = MxNTreeNode(tree_node_list=[MatrixLawBase.db, 
                            ReinfLawBase.db], node_name='database')
database_view = MxNTreeView(root=database_root_node)
database_view.configure_traits()