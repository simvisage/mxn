'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.

@author: rch
'''
from etsproxy.traits.api import \
    HasStrictTraits, Float, Property, cached_property, Int, \
    Event, on_trait_change, DelegatesTo, Instance, WeakRef, Constant

from etsproxy.traits.ui.api import \
    View, Item, Group, HGroup

from cross_section_state import \
    CrossSectionState

from mxn.view import \
    MxNTreeNode

import numpy as np


COMPONENT_CHANGE = '+geo_input,+law_input,geo.changed'

class CrossSectionComponent(MxNTreeNode):
    '''Cross section component supplying the normal force and moment..
    '''
    state = WeakRef(CrossSectionState)
    '''Strain state of a cross section
    '''

    unit_conversion_factor = Constant(1000.0)

    eps_changed = Event
    '''State notifier that is set to true if the cross section state has changed
    upon modifications of eps_lo and eps_up
    '''

    @on_trait_change(COMPONENT_CHANGE)
    def notify_change(self):
        '''Propagate the change of the component geometry or stress-strain 
        law to the cross section state.
        '''
        if self.state:
            self.state.changed = True


    #===========================================================================
    # Cross-sectional stress resultants
    #===========================================================================

    N = Property()
    '''Resulting normal force.
    '''

    M = Property()
    '''Resulting moment.
    '''

if __name__ == '__main__':
    #ecs.configure_traits()
    pass
