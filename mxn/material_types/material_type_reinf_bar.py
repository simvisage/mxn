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

from mxn.reinf_laws import \
    ReinfLawBase, ReinfLawSteel

from material_type_base import \
    MaterialTypeBase

basic_laws = { 'steel':
               ReinfLawSteel(f_yk=500., E_s=200000., eps_u=0.025),
               }

class MTReinfBar(MaterialTypeBase):

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
    # UI-related functionality
    #===========================================================================

    traits_view = View(Item('area'),
                      )

MTReinfBar.db = MxNClassExt(
            klass=MTReinfBar,
            verbose='io',
            node_name='Reinforcement fabrics'
            )

print 'XXXXX'
if MTReinfBar.db.get('bar_d10', None):
    del MTReinfBar.db['bar_d10']
MTReinfBar.db['bar_d10'] = MTReinfBar(area=0.0000785)