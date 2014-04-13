'''
Created on 27. 2. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    Instance, Property, cached_property, Event, Button

from etsproxy.traits.ui.api import \
    TreeEditor, TreeNode, View, Item, Group, HSplit, \
    ModelView, VGroup, HGroup

from cross_section import \
    CrossSection

from reinf_laws import \
    ReinfLawBase

from ecb_calib import \
    ECBCalib

from util.traits.editors.mpl_figure_editor import  \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from matresdev.db.simdb import SimDB
simdb = SimDB()

class ECBCalibModelView(ModelView):
    '''Model in a viewable window.
    '''
    model = Instance(ECBCalib)
    def _model_default(self):
        return ECBCalib()

    cs_state = Property(Instance(CrossSection), depends_on='model')
    @cached_property
    def _get_cs_state(self):
        return self.model.cs

    data_changed = Event

    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        return figure

    replot = Button()
    def _replot_fired(self):
        ax = self.figure.add_subplot(1, 1, 1)
        self.model.calibrated_ecb_law.plot_ax(ax)
        self.data_changed = True

    clear = Button()
    def _clear_fired(self):
        self.figure.clear()
        self.data_changed = True

    calibrated_ecb_law = Property(Instance(ReinfLawBase), depends_on='model')
    @cached_property
    def _get_calibrated_ecb_law(self):
        return self.model.calibrated_ecb_law

    view = View(HSplit(VGroup(
                       Item('cs_state', label='Cross section', show_label=False),
                       Item('model@', show_label=False),
                       Item('calibrated_ecb_law@', show_label=False, resizable=True),
                       ),
                       Group(HGroup(
                             Item('replot', show_label=False),
                             Item('clear', show_label=False),
                      ),
                      Item('figure', editor=MPLFigureEditor(),
                           resizable=True, show_label=False),
                      id='simexdb.plot_sheet',
                      label='plot sheet',
                      dock='tab',
                      ),
                       ),
                width=0.5,
                height=0.4,
                buttons=['OK', 'Cancel'],
                resizable=True)
