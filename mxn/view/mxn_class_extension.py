'''
Created on 14. 4. 2014

@author: Vancikv
'''

from traits.api import \
    Property, Button

from matresdev.db.simdb import \
    SimDBClassExt

from mxn_tree_node import \
    MxNTreeNode

from traitsui.api import \
    View, Item

from mxn_class_extension_handler import \
    MxNClassExtHandler

class MxNClassExt(SimDBClassExt, MxNTreeNode):
    node_name = 'database'

    def __setitem__(self, key, value):
        super(MxNClassExt, self).__setitem__(key, value)
        self.instances[key].key = key
        self.instances[key].node_name = key

    new_material = Button(label='Make new material')
    def _new_material_fired(self):
        pass

    tree_node_list = Property
    def _get_tree_node_list(self):
        for inst in self.inst_list:
            inst.node_name = inst.key
        return self.inst_list

    tree_view = View(Item('new_material'), handler=MxNClassExtHandler())

