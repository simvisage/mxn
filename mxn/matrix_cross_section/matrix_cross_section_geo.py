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

    #===========================================================================
    # Plotting of the cross section
    #===========================================================================
    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        figure.add_axes([0.08, 0.13, 0.85, 0.74])
        return figure

    data_changed = Event

    replot = Button
    def _replot_fired(self):

        self.figure.clear()
        fig = self.figure
        ax = fig.add_subplot(111)

        self.plot_geometry(ax)

        self.data_changed = True
        
    def plot_geometry(self, ax):
        '''Plot geometry'''


if __name__ == '__main__':

    #ecs = GeoI()
    #ecs.configure_traits()
    pass
