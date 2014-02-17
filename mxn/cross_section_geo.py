'''
Created on Jan 21, 2014

@author: rch
'''

from traits.api import HasStrictTraits, \
    Float, Property, cached_property, Int, \
    Trait, Event, on_trait_change, Instance, Button, Callable, \
    DelegatesTo, Constant, WeakRef, List

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from etsproxy.traits.ui.api import \
    View, Item, Group, HSplit, VGroup, HGroup

import numpy as np

from traitsui.api import \
    TableEditor, ObjectColumn, Label

class CrossSectionGeo(HasStrictTraits):
    '''Base class for cross section types.
    '''

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

class GeoRect(CrossSectionGeo):
    '''Rectangular cross section
    '''

    height = Float(0.3, auto_set=False, enter_set=True, geo_input=True)
    '''total height of cross section
    '''

    width = Float(0.2, auto_set=False, enter_set=True, geo_input=True)
    '''total width of cross section
    '''

    gravity_centre = Property(depends_on='+geo_input')
    '''z distance of gravity centre from upper rim
    '''
    def _get_gravity_centre(self):
        return self.height / 2

    def get_width(self, z):
        '''returns width of cross section for different vertical coordinates
        '''
        return self.width

    width_vct = Property()
    def _get_width_vct(self):
        return np.vectorize(self.get_width, otypes = [np.float])

    def plot_geometry(self, ax):
        '''Plot geometry'''
        dx, dz = 0.0, 0.0
        xdata = np.array([0, self.width, self.width, 0, 0], dtype=float)
        zdata = np.array([0, 0, self.height, self.height, 0], dtype=float)
        ax.plot(xdata + dx, zdata + dz, color='blue')
        ax.axis('equal')
        ax.axis([dx - 0.1 * self.width, dx + 1.1 * self.width, dz - 0.1 * self.height, dz + 1.1 * self.height])
        

    view = View(HSplit(Group(
                HGroup(
                Group(Item('width', springy=True),
                      Item('height'),
                      label='Geometry',
                      springy=True
                      ),
                springy=True,
                ),
                scrollable=True,
                ),
                Group(Item('replot', show_label=False),
                      Item('figure', editor=MPLFigureEditor(),
                           resizable=True, show_label=False),
                      id='simexdb.plot_sheet',
                      label='plot sheet',
                      dock='tab',
                      ),
                       ),
                width=0.8,
                height=0.7,
                resizable=True,
                buttons=['OK', 'Cancel'])

class GeoI(CrossSectionGeo):
    '''I-shaped cross section
    '''

    height = Float(0.6, auto_set=False, enter_set=True, geo_input=True)
    '''total height of crosssection
    '''

    height_up = Float(0.1, auto_set=False, enter_set=True, geo_input=True)
    '''height of upper flange
    '''

    height_lo = Float(0.1, auto_set=False, enter_set=True, geo_input=True)
    '''height of lower flange
    '''

    width_up = Float(0.4, auto_set=False, enter_set=True, geo_input=True)
    '''width of upper flange
    '''

    width_lo = Float(0.6, auto_set=False, enter_set=True, geo_input=True)
    '''width of lower flange
    '''

    width_st = Float(0.2, auto_set=False, enter_set=True, geo_input=True)
    '''width of stalk
    '''

    width = Property(depends_on='+geo_input')
    '''Width of cross section
    '''
    def _get_width(self):
        return max(self.width_lo, self.width_up)

    gravity_centre = Property(depends_on='+geo_input')
    '''z distance of gravity centre from upper rim
    '''
    def _get_gravity_centre(self):
        A_up, z_up = self.width_up * self.height_up, self.height_up / 2
        A_lo, z_lo = self.width_lo * self.height_lo, self.height - self.height_lo / 2
        A_st, z_st = self.width_st * (self.height - self.height_up - self.height_lo), (self.height + self.height_up - self.height_lo) / 2
        return (A_up*z_up + A_lo*z_lo + A_st*z_st) / (A_up + A_lo + A_st)
    
    def get_width(self, z):
        '''returns width of cross section for different vertical coordinates
        '''
        width = self.width_up + (np.sign(z-self.height_up)+1)/2 * (self.width_st - self.width_up) + \
        (np.sign(z-self.height + self.height_lo)+1)/2 * (self.width_lo - self.width_st)
        return width

    width_vct = Property()
    def _get_width_vct(self):
        return np.vectorize(self.get_width, otypes = [np.float])
        
    def plot_geometry(self, ax):
        '''Plot geometry'''
        w_max = self.width
       
        dx, dz = 0.0, 0.0

        xdata = np.array([- self.width_lo / 2, self.width_lo / 2, self.width_lo / 2, self.width_st / 2,
                          self.width_st / 2, self.width_up / 2, self.width_up / 2, - self.width_up / 2,
                          - self.width_up / 2, - self.width_st / 2, - self.width_st / 2,
                          - self.width_lo / 2, - self.width_lo / 2], dtype=float) + w_max / 2
                          
        zdata = np.array([0, 0, self.height_lo, self.height_lo, self.height - self.height_up,
                          self.height - self.height_up, self.height, self.height, self.height - self.height_up,
                          self.height - self.height_up, self.height_lo, self.height_lo, 0], dtype=float)

        ax.plot(xdata + dx, zdata + dz, color='blue')

        ax.axis('equal')
        ax.axis([dx - 0.1 * w_max, dx + 1.1 * w_max, dz - 0.1 * self.height, dz + 1.1 * self.height])

    view = View(HSplit(Group(
                HGroup(
                Group(Item('width_up', springy=True),
                      Item('width_lo'),
                      Item('width_st'),
                      Item('height'),
                      Item('height_lo'),
                      Item('height_up'),
                      label='Geometry',
                      springy=True
                      ),
                springy=True,
                ),
                scrollable=True,
                ),
                Group(Item('replot', show_label=False),
                      Item('figure', editor=MPLFigureEditor(),
                           resizable=True, show_label=False),
                      id='simexdb.plot_sheet',
                      label='plot sheet',
                      dock='tab',
                      ),
                       ),
                width=0.8,
                height=0.7,
                resizable=True,
                buttons=['OK', 'Cancel'])

class GeoCirc(CrossSectionGeo):
    '''Circular shaped cross section
    '''

    radius = Float(0.3, auto_set=False, enter_set=True, geo_input=True)
    '''radius of cross section
    '''
    
    height = Property(depends_on='radius')
    '''Height of cross section
    '''
    def _get_height(self):
        return 2 * self.radius

    width = Property(depends_on='radius')
    '''Width of cross section
    '''
    def _get_width(self):
        return 2 * self.radius

    gravity_centre = Property(depends_on='+geo_input')
    '''z distance of gravity centre from upper rim
    '''
    def _get_gravity_centre(self):
        return self.radius

    def get_width(self, z):
        '''returns width of cross section for given vertical coordinate
        '''
        r_dist = z - self.radius
        '''transfer distance from top to distance from center
        '''
        width = 2 * np.sqrt(self.radius ** 2 - r_dist ** 2)
        return width

    width_vct = Property()
    def _get_width_vct(self):
        return np.vectorize(self.get_width, otypes = [np.float])
        
    def plot_geometry(self, ax):
        '''Plot geometry'''
        dx, dz = self.radius, self.radius
        #fi_outline_arr = np.append(np.arange(0, 2 * np.pi, np.pi / 60, dtype=float), 0.0)
        fi_outline_arr = np.linspace(0, 2 * np.pi, 60)

        ax.plot(np.cos(fi_outline_arr) * self.radius + dx, np.sin(fi_outline_arr) * self.radius + dz, color='blue')
        ax.axis('equal')
        ax.axis([dx - self.radius * 1.1, dx + self.radius * 1.1, dz - self.radius * 1.1, dz + self.radius * 1.1])

    view = View(HSplit(Group(
                HGroup(
                Group(Item('radius', springy=True),
                      label='Geometry',
                      springy=True
                      ),
                springy=True,
                ),
                scrollable=True,
                ),
                Group(Item('replot', show_label=False),
                      Item('figure', editor=MPLFigureEditor(),
                           resizable=True, show_label=False),
                      id='simexdb.plot_sheet',
                      label='plot sheet',
                      dock='tab',
                      ),
                       ),
                width=0.8,
                height=0.7,
                resizable=True,
                buttons=['OK', 'Cancel'])

if __name__ == '__main__':

    ecs = GeoI(width_up=0.8, width_lo=0.5)

    ecs.configure_traits()
