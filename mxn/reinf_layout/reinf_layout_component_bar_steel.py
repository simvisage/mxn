'''
Created on 25. 2. 2014

@author: Vancikv
'''

from reinf_layout_component_bar import \
    RLCBar

from mxn.reinf_laws import \
    ReinfLawBase

from etsproxy.traits.api import \
    Property, cached_property, \
    Trait, Instance, Button

class RLCSteelBar(RLCBar):
    '''Steel reinforcement bar
    '''
    node_name = 'Steel bar'
    ecb_law = 'steel-default'

if __name__ == '__main__':
    bar = RLCSteelBar()
    print bar.x
