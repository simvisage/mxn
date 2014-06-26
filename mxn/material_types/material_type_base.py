'''
Created on 26. 6. 2014

@author: Vancikv
'''

from traits.api import \
    Property, cached_property, Dict, Str, \
    on_trait_change, List

from mxn.view import \
    MxNTreeNode

from matresdev.db.simdb import \
    SimDBClass

from mxn.constitutive_law import \
    CLBase

import weakref

class MaterialTypeBase(MxNTreeNode, SimDBClass):

    mtrl_laws = Dict((Str, CLBase))

    #===========================================================================
    # Management of backward links
    #===========================================================================

    state_link_lst = List(transient=True)
    '''List of backward links to objects using the fabric
    '''
    def _state_link_lst_default(self):
        return []

    @on_trait_change('+geo_input,+law_input')
    def notify_change(self):
        for link in self.state_link_lst:
            if link():
                link().material_changed = True

    def add_link(self, link_to_add):
        '''Adding a backward link to the list - to be called
        from objects using the fabric
        '''
        if link_to_add not in self.state_link_lst:
            self.state_link_lst.append(weakref.ref(link_to_add))

    def del_link(self, link_to_del):
        '''Removing a backward link from the list - to be called
        from objects using the fabric
        '''
        self.state_link_lst[:] = [link for link in self.state_link_lst if link() != link_to_del]

    #===========================================================================
    # UI-related functionality
    #===========================================================================

    tree_node_list = Property(depends_on='mtrl_laws')
    @cached_property
    def _get_tree_node_list(self):
        return self.named_mtrl_laws.values()