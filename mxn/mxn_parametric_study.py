'''
Created on 6. 4. 2014

@author: Vancikv

'''

from traits.api import \
    HasStrictTraits, Instance, Property, \
    List, Str, Trait

from traitsui.api import \
    View, Item, VGroup

from cross_section import \
    CrossSection

from ecb_calib import \
    ECBCalib

from mxn_diagram import \
    MxNDiagram

from view import \
    MxNTreeNode

from reinf_layout import \
    RLCTexUniform

from matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

class MxNDescription(HasStrictTraits):
    '''Class controlling plotting options
    for an instance of MxNDiagram
    '''
    node_name = Str('<unnamed mxn diagram>')

    mxn = Instance(MxNDiagram)
    def _mxn_default(self):
        cs = CrossSection(reinf=[RLCTexUniform(n_layers=12)],
                          matrix_cs=MatrixCrossSection(geo=MCSGeoRect(width=0.2,
                                    height=0.06), n_cj=20, mm_key='default_mixture'))
        return MxNDiagram(cs=cs, n_eps=20)

    tree_node_list = Property(depends_on='mxn')
    def _get_tree_node_list(self):
        return [self.mxn]

    color = Trait('black', dict(black='k',
                                cyan='c',
                                green='g',
                                blue='b',
                                yellow='y',
                                magneta='m',
                                red='r')
                      )

    linestyle = Trait('solid', dict(solid='-',
                                    dashed='--',
                                    dash_dot='-.',
                                    dotted=':')
                      )

    view = View(VGroup(Item('node_name', label='label'),
                       Item('linestyle'),
                       Item('color'),
                       label='Plotting options'))

    def plot(self, fig):
        ax = fig.add_subplot(1, 1, 1)
        self.mxn.plot_MN_custom(ax=ax, color=self.color_, linestyle=self.linestyle_, label=self.node_name)

    def plot_ax(self, ax):
        self.mxn.plot_MN_custom(ax=ax, color=self.color_, linestyle=self.linestyle_, label=self.node_name)


class MxNParametricStudy(HasStrictTraits):
    '''Contains MxN diagrams wrapped in MxNDescription classes.
    MxNDescription controls plotting of particular MxNDiagram
    that can added/removed or modified ,e.g. via tree editor.
    '''

    node_name = Str('Parametric study')
    view = View()

    description_lst = List()
    def _description_lst_default(self):
        return [ECBCalib(), MxNDescription()]

    def plot(self, fig):
        ax = fig.add_subplot(1, 1, 1)
        for dsc in self.description_lst:
            if dsc.__class__ == MxNDescription:
                dsc.plot_ax(ax=ax)
        ax.legend()
        ax.set_xlabel('M[kNm]')
        ax.set_ylabel('N[kN]')
