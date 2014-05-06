'''
Created on 23. 4. 2014

@author: Vancikv
'''

from traits.api import \
    Property, cached_property, Dict, Str, \
    Float, on_trait_change

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

    s_0 = Float(0.02, auto_set=False, enter_set=True, geo_input=True)
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

if not ReinfFabric.db.get('default_fabric', None):
    ReinfFabric.db['default_fabric'] = ReinfFabric()