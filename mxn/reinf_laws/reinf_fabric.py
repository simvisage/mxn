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

from reinf_law_bilinear import \
    ReinfLawBilinear

from reinf_law_cubic import \
    ReinfLawCubic

from reinf_law_fbm import \
    ReinfLawFBM

from reinf_law_linear import \
    ReinfLawLinear
#
# from mxn.utils import \
#     KeyRef

import weakref

basic_laws = {'bilinear':
               ReinfLawBilinear(sig_tex_u=1216., eps_u=0.014,
                                var_a=0.8, eps_el_fraction=0.0001),
              'cubic':
               ReinfLawCubic(sig_tex_u=1216., eps_u=0.016,
                                var_a=-5e+6),
              'fbm':
               ReinfLawFBM(sig_tex_u=1216., eps_u=0.014,
                           m=0.5),
              'linear':
               ReinfLawLinear(eps_u=0.014, E_tex=80000.),
               }

class ReinfFabric(MxNTreeNode, SimDBClass):

    A_roving = Float(0.461, auto_set=False, enter_set=True, geo_input=True)
    '''Cross section of one roving [mm**2]'''

    s_0 = Float(0.0083, auto_set=False, enter_set=True, geo_input=True)
    '''Distance between rovings oriented in 0-direction [m]'''

    s_90 = Float(0.02, auto_set=False, enter_set=True, geo_input=True)
    '''Distance between rovings oriented in 90-direction [m]'''

    mtrl_laws = Dict((Str, ReinfLawBase))
    def _mtrl_laws_default(self):
        return basic_laws

    named_mtrl_laws = Property(depends_on='mtrl_laws')
    @cached_property
    def _get_named_mtrl_laws(self):
        for key, mtrl_law in self.mtrl_laws.items():
            mtrl_law.node_name = key
        return self.mtrl_laws

    def get_mtrl_law(self, key):
        law = self.named_mtrl_laws[key]
        return law

#     def link_mat_laws(self, obj, trait_name):
#         if trait_name in obj.trait_names():
#             obj.remove_trait(trait_name)
#         print 'linking fabric law database to reinforcement element %s' % obj
#         print obj.trait_names()
#         law_trait = Trait('fbm', self.named_mtrl_laws)
#         obj.add_trait(trait_name, law_trait)
#         print obj.trait_names()

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
                link().fabric_changed = True

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

    traits_view = View(Item('A_roving'),
                      Item('s_0'),
                      Item('s_90'),
                      )

ReinfFabric.db = MxNClassExt(
            klass=ReinfFabric,
            verbose='io',
            node_name='Reinforcement fabrics'
            )

print 'XXXXX'
if ReinfFabric.db.get('default_fabric', None):
    del ReinfFabric.db['default_fabric']
ReinfFabric.db['default_fabric'] = ReinfFabric()
