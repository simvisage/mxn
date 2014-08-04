'''
Created on Sep 4, 2012

@author: rch
'''
from traits.api import \
    Int, Instance, Property, \
    cached_property, Event, List, \
    on_trait_change

from traitsui.api import \
    View, Item, Group, HSplit, VGroup, \
    HGroup, RangeEditor, InstanceEditor

from mxn.mxn_tree_node import \
    MxNTreeNode

from mxn.cross_section import \
    CrossSection

from mxn.reinf_layout import \
    RLCTexUniform

import numpy as np

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

class MxNDiagram(MxNTreeNode):

    modified = Event
    def set_modified(self):
        self.modified = True

    tree_node_list = List(Instance(CrossSection))
    def _tree_node_list_default(self):
        return [CrossSection(notify_change_ext=self.set_modified,
                            reinf=[RLCTexUniform(n_layers=12, material='default_fabric')],
                            matrix_cs=MatrixCrossSection(geo=MCSGeoRect(width=0.2,
                                        height=0.06), n_cj=20, material='default_mixture',
                                                            material_law='constant'))]

    @on_trait_change('tree_node_list')
    def cs_changed(self):
        self.modified = True

    cs = Property(depends_on='tree_node_list')
    def _get_cs(self):
        val = self.tree_node_list[0]
        val.notify_change_ext = self.set_modified
        return val
    def _set_cs(self, val):
        self.tree_node_list = [val]

    eps_cu = Property()
    def _get_eps_cu(self):
        return -self.cs.matrix_cs_with_state.material_law_.eps_c_u

    eps_tu = Property()
    def _get_eps_tu(self):
        eps_lo_arr = [r.converted_eps_u_2_lo for r in self.cs.reinf_components_with_state]
        eps_tu = np.max(np.hstack([[0], eps_lo_arr]))
        return eps_tu

    n_eps = Int(20, auto_set=False, enter_set=True)
    eps_range = Property(depends_on='n_eps,modified')
    @cached_property
    def _get_eps_range(self):
        eps_c_space = np.linspace(self.eps_cu, 0, self.n_eps)
        eps_t_space = np.linspace(0, self.eps_tu, self.n_eps)

        eps_ccu = 0.8 * self.eps_cu

        # eps_cc = self.eps_cu * np.ones_like(eps_c_space)
        eps_cc = np.linspace(eps_ccu, self.eps_cu, self.n_eps)
        eps_ct = self.eps_cu * np.ones_like(eps_t_space)
        eps_tc = self.eps_tu * np.ones_like(eps_c_space)
        eps_tt = self.eps_tu * np.ones_like(eps_t_space)

        eps1 = np.vstack([eps_c_space, eps_cc])
        eps2 = np.vstack([eps_t_space, eps_ct])
        eps3 = np.vstack([eps_tc, eps_c_space])
        eps4 = np.vstack([eps_tt, eps_t_space])

        return np.hstack([eps1, eps2, eps3, eps4])

    n_eps_range = Property(depends_on='n_eps,modified')
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

    MN_vct = Property()
    def _get_MN_vct(self):
        return np.vectorize(self._get_MN_fn)

    MN_arr = Property(depends_on='modified,n_eps')
    @cached_property
    def _get_MN_arr(self):
        return self.MN_vct(self.eps_range[0, :], self.eps_range[1, :])

    #===========================================================================
    # f_eps Diagram
    #===========================================================================

    current_eps_idx = Int(1)  # , auto_set = False, enter_set = True)

    current_eps = Property(depends_on='current_eps_idx,modified')
    @cached_property
    def _get_current_eps(self):
        return self.eps_range[(0, 1), self.current_eps_idx - 1]

    current_MN = Property(depends_on='current_eps_idx,modified')
    @cached_property
    def _get_current_MN(self):
        return self._get_MN_fn(*self.current_eps)

    def plot_eps(self, ax):
        ax.plot(-self.eps_range, [0, self.cs.matrix_cs_with_state.geo.height], color='black')
        ax.plot(-self.current_eps, [0, self.cs.matrix_cs_with_state.geo.height], lw=3, color='red')

        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

    def plot_MN(self, ax):
        ax.plot(self.MN_arr[0], -self.MN_arr[1], lw=2, color='blue')
        ax.plot(self.current_MN[0], -self.current_MN[1], 'g.', markersize=20.0, color='red')

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(b=None, which='major')
        x1, x2, z1, z2 = ax.axis()
        ax.axis([0, x2, z1, z2])

    def plot_custom(self, ax, color='blue', linestyle='-', linewidth=2, label='<unnamed>'):
        M = self.MN_arr[0]
        N = -self.MN_arr[1]
        ax.plot(M, N, lw=linewidth, color=color, ls=linestyle, label=label)

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(b=None, which='major')
        x1, x2, z1, z2 = ax.axis()
        z_min = np.min(np.hstack([[z1], N]))
        z_max = np.max(np.hstack([[z2], N]))
        x_max = np.max(np.hstack([[x2], M]))
        ax.axis([0, x_max, z_min, z_max])

    #===========================================================================
    # Visualisation related attributes
    #===========================================================================

    def plot(self, fig):
        ax1 = fig.add_subplot(1, 2, 1)
        self.plot_eps(ax1)
        ax2 = fig.add_subplot(1, 2, 2)
        self.plot_MN(ax2)

    node_name = 'MxN diagram'

    traits_view = View(HSplit(Group(
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

    tree_view = View(Group(
                HGroup(
                Group(Item('n_eps', springy=True),
                      Item('current_eps_idx', editor=RangeEditor(low=1,
                                   high_name='n_eps_range',
                                   format='(%s)',
                                   mode='slider',
                                   auto_set=False,
                                   enter_set=False,
                                   ),
                           show_label=False,
                           ),
                      label='Discretization',
                      springy=True
                      ),
                springy=True,
                ),
                scrollable=True,
                ),
                width=1.0,
                height=0.8,
                resizable=True,
                buttons=['OK', 'Cancel'])

if __name__ == '__main__':
    pass
