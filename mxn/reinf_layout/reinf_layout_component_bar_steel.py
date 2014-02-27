'''
Created on 25. 2. 2014

@author: Vancikv
'''

from reinf_layout_component_bar import \
    RLCBar
    
from etsproxy.traits.api import \
    Property, cached_property, \
    Trait, Instance, Button, WeakRef

class RLCSteelBar(RLCBar):
    '''Steel reinforcement bar
    '''
    name = 'Steel bar'
    ecb_law_type = 'steel'
    def _get_ecb_law(self):
        return self.ecb_law_type_(f_yk=500., E_s=200000., eps_s_u=0.025)

if __name__ == '__main__':
    bar = RLCSteelBar()
    print bar.position