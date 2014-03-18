'''
Created on Sep 4, 2012

@author: rch
'''
from etsproxy.traits.api import \
    HasTraits, Int, Instance, Property, cached_property, DelegatesTo, \
    Event, Button

from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from etsproxy.traits.ui.api import \
    View, Item, Group, HSplit, VGroup, HGroup, RangeEditor, InstanceEditor

from ecb_calib import \
    ECBCalib

from cross_section import \
    CrossSection

from reinf_layout import \
    RLCTexUniform

from matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

import numpy as np

class MxNDiagram(HasTraits):

    # calibrator supplying the effective material law
    calib = Instance(ECBCalib)
    def _calib_changed(self):
        c = self.calib.calibrated_ecb_law
        self.cs = self.calib.cs
        self.calib.notify_change = self.set_modified
            
    modified = Event
    def set_modified(self):
        self.modified = True

    # cross section
    cs = Instance(CrossSection)
    def _cs_default(self):
        return CrossSection()
            
    eps_cu = Property()
    def _get_eps_cu(self):
        return -self.cs.matrix_cs_with_state.cc_law.eps_c_u

    eps_tu = Property()
    def _get_eps_tu(self):
        eps = 0
        for r in self.cs.reinf_components_with_state:
            if eps < r.ecb_law.eps_u:
                eps = r.ecb_law.eps_u
        return eps

    n_eps = Int(5, auto_set=False, enter_set=True)
    eps_range = Property(depends_on='n_eps')
    @cached_property
    def _get_eps_range(self):
        eps_c_space = np.linspace(self.eps_cu, 0, self.n_eps)
        eps_t_space = np.linspace(0, self.eps_tu, self.n_eps)

        eps_ccu = 0.8 * self.eps_cu

        #eps_cc = self.eps_cu * np.ones_like(eps_c_space)
        eps_cc = np.linspace(eps_ccu, self.eps_cu, self.n_eps)
        eps_ct = self.eps_cu * np.ones_like(eps_t_space)
        eps_tc = self.eps_tu * np.ones_like(eps_c_space)
        eps_tt = self.eps_tu * np.ones_like(eps_t_space)

        eps1 = np.vstack([eps_c_space, eps_cc])
        eps2 = np.vstack([eps_t_space, eps_ct])
        eps3 = np.vstack([eps_tc, eps_c_space])
        eps4 = np.vstack([eps_tt, eps_t_space])

        return np.hstack([eps1, eps2, eps3, eps4])

    n_eps_range = Property(depends_on='n_eps')
    @cached_property
    def _get_n_eps_range(self):
        return self.eps_range.shape[1]
    #===========================================================================
    # MN Diagram
    #===========================================================================

    def _get_MN_fn(self, eps_lo, eps_up):
        self.cs.set(eps_lo=eps_lo,
                    eps_up=eps_up)
        return (self.cs.M, self.cs.N)

    MN_vct = Property(depends_on='modified')
    def _get_MN_vct(self):
        return np.vectorize(self._get_MN_fn)

    MN_arr = Property(depends_on='modified,n_eps')
    @cached_property
    def _get_MN_arr(self):
        return self.MN_vct(self.eps_range[0, :], self.eps_range[1, :])

    #===========================================================================
    # f_eps Diagram
    #===========================================================================

    current_eps_idx = Int(0) # , auto_set = False, enter_set = True)

    current_eps = Property(depends_on='current_eps_idx')
    @cached_property
    def _get_current_eps(self):
        return self.eps_range[(0, 1), self.current_eps_idx]

    current_MN = Property(depends_on='current_eps_idx')
    @cached_property
    def _get_current_MN(self):
        return self._get_MN_fn(*self.current_eps)

    view = View(HSplit(Group(
                HGroup(
                Group(Item('n_eps', springy=True),
                      label='Discretization',
                      springy=True
                      ),
                springy=True,
                ),
                HGroup(
                Group(VGroup(
                      Item('cs', label='Cross section', show_label=False, springy=True,
                           editor=InstanceEditor(kind='live'),
                           ),
                      Item('calib', label='Calibration', show_label=False, springy=True,
                           editor=InstanceEditor(kind='live'),
                           ),
                      springy=True,
                      ),
                      label='Cross section',
                      springy=True
                      ),
                springy=True,
                ),
                scrollable=True,
                ),
                ),
                width=1.0,
                height=0.8,
                resizable=True,
                buttons=['OK', 'Cancel'])

if __name__ == '__main__':
    rf = RLCTexUniform(n_layers=12,ecb_law_type='fbm')
    mx = MatrixCrossSection(geo=MCSGeoRect(width=0.2, height=0.06), n_cj=20, cc_law_type='quadratic')    
    cs1 = CrossSection(reinf = [rf], matrix_cs = mx)
    
    c = ECBCalib(Mu=3.49, cs = cs1)

    mn = MxNDiagram(calib=c, n_eps=5)

    print mn.MN_arr
    mn.configure_traits()

