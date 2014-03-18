'''
Created on 15. 3. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    HasStrictTraits, Int, Instance, Property, cached_property, DelegatesTo, \
    Event, Button

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from etsproxy.traits.ui.api import \
    View, Item, Group, HSplit, VGroup, HGroup, RangeEditor, InstanceEditor

from ecb_calib import \
    ECBCalib

from mxn_diagram import \
    MxNDiagram

class MxNDiagramView(HasStrictTraits):
    mxn = Instance(MxNDiagram)
    current_eps_idx = DelegatesTo('mxn')

    def _current_eps_idx_changed(self):
        self._clear_fired()
        self._replot_fired()

    n_eps_range = DelegatesTo('mxn')
    
    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        return figure

    data_changed = Event

    clear = Button
    def _clear_fired(self):
        self.figure.clear()
        self.data_changed = True

    replot = Button
    def _replot_fired(self):

        ax = self.figure.add_subplot(2, 2, 1)

        ax.plot(-self.mxn.eps_range, [0, self.mxn.cs.matrix_cs_with_state.geo.height], color='black')

        ax.plot(-self.mxn.current_eps, [0, self.mxn.cs.matrix_cs_with_state.geo.height], lw=3, color='red')

        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        ax = self.figure.add_subplot(2, 2, 2)

        ax.plot(self.mxn.MN_arr[0], -self.mxn.MN_arr[1], lw=2, color='blue')
        ax.plot(self.mxn.current_MN[0], -self.mxn.current_MN[1], 'g.', markersize=20.0, color='red')

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(b=None, which='major')

        self.mxn.cs.set(eps_lo=self.mxn.current_eps[0],
                    eps_up=self.mxn.current_eps[1])

        ax = self.figure.add_subplot(2, 2, 3)

        self.mxn.cs.plot_eps(ax)

        ax = self.figure.add_subplot(2, 2, 4)

        self.mxn.cs.plot_sig(ax)

        self.data_changed = True

    view = View(HSplit(Item('mxn@',show_label=False,springy=True),
                Group(HGroup(
                             Item('replot', show_label=False),
                             Item('clear', show_label=False),
                      ),
                      Item('current_eps_idx', editor=RangeEditor(low=0,
                                   high_name='n_eps_range',
                                   format='(%s)',
                                   mode='slider',
                                   auto_set=False,
                                   enter_set=False,
                                   ),
                           show_label=False,
                           ),
                      Item('figure', editor=MPLFigureEditor(),
                           resizable=True, show_label=False),
                      id='simexdb.plot_sheet',
                      label='plot sheet',
                      dock='tab',
                      ),
                       ),
                width=1.0,
                height=0.8,
                resizable=True,
                buttons=['OK', 'Cancel'])
