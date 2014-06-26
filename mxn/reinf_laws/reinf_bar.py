'''
Created on 23. 4. 2014

@author: Vancikv
'''

from traits.api import \
    Property, cached_property, Dict, Str, \
    Float, on_trait_change, List, WeakRef, \
    Trait

from traitsui.api import \
    View, Item

from mxn.view import \
    MxNTreeNode, MxNClassExt

from matresdev.db.simdb import \
    SimDBClass

from reinf_law_base import \
    ReinfLawBase

from reinf_law_steel import \
    ReinfLawSteel

import weakref

basic_laws = { 'steel':
               ReinfLawSteel(f_yk=500., E_s=200000., eps_u=0.025),
               }

class ReinfBar(MxNTreeNode, SimDBClass):

    area = Float(0.0000785, auto_set=False, enter_set=True, geo_input=True)
    '''Cross section area [m**2]'''

    mtrl_laws = Dict((Str, ReinfLawBase))
    def _mtrl_laws_default(self):
        return basic_laws

    named_mtrl_laws = Property(depends_on='mtrl_laws')
    @cached_property
    def _get_named_mtrl_laws(self):
        for key, mtrl_law in self.mtrl_laws.items():
            mtrl_law.node_name = key
        return self.mtrl_laws

    #===========================================================================
    # Management of backward links
    #===========================================================================

    state_link_lst = List(transient=True)
    '''List of backward links to objects using the fabric
    '''
    def _state_link_lst_default(self):
        return []

    @on_trait_change('+geo_input')
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

    traits_view = View(Item('area'),
                      )

ReinfBar.db = MxNClassExt(
            klass=ReinfBar,
            verbose='io',
            node_name='Reinforcement fabrics'
            )

print 'XXXXX'
if ReinfBar.db.get('bar_d10', None):
    del ReinfBar.db['bar_d10']
ReinfBar.db['bar_d10'] = ReinfBar(area=0.0000785)
