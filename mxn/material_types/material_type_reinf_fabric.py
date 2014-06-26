'''
Created on 23. 4. 2014

@author: Vancikv
'''

from traits.api import \
    Property, cached_property, Dict, Str, \
    Float

from traitsui.api import \
    View, Item

from mxn.view import \
    MxNClassExt

from reinf_laws import \
    ReinfLawBase, ReinfLawBilinear, \
    ReinfLawCubic, ReinfLawFBM, \
    ReinfLawLinear

from material_type_base import \
    MaterialTypeBase

basic_laws = { 'bilinear':
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

class MTReinfFabric(MaterialTypeBase):

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

    #===========================================================================
    # UI-related functionality
    #===========================================================================

    traits_view = View(Item('A_roving'),
                      Item('s_0'),
                      Item('s_90'),
                      )

MTReinfFabric.db = MxNClassExt(
            klass=MTReinfFabric,
            verbose='io',
            node_name='Reinforcement fabrics'
            )

print 'XXXXX'
if MTReinfFabric.db.get('default_fabric', None):
    del MTReinfFabric.db['default_fabric']
MTReinfFabric.db['default_fabric'] = MTReinfFabric()
