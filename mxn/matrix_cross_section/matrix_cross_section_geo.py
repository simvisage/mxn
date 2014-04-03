'''
Created on Jan 21, 2014

@author: rch
'''

from traits.api import HasStrictTraits, \
    Event, on_trait_change, Instance, Button

from matplotlib.figure import \
    Figure

class MCSGeo(HasStrictTraits):
    '''Base class for cross section types.
    '''
    changed = Event
    @on_trait_change('+geo_input')
    def set_changed(self):
        self.changed = True
      
    def plot_geometry(self, ax):
        '''Plot geometry'''


if __name__ == '__main__':

    #ecs = GeoI()
    #ecs.configure_traits()
    pass
