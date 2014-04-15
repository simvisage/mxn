'''
Created on 14. 4. 2014

@author: Vancikv
'''

from traits.api import \
    Property

from matresdev.db.simdb import \
    SimDBClassExt

from mxn_tree_node import \
    MxNTreeNode
    
class MxNClassExt(SimDBClassExt, MxNTreeNode):
    node_name = 'database'
    
    tree_node_list = Property
    def _get_tree_node_list(self):
        for inst in self.inst_list:
            inst.node_name = inst.key
        return self.inst_list
 
