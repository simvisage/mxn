'''
Created on Sep 4, 2012

@todo: introduce the dock feature for the views
@todo: classify the state changes and provide examples.

@author: rch
'''
from etsproxy.traits.api import \
    HasStrictTraits, Property, \
    Event, on_trait_change, WeakRef, Constant

from cross_section_state import \
    CrossSectionState

from mxn.view import \
    MxNTreeNode

COMPONENT_CHANGE = '+geo_input,+law_input,geo.changed,law_changed'

class CrossSectionComponent(MxNTreeNode):
    '''Cross section component supplying the normal force and moment..
    '''
    state = WeakRef(CrossSectionState, transient=True)
    '''Strain state of a cross section
    '''
    
    def __getstate__ ( self ):
        '''Overriding __getstate__ because of WeakRef usage
        '''
        state = super( HasStrictTraits, self ).__getstate__()
        
        for key in [ 'state', 'state_', 'plot_state', 'plot_state_' ]:
            if state.has_key( key ):
                del state[ key ]
                
        return state    


    unit_conversion_factor = Constant(1000.0)
    
    law_changed = Event
    '''Notifier set to True when internal values of a constitutive law change
    '''

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
    pass
